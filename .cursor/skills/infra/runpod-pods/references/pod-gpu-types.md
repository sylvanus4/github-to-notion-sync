# RunPod GPU Types Reference

Common GPU IDs for use with `runpodctl pod create --gpu-id <ID>`.

Run `runpodctl gpu list --output table` for the live list with current availability.

## Consumer / Professional GPUs

| GPU ID | GPU | VRAM | Use Case |
|--------|-----|------|----------|
| `RTX_3090` | NVIDIA RTX 3090 | 24 GB | Budget inference, small training |
| `RTX_4080` | NVIDIA RTX 4080 | 16 GB | Inference, light fine-tuning |
| `RTX_4090` | NVIDIA RTX 4090 | 24 GB | Inference, fine-tuning, dev work |
| `RTX_A5000` | NVIDIA RTX A5000 | 24 GB | Professional inference |
| `RTX_A6000` | NVIDIA RTX A6000 | 48 GB | Large model inference, training |

## Data Center GPUs

| GPU ID | GPU | VRAM | Use Case |
|--------|-----|------|----------|
| `A100_PCIE` | NVIDIA A100 PCIe | 40/80 GB | Training, large-batch inference |
| `A100_SXM` | NVIDIA A100 SXM | 80 GB | Multi-GPU training (NVLink) |
| `H100_SXM` | NVIDIA H100 SXM | 80 GB | Frontier training, fastest option |
| `H100_PCIE` | NVIDIA H100 PCIe | 80 GB | High-performance training |
| `L40S` | NVIDIA L40S | 48 GB | Inference, mixed precision training |
| `A40` | NVIDIA A40 | 48 GB | Balanced training and inference |

## Approximate Hourly Costs

Costs vary by availability and cloud tier. Community tier is typically 2-3x cheaper than secure tier.

| GPU | Secure ($/hr) | Community ($/hr) |
|-----|--------------|-----------------|
| RTX 4090 | ~$0.44 | ~$0.16 |
| A100 SXM 80GB | ~$1.64 | ~$0.64 |
| H100 SXM 80GB | ~$3.89 | ~$1.49 |
| RTX A6000 | ~$0.79 | ~$0.32 |

Check current pricing at [runpod.io/pricing](https://www.runpod.io/pricing) or via `runpodctl gpu list`.

## Selection Guide

| Scenario | Recommended GPU |
|----------|----------------|
| Quick experiment / dev | `RTX_4090` (community) |
| Fine-tuning 7B model | `A100_PCIE` or `RTX_A6000` |
| Training 13B-70B model | `A100_SXM` x 2-4 |
| Frontier training (100B+) | `H100_SXM` x 4-8 |
| Inference serving | `RTX_4090` or `L40S` |
| Budget inference | `RTX_3090` (community) |
