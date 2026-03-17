# Deployment Guide — Winner Hardware Selection

## Hardware Selection by Model Size

| Model Parameters | Recommended Instance | VRAM Required | Estimated Cost |
|-----------------|---------------------|---------------|---------------|
| < 3B | `nvidia-t4` (x1) | 8-12 GB | ~$0.50/hr |
| 3B - 8B | `nvidia-a10g` (x1) | 16-24 GB | ~$1.05/hr |
| 8B - 14B | `nvidia-a10g` (x2) or `nvidia-a100` | 32-48 GB | ~$2.10-4.50/hr |
| 14B - 34B | `nvidia-a100` (x1) | 48-80 GB | ~$4.50/hr |
| 34B - 70B | `nvidia-a100` (x2) or `nvidia-h100` | 80-160 GB | ~$9.00-16.00/hr |
| > 70B | Multi-GPU A100/H100 | 160+ GB | ~$16.00+/hr |

## Quantization Options

If model is too large for target hardware, consider quantization:

| Quantization | Memory Reduction | Quality Impact | Support |
|-------------|-----------------|---------------|---------|
| FP16 | ~50% vs FP32 | Negligible | Universal |
| INT8 (bitsandbytes) | ~50% vs FP16 | Minimal | Wide |
| GPTQ (4-bit) | ~75% vs FP16 | Small | Growing |
| AWQ (4-bit) | ~75% vs FP16 | Small | Growing |
| GGUF (various) | Varies | Varies | llama.cpp |

## Deployment Configuration Template

```bash
hf endpoints deploy arena-winner-{TASK} \
  --repo {WINNER_MODEL_ID} \
  --framework pytorch \
  --accelerator gpu \
  --instance-type {RECOMMENDED_INSTANCE} \
  --instance-size x1 \
  --min-replica 1 \
  --max-replica 1 \
  --region us-east-1 \
  --vendor aws \
  --namespace {ORG}
```

## Cost Optimization

1. **Scale-to-zero**: Use for infrequent inference
   ```bash
   hf endpoints scale-to-zero arena-winner-TASK
   ```

2. **Pause when not needed**: Use for development/testing
   ```bash
   hf endpoints pause arena-winner-TASK
   ```

3. **Right-size**: Start small, scale up only if latency SLOs are not met
