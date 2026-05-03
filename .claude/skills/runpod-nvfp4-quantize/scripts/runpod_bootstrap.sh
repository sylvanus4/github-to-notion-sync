#!/usr/bin/env bash
# Bootstrap script run on the RunPod B200 pod.
# Installs deps, runs trace gate, smoke PTQ, vLLM sanity, and writes logs to /workspace/output/logs.

set -euo pipefail

LOG_DIR=/workspace/output/logs
mkdir -p "$LOG_DIR" /workspace/output/nvfp4

echo "=== gpu / cuda check ===" | tee "$LOG_DIR/00-env.log"
nvidia-smi 2>&1 | tee -a "$LOG_DIR/00-env.log"
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.version.cuda); print('device', torch.cuda.get_device_name(0)); print('cap', torch.cuda.get_device_capability(0))" 2>&1 | tee -a "$LOG_DIR/00-env.log"

echo "=== install modelopt + deps ===" | tee "$LOG_DIR/01-install.log"
python3 -m pip install --no-cache-dir --quiet --break-system-packages \
    "nvidia-modelopt[hf]==0.43.0" \
    "transformers>=4.46" \
    "accelerate>=1.0" \
    "datasets>=3.0" \
    "huggingface_hub>=0.27" \
    2>&1 | tail -30 | tee -a "$LOG_DIR/01-install.log"

python3 -c "
import importlib.metadata as md
for p in ['torch','transformers','accelerate','datasets','huggingface_hub','nvidia-modelopt']:
    try: print(f'{p}: {md.version(p)}')
    except Exception as e: print(f'{p}: ERROR {e}')
" 2>&1 | tee -a "$LOG_DIR/01-install.log"

# HF auth via env var (huggingface_hub reads HF_TOKEN automatically; no CLI login needed)
if [ -n "${HF_TOKEN:-}" ]; then
    export HF_TOKEN
    echo "HF_TOKEN exported (${#HF_TOKEN} chars)" | tee -a "$LOG_DIR/01-install.log"
fi

echo "=== build mini calibration set ===" | tee "$LOG_DIR/02-calib.log"
# datasets/pyarrow can SIGABRT on interpreter teardown — tolerate if output is good.
python3 /workspace/scripts/build_calib_mini.py 2>&1 | tee -a "$LOG_DIR/02-calib.log" || true
calib_lines=$(wc -l < /workspace/calib_mini.jsonl 2>/dev/null || echo 0)
echo "calib_mini.jsonl line count: $calib_lines" | tee -a "$LOG_DIR/02-calib.log"
if [ "$calib_lines" -lt 100 ]; then
    echo "CALIB FAILED: too few samples (<100)" | tee -a "$LOG_DIR/02-calib.log"
    exit 1
fi

echo "=== TRACE GATE (1 forward pass, no PTQ) ===" | tee "$LOG_DIR/03-trace.log"
timeout 1500 python3 /workspace/scripts/quantize_smoke.py \
    --trace-only \
    --timeout-sec 1400 \
    2>&1 | tee -a "$LOG_DIR/03-trace.log"

trace_rc=${PIPESTATUS[0]}
if [ "$trace_rc" -ne 0 ]; then
    echo "TRACE GATE FAILED (rc=$trace_rc) — aborting before PTQ" | tee -a "$LOG_DIR/03-trace.log"
    exit "$trace_rc"
fi

echo "=== SMOKE PTQ (8 samples, 2 layers) ===" | tee "$LOG_DIR/04-ptq.log"
timeout 1200 python3 /workspace/scripts/quantize_smoke.py \
    --max-samples 8 \
    --num-layers 2 \
    --timeout-sec 1100 \
    --output /workspace/output/nvfp4 \
    2>&1 | tee -a "$LOG_DIR/04-ptq.log"

ptq_rc=${PIPESTATUS[0]}
echo "ptq exit code: $ptq_rc" | tee -a "$LOG_DIR/04-ptq.log"

if [ "$ptq_rc" -eq 0 ]; then
    echo "=== install deep-gemm (NVFP4 backend for vLLM 0.7+) ===" | tee "$LOG_DIR/05a-deep-gemm.log"
    # vLLM 0.7+ FP4/FP8 path requires deep-gemm (Blackwell SM100 kernels).
    # Install before vllm so the engine's kernel_warmup doesn't RuntimeError.
    # Fallback to source build if no prebuilt wheel for the host CUDA version.
    python3 -m pip install --no-cache-dir --quiet --break-system-packages "deep-gemm" 2>&1 | tail -5 | tee -a "$LOG_DIR/05a-deep-gemm.log" \
        || python3 -m pip install --no-cache-dir --break-system-packages "git+https://github.com/deepseek-ai/DeepGEMM.git" 2>&1 | tail -10 | tee -a "$LOG_DIR/05a-deep-gemm.log" \
        || echo "WARN: deep-gemm install failed — vLLM sanity will fail but model artifact is still valid" | tee -a "$LOG_DIR/05a-deep-gemm.log"

    echo "=== vLLM SANITY ===" | tee "$LOG_DIR/05-vllm.log"
    python3 -m pip install --no-cache-dir --quiet --break-system-packages "vllm>=0.7.0" 2>&1 | tail -5 | tee -a "$LOG_DIR/05-vllm.log" || true
    timeout 600 python3 /workspace/scripts/vllm_sanity.py \
        --model /workspace/output/nvfp4 \
        --max-tokens 4 \
        2>&1 | tee -a "$LOG_DIR/05-vllm.log" || true
fi

echo "=== artifact summary ===" | tee "$LOG_DIR/06-summary.log"
ls -la /workspace/output/nvfp4 2>&1 | tee -a "$LOG_DIR/06-summary.log"
du -sh /workspace/output/nvfp4 2>&1 | tee -a "$LOG_DIR/06-summary.log"

echo "BOOTSTRAP DONE"
