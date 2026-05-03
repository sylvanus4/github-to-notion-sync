---
name: runpod-nvfp4-quantize
description: Quantize a HuggingFace LLM (especially Qwen3-MoE family) to NVFP4 (W4A4 group_size=16) on a RunPod B200 pod, using NVIDIA ModelOpt v0.43+ and a curated calibration mini-set (C4 + wikitext + KoAlpaca + tool-call). Two modes — `smoke` (8 calib samples × full model, ~3 min PTQ, validates the pipeline end-to-end) and `full` (8.6K calib for production). Handles RunPod pod lifecycle (create → SSH → bootstrap → upload → delete), uploads results to a HuggingFace Hub private repo, and writes a structured report.
---

# RunPod NVFP4 Quantization

End-to-end pipeline that turns `Qwen/Qwen3-30B-A3B` (or any HF-compatible LLM) into a vLLM-loadable **NVFP4 (W4A4, group_size=16)** checkpoint, on a RunPod B200 (Blackwell SM100) pod.

Battle-tested on 2026-05-01 against `Qwen/Qwen3-30B-A3B`. Produced 17.1 GB artifact in 137s of compute, total wall-clock ~25 min, total cost $3.48 (B200 ondemand, 38 min including a failed pod attempt with NGC image).

See `output/qwen3-nvfp4-smoke/REPORT.md` in the parent project for the original validation run.

## When to Use

- Need to quantize a HF LLM to NVFP4 for vLLM serving on B200 / B100 / Blackwell hardware
- Need a smoke-test to verify NVFP4 toolchain integrity for a new model architecture (Qwen3-MoE, DeepSeek-V3, Llama4 MoE, etc.) before committing to a full PTQ
- Need a reproducible RunPod recipe that won't get stuck on environment quirks

## Do NOT Use

- For pre-Blackwell GPUs (H100 / A100): NVFP4 Tensor Core not present → use INT8/FP8 instead
- For models < 7B: simpler `bitsandbytes` 4-bit is faster
- If you already have a working PTQ environment locally — this skill assumes no local GPU
- For inference benchmarking — this skill stops at "model loads in vLLM"; use `vllm-lmcache-integration` for serving benchmarks

## Inputs (caller must provide)

| Input | Required | Default | Notes |
|-------|----------|---------|-------|
| `MODEL_ID` | yes | — | HF model id, e.g. `Qwen/Qwen3-30B-A3B` |
| `HF_TOKEN` | yes (env) | from `.env` | Read access for source model + write access to target repo |
| `RUNPOD_API_KEY` | yes (env) | from `~/.runpod/config.toml` after `runpodctl config` | Account that owns the pod |
| `TARGET_HF_REPO` | yes | — | e.g. `ThakiCloud/Qwen3-30B-A3B-NVFP4` (must exist or be creatable; case sensitive — RunPod org slug is `ThakiCloud` not `thakicloud`) |
| `MODE` | no | `smoke` | `smoke` (8 calib × full layers, ~3 min PTQ) or `full` (8600 calib × full layers, ~1.5–3 h) |
| `STORAGE_MODE` | no | `ephemeral` | `ephemeral` (default — model downloaded on GPU pod's container disk) or `nfs` (model pre-downloaded to RunPod Network Volume via cheap CPU pod) |
| `NFS_VOLUME_ID` | nfs mode | — | RunPod Network Volume ID (from `runpodctl nv create`); required when `STORAGE_MODE=nfs` |
| `DC_PREFERENCE` | no | `EU-RO-1,US-CA-2,US-NC-2` | RunPod DCs with B200 stock; check `runpodctl dc list` first |
| `BUDGET_USD` | no | `6.00` | Hard cap; pod auto-deleted if exceeded |

## Workflow (10 phases, all enforced by `runpod_bootstrap.sh`)

### Default Mode (`STORAGE_MODE=ephemeral`)

```
P0 Pre-flight (local)         → P1 Create B200 pod (RunPod)
                                  ↓ (poll for SSH ready, ~3-5 min)
P3 Upload scripts (scp)       ← P2 SSH connect (proxy or direct)
                                  ↓
P4 Bootstrap on pod (background, monitored from local)
   ├─ install (modelopt 0.43, transformers 4.57+, datasets, accelerate)
   ├─ build calib (400 or 8600 samples, 4 sources)
   ├─ trace gate (model load + 1 forward; abort on NaN/OOM)
   ├─ PTQ (mtq.quantize() with NVFP4_DEFAULT_CFG)
   ├─ tokenizer save (separate from modelopt export)
   └─ vLLM sanity (best-effort; see Known Issues)
                                  ↓
P5 Download metadata (logs + JSON configs)
P6 Upload to HF Hub (logs + scripts + small files; weights pushed in MODE=full only)
P7 Delete pod (CRITICAL — costs $5.49/hr until deleted)
P8 Write REPORT.md
```

### NFS Pre-download Mode (`STORAGE_MODE=nfs`)

Separates model download from GPU compute to reduce B200 idle cost.

```
Phase A — Storage & Download (CPU pod, no GPU)
   A0 Create Network Volume (150GB)        ← runpodctl nv create --name "qwen3-nvfp4-models" --size 150
   A1 Create CPU pod (attached to NFS)     ← runpodctl pod create --compute-type CPU --volume-id $NFS_ID
   A2 Download model to /workspace/models/ ← huggingface-cli download $MODEL_ID --local-dir /workspace/models/$MODEL_ID
   A3 Delete CPU pod                       ← runpodctl pod delete $CPU_POD_ID

Phase B — Quantization (GPU pod, model already on NFS)
   P0 Pre-flight (local)         → P1 Create B200 pod (--volume-id $NFS_ID, --container-disk-in-gb 50)
                                      ↓ (poll for SSH ready, ~3-5 min)
   P3 Upload scripts (scp)       ← P2 SSH connect
                                      ↓
   P4 Bootstrap on pod (model loaded from /workspace/models/, NO download)
      ├─ install deps
      ├─ build calib
      ├─ trace gate (model path = /workspace/models/$MODEL_ID)
      ├─ PTQ
      ├─ tokenizer save
      └─ vLLM sanity
                                      ↓
   P5–P8 same as default mode

Phase C — Cleanup
   C1 Delete GPU pod (CRITICAL)
   C2 NFS Volume: keep ($10.5/월) for future runs or delete
```

## Critical Pre-flight Checks (DO NOT SKIP)

Before creating any pod, verify all six:

1. `runpodctl version` — CLI present (`brew install --cask runpod/runpodctl/runpodctl` or release tarball)
2. `runpodctl config --apiKey "$RUNPOD_API_KEY"` succeeded (writes `~/.runpod/config.toml`)
3. `python3 -c "from huggingface_hub import HfApi; print(HfApi(token=...).whoami())"` returns expected user
4. `python3 -c "from huggingface_hub import HfApi; HfApi(token=...).model_info('$MODEL_ID')"` succeeds (resolves gating)
5. `runpodctl dc list` shows target DC has B200 stock ≠ EMPTY
6. Target HF Hub repo exists (or `HfApi.create_repo(..., exist_ok=True)` first) — note org slug is case-sensitive

## Pod Creation (validated)

Use **template `runpod-torch-v280`** (RunPod-native, pre-cached image). Do NOT use NGC images directly — `nvcr.io/nvidia/pytorch:25.02-py3` was observed to hang at uptime=0 for 14+ min in US-CA-2.

### Default Mode (`STORAGE_MODE=ephemeral`)

```bash
runpodctl pod create \
    --compute-type GPU \
    --gpu-id "NVIDIA B200" \
    --gpu-count 1 \
    --cloud-type SECURE \
    --data-center-ids "$DC_PREFERENCE" \
    --template-id runpod-torch-v280 \
    --container-disk-in-gb 100 \
    --volume-in-gb 0 \
    --name "qwen3-nvfp4-$(date +%s)" \
    --ssh \
    -o yaml
```

Notes:
- Container disk 100GB (model 60GB + deps 10GB + output 17GB + headroom)
- Volume 0 (ephemeral; smoke is one-shot, no persistence needed)
- `runpod-torch-v280` = `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404` (CUDA 12.8.1 + PyTorch 2.8, B200 SM100 native)

### NFS Mode (`STORAGE_MODE=nfs`)

**Phase A — CPU pod for model download:**

```bash
runpodctl pod create \
    --compute-type CPU \
    --cloud-type SECURE \
    --data-center-ids "$DC_PREFERENCE" \
    --template-id runpod-torch-v280 \
    --container-disk-in-gb 20 \
    --volume-id "$NFS_VOLUME_ID" \
    --name "qwen3-download-$(date +%s)" \
    --ssh \
    -o yaml
```

**Phase B — GPU pod with NFS attached (model already downloaded):**

```bash
runpodctl pod create \
    --compute-type GPU \
    --gpu-id "NVIDIA B200" \
    --gpu-count 1 \
    --cloud-type SECURE \
    --data-center-ids "$DC_PREFERENCE" \
    --template-id runpod-torch-v280 \
    --container-disk-in-gb 50 \
    --volume-id "$NFS_VOLUME_ID" \
    --name "qwen3-nvfp4-$(date +%s)" \
    --ssh \
    -o yaml
```

Notes:
- Container disk reduced to 50GB (model NOT on container disk — loaded from NFS `/workspace/models/`)
- `--volume-id` attaches the pre-populated Network Volume containing the downloaded model
- GPU pod starts quantization immediately without download wait

## SSH Connection (validated)

Once `runpodctl pod get $POD_ID -o yaml` shows `ssh.ip` and `ssh.port` (not just `ssh.error`), connect via:

```bash
ssh -o StrictHostKeyChecking=no -o BatchMode=yes \
    -i ~/.runpod/ssh/RunPod-Key-Go \
    -p $POD_PORT \
    root@$POD_IP
```

The CLI auto-generates `~/.runpod/ssh/RunPod-Key-Go` (RSA, registered to account on first `runpodctl config`). Do NOT assume `~/.ssh/id_ed25519` works — it depends on whether the user uploaded their own key to RunPod first.

## Bootstrap on Pod

The `scripts/runpod_bootstrap.sh` runs on the pod and is the single source of truth for the install/PTQ/vLLM sequence. It:

- Uses `python3 -m pip install --break-system-packages` (Ubuntu 24.04 PEP 668 enforces externally-managed env)
- Reads `HF_TOKEN` from env (set via uploaded `/workspace/.hf_token` file before launch)
- Writes per-stage logs to `/workspace/output/logs/{00-env,01-install,02-calib,03-trace,04-ptq,05-vllm,06-summary}.log`
- Has internal timeouts: trace 25min, PTQ 20min, vLLM 10min
- Tolerates `build_calib_mini.py` SIGABRT on teardown (datasets/pyarrow C++ dtor race) — verifies output line count instead

## NVFP4 Recipe (the core 4 lines)

```python
import modelopt.torch.quantization as mtq
cfg = mtq.NVFP4_DEFAULT_CFG
mtq.quantize(model, cfg, forward_loop=lambda m: [m(**enc) for enc in calib_loader])
modelopt.torch.export.export_hf_checkpoint(model, export_dir=output_path)
```

Resulting `config.json` quantization_config:
- W4A4: `input_activations.num_bits=4, type=float, group_size=16` + same for `weights`
- Targets: `["Linear"]`
- Auto-ignored: `lm_head` + all `model.layers.*.mlp.gate` (router gates kept in BF16)

For Qwen3-MoE specifically, ModelOpt 0.43 auto-registers:
- `Qwen3MoeAttention` → `_QuantAttention` (KV cache support)
- `Qwen3MoeSparseMoeBlock` → `_QuantSparseMoe` (expert tensor quant)

## Tokenizer Caveat (must-fix)

`modelopt.torch.export.export_hf_checkpoint` **does not save tokenizer files**. vLLM constructor will fail with `TypeError('expected str, bytes or os.PathLike object, not NoneType')` if you try to load the export dir directly. After PTQ, always:

```python
AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True).save_pretrained(output_dir)
```

This adds: `tokenizer.json`, `vocab.json`, `merges.txt`, `tokenizer_config.json`, `special_tokens_map.json`, `added_tokens.json`, `chat_template.jinja`.

## Known Issues / Gotchas (battle-tested)

| Issue | Symptom | Fix |
|-------|---------|-----|
| NGC pytorch image hangs | `uptimeSeconds: 0`, `ssh.error: pod not ready` after 10+ min | Use RunPod template `runpod-torch-v280`, not raw NGC image |
| `mteb/miracl-ko` 404 | dataset load fails | Use `beomi/KoAlpaca-v1.1a` for Korean calibration |
| PEP 668 pip block | `× This environment is externally managed` | `pip install --break-system-packages` |
| `build_calib_mini.py` SIGABRT exit 134 | datasets/pyarrow teardown C++ exception | Allow `\|\| true`, verify line count of `calib_mini.jsonl` |
| `mtq.quantize` schema rejection | `pydantic ValidationError: Cannot specify only {'enable': True}` | Don't try to restrict by layer regex — use full default cfg |
| vLLM NVFP4 path needs `deep_gemm` | `RuntimeError: DeepGEMM backend is not available` | 2-tier fallback in `runpod_bootstrap.sh:73-76` — (1) PyPI `pip install deep-gemm` → (2) git source `pip install git+https://github.com/deepseek-ai/DeepGEMM.git` → (3) warn-and-skip. All branches use `--break-system-packages` (PEP 668). Model artifact stays valid even if all 3 fail; only vLLM sanity is gated. |
| HF org slug case sensitive | `403 Forbidden: don't have rights under namespace "thakicloud"` | Use `ThakiCloud` (TitleCase) |
| RunPod no instances available | GPU stock exhausted in selected data center | Retry across data centers; use H100 SXM as fallback (B200 > H100 SXM). Check `runpodctl dc list` for availability |
| deep-gemm PyPI install fails | No pre-built binary wheels on PyPI | Build from GitHub source: `pip install git+https://github.com/deepseek-ai/DeepGEMM.git --break-system-packages`. Requires CUDA 12.8+ and C++17 |
| Disk full (`/` 100%) on pod | HF cache downloads fill container root filesystem | Set `HF_HOME=/workspace/.cache/huggingface` before any model download |
| cuDNN Frontend error during model load | Flash Attention incompatibility on H100/B200 | Pass `attn_implementation="eager"` to `AutoModelForCausalLM.from_pretrained()`. Disables Flash Attention (~10-20% slowdown) |
| Full PTQ exceeds timeout (4h+) | 8600-sample calibration on large MoE models | Use Smoke PTQ (8 samples) for pipeline validation; set `signal.alarm(14400)` as hard guard |
| DeepGEMM backend not available (vLLM) | vLLM 0.8+ FP8 codepath requires DeepGEMM at import time | Skip vLLM sanity; validate NVFP4 quantized artifact by loading checkpoint separately |
| Model download took >30 min on GPU pod | Large model (60GB+) on slow DC or congested network | **Use `STORAGE_MODE=nfs`**: pre-download to Network Volume via $0.10/hr CPU pod, then attach to GPU pod. Eliminates download wait from B200 billing entirely |

## Cost Reference (B200 ondemand $5.49/hr)

| Phase | Time | Cost |
|-------|------|------|
| Pod boot + install | 4–8 min | $0.37–$0.73 |
| Model download (60GB Qwen3-30B-A3B → ~3.5 GB/s on B200 pod) | <1 min | $0.09 |
| Trace gate | <1 min | $0.09 |
| PTQ smoke (8 calib × full) | 1.5 min | $0.14 |
| PTQ full (8600 calib × full) | 1.5–3h | $8.20–$16.50 |
| vLLM sanity (with deep_gemm pre-installed) | 5 min | $0.46 |
| HF upload + cleanup | 5 min | $0.46 |
| **smoke total** | **~25 min** | **~$2.30** |
| **full total** | **~3h** | **~$16** |

### NFS Mode Additional Cost (`STORAGE_MODE=nfs`)

| Phase | Time | Cost |
|-------|------|------|
| Network Volume 150GB (persistent) | ongoing | $10.5/month ($0.07/GB) |
| CPU pod boot + model download (57GB) | ~30 min | ~$0.05 ($0.10/hr) |
| GPU pod (container-disk reduced to 50GB) | same as default | same as default |
| **NFS smoke total** | **~25 min GPU + ~30 min CPU** | **~$2.35 + $10.5/month storage** |

NFS mode adds ~$0.05 one-time CPU cost per download but saves 15–30 min of B200 idle time ($1.37–$2.75) on repeated runs. The Network Volume persists across runs — subsequent quantizations skip the download entirely.

Always set `BUDGET_USD` cap and check `pod list -a` before proceeding.

## Outputs

```
{project_root}/output/{run_name}/
├── PLAN.md                        — input plan (caller-provided)
├── REPORT.md                      — auto-written, single source of truth for results
├── scripts/                       — copy of skill scripts that ran
├── logs/                          — 7 per-stage logs from pod
├── artifact-meta/                 — config.json, hf_quant_config.json, tokenizer files
└── (optional) weights/            — only if MODE=full and weights downloaded locally
```

Plus on HF Hub:
- `{TARGET_HF_REPO}/logs/*.log`
- `{TARGET_HF_REPO}/scripts/*`
- `{TARGET_HF_REPO}/PLAN.md`, `REPORT.md`
- `{TARGET_HF_REPO}/model-*.safetensors` (only in MODE=full)

## Cleanup Protocol (CRITICAL)

Before declaring task done, **always**:

```bash
runpodctl pod delete $POD_ID
runpodctl pod list -a | grep -c "$POD_ID"   # must be 0
```

Pods cost $5.49/hr until deleted. A forgotten pod over a weekend = $920.

## Reference Run

Smoke test 2026-05-01:
- Model: `Qwen/Qwen3-30B-A3B` (30.5B params, 48 layers, 128 experts)
- Calib: 400 samples (C4 100 + wikitext 100 + KoAlpaca 100 + tool-call 100)
- PTQ: 8 samples, full layers, 60s wall-clock
- Output: 17.1GB NVFP4 (3.5× compression vs 60GB BF16)
- 56,211 quantizers inserted, MoE/Attention auto-registered
- Total run: 25 min, $2.30 (B200 ondemand US-CA-2)
- Result: PASS for S1-S6 + S8-S10. S7 (vLLM load) failed on `deep_gemm` env, model artifact valid.
- Full report: `output/qwen3-nvfp4-smoke/REPORT.md`
- Output repo: https://huggingface.co/ThakiCloud/Qwen3-30B-A3B-NVFP4-smoke (private)

## Scripts (in `scripts/`)

| File | Purpose |
|------|---------|
| `build_calib_mini.py` | 4-source calibration JSONL builder; env vars `CALIB_N_PER_SOURCE` (default 100) and `CALIB_OUT` |
| `quantize_smoke.py` | ModelOpt PTQ runner; flags `--model`, `--calib`, `--output`, `--max-samples`, `--num-layers` (currently unused due to schema), `--timeout-sec`, `--trace-only` |
| `vllm_sanity.py` | vLLM constructor + 1-token generate; flags `--model`, `--quant` (default `modelopt_fp4`), `--max-tokens` |
| `runpod_bootstrap.sh` | Stages 00-06 sequenced with timeouts; reads `HF_TOKEN` from env, writes logs to `/workspace/output/logs/` |

## Skill Lifecycle Notes

- v1.0 (2026-05-01): initial extraction from validated smoke run on Qwen3-30B-A3B
- Open issues to address in v1.1:
  - Add `deep_gemm` install to bootstrap (vLLM sanity will then PASS)
  - Add `MODE=full` path with 8.6K calibration set (currently smoke-only logic)
  - Add automatic HF org slug normalization
  - Multi-DC fallback in pod create command (currently caller specifies)
  - NFS pre-download mode (`STORAGE_MODE=nfs`) for cost-optimized repeated quantization runs
