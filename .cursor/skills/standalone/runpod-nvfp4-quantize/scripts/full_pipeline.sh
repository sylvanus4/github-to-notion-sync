#!/usr/bin/env bash
set -euo pipefail

export HF_TOKEN=$(cat /workspace/.hf_token)
export HF_REPO="ThakiCloud/Qwen3-30B-A3B-NVFP4"
export MODEL_ID="Qwen/Qwen3-30B-A3B"

LOG=/workspace/output/logs
mkdir -p "$LOG" /workspace/output/nvfp4-smoke /workspace/output/nvfp4-full

# ====== STAGE 1: Environment + deep_gemm fix ======
echo "=== STAGE 1: ENV + DEEP_GEMM ===" | tee "$LOG/00-env.log"
nvidia-smi 2>&1 | tee -a "$LOG/00-env.log"

pip install --no-cache-dir --quiet --break-system-packages \
    "nvidia-modelopt[hf]==0.43.0" "transformers>=4.46" \
    "accelerate>=1.0" "datasets>=3.0" "huggingface_hub>=0.27" \
    2>&1 | tail -20 | tee -a "$LOG/01-install.log"

# deep_gemm: 3-tier fallback
pip install --no-cache-dir --break-system-packages "deep-gemm" 2>&1 | tee "$LOG/01a-deepgemm.log" \
    || pip install --no-cache-dir --break-system-packages \
       "git+https://github.com/deepseek-ai/DeepGEMM.git" 2>&1 | tee -a "$LOG/01a-deepgemm.log" \
    || { echo "FATAL: deep_gemm install failed" | tee -a "$LOG/01a-deepgemm.log"; exit 1; }

# vLLM nightly (deep_gemm compat)
pip install --no-cache-dir --break-system-packages "vllm>=0.7.0" \
    2>&1 | tail -10 | tee "$LOG/01b-vllm.log"

# ====== STAGE 1b: Smoke PTQ → vLLM Sanity (G1) ======
echo "=== STAGE 1b: SMOKE RE-RUN ===" | tee "$LOG/02-smoke.log"
python3 /workspace/scripts/build_calib_mini.py 2>&1 | tee -a "$LOG/02-smoke.log" || true
calib_lines=$(wc -l < /workspace/calib_mini.jsonl 2>/dev/null || echo "0")
echo "calib lines: $calib_lines" | tee -a "$LOG/02-smoke.log"

python3 /workspace/scripts/quantize_smoke.py \
    --max-samples 8 --output /workspace/output/nvfp4-smoke \
    2>&1 | tee -a "$LOG/02-smoke.log"

python3 -c "
from transformers import AutoTokenizer
AutoTokenizer.from_pretrained('$MODEL_ID', trust_remote_code=True) \
    .save_pretrained('/workspace/output/nvfp4-smoke')
" 2>&1 | tee -a "$LOG/02-smoke.log"

echo "=== STAGE 1c: vLLM SANITY (smoke) ===" | tee "$LOG/03-vllm-smoke.log"
timeout 600 python3 /workspace/scripts/vllm_sanity.py \
    --model /workspace/output/nvfp4-smoke --max-tokens 4 \
    2>&1 | tee -a "$LOG/03-vllm-smoke.log" || echo "vLLM smoke sanity timeout/fail (non-fatal)" | tee -a "$LOG/03-vllm-smoke.log"
echo "vLLM SANITY (smoke): rc=$?" | tee -a "$LOG/03-vllm-smoke.log"

# ====== STAGE 2: Full PTQ (G2) ======
echo "=== STAGE 2: FULL PTQ (8.6K calib) ===" | tee "$LOG/04-full-ptq.log"
CALIB_N_PER_SOURCE=2150 CALIB_OUT=/workspace/calib_full.jsonl \
    python3 /workspace/scripts/build_calib_mini.py 2>&1 | tee -a "$LOG/04-full-ptq.log" || true
full_lines=$(wc -l < /workspace/calib_full.jsonl 2>/dev/null || echo "0")
echo "full calib lines: $full_lines" | tee -a "$LOG/04-full-ptq.log"

timeout 14400 python3 /workspace/scripts/quantize_smoke.py \
    --model "$MODEL_ID" \
    --calib /workspace/calib_full.jsonl \
    --max-samples 8600 \
    --output /workspace/output/nvfp4-full \
    --timeout-sec 14000 \
    2>&1 | tee -a "$LOG/04-full-ptq.log"

python3 -c "
from transformers import AutoTokenizer
AutoTokenizer.from_pretrained('$MODEL_ID', trust_remote_code=True) \
    .save_pretrained('/workspace/output/nvfp4-full')
" 2>&1 | tee -a "$LOG/04-full-ptq.log"

echo "=== STAGE 2b: vLLM SANITY (full) ===" | tee "$LOG/05-vllm-full.log"
timeout 600 python3 /workspace/scripts/vllm_sanity.py \
    --model /workspace/output/nvfp4-full --max-tokens 16 \
    2>&1 | tee -a "$LOG/05-vllm-full.log" || echo "vLLM full sanity timeout/fail (non-fatal)" | tee -a "$LOG/05-vllm-full.log"

# ====== STAGE 3: HF Hub Upload (G3) ======
echo "=== STAGE 3: HF HUB UPLOAD ===" | tee "$LOG/06-upload.log"
pip install --quiet --break-system-packages hf_transfer 2>&1 | tee -a "$LOG/06-upload.log"
export HF_HUB_ENABLE_HF_TRANSFER=1
huggingface-cli upload "$HF_REPO" /workspace/output/nvfp4-full . \
    --repo-type model --commit-message "Full NVFP4 W4A4 (8.6K calib)" \
    2>&1 | tee -a "$LOG/06-upload.log"

# ====== STAGE 4: Benchmark (G4) ======
echo "=== STAGE 4: BENCHMARK ===" | tee "$LOG/07-bench.log"
python3 /workspace/scripts/benchmark.py 2>&1 | tee -a "$LOG/07-bench.log"

echo "=== ALL STAGES DONE ==="
