# Cost Estimation Reference

## HF Jobs Hardware Pricing (approximate, check `hf jobs hardware` for latest)

| Flavor | GPU | VRAM | FP16 TFLOPS | Est. $/hr |
|--------|-----|------|-------------|-----------|
| `cpu-basic` | None | N/A | N/A | ~$0.10 |
| `cpu-upgrade` | None | N/A | N/A | ~$0.20 |
| `a10g-small` | 1x A10G | 24 GB | ~125 | ~$1.05 |
| `a10g-large` | 4x A10G | 96 GB | ~500 | ~$3.15 |
| `a100-large` | 1x A100 | 80 GB | ~312 | ~$4.50 |
| `h100` | 1x H100 | 80 GB | ~990 | ~$8.00 |

## Training Time Estimation Formula

```
tokens_total = dataset_rows * avg_tokens_per_row * num_epochs
time_seconds = tokens_total / (throughput_tokens_per_sec)
time_hours = time_seconds / 3600
cost = time_hours * hourly_rate
```

## Throughput Estimates (tokens/sec, LoRA fine-tuning)

| Model Size | A10G (24GB) | A100 (80GB) | H100 (80GB) |
|-----------|-------------|-------------|-------------|
| 1-3B | ~2000 | ~4000 | ~8000 |
| 7-8B | ~800 | ~2000 | ~4000 |
| 13-14B | ~400 | ~1200 | ~2500 |
| 32-34B | N/A (OOM) | ~600 | ~1500 |
| 70B | N/A | ~200 (QLoRA) | ~600 |

## Quick Estimate Examples

| Scenario | Dataset | Model | Hardware | Time | Cost |
|----------|---------|-------|----------|------|------|
| Small classification | 10K rows, 3 epochs | 7B | A10G | ~2h | ~$2 |
| Medium SFT | 50K rows, 3 epochs | 7B | A100 | ~6h | ~$27 |
| Large instruction | 100K rows, 2 epochs | 14B | A100 | ~12h | ~$54 |
| Full fine-tune | 500K rows, 1 epoch | 7B | 4xA10G | ~8h | ~$25 |
