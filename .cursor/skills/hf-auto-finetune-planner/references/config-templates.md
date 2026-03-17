# Training Config Templates

## SFT (Supervised Fine-Tuning) — LoRA

```yaml
model_id: "{MODEL_ID}"
dataset_id: "{DATASET_ID}"
training_method: "sft"
hardware_flavor: "a10g-large"
hyperparameters:
  learning_rate: 2e-5
  num_epochs: 3
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  warmup_ratio: 0.1
  weight_decay: 0.01
  max_seq_length: 512
  fp16: true
lora:
  r: 16
  alpha: 32
  dropout: 0.05
  target_modules: ["q_proj", "k_proj", "v_proj", "o_proj"]
output_repo: "{ORG}/{MODEL_NAME}-sft"
push_to_hub: true
```

## DPO (Direct Preference Optimization)

```yaml
model_id: "{MODEL_ID}"
dataset_id: "{DATASET_ID}"
training_method: "dpo"
hardware_flavor: "a100-large"
hyperparameters:
  learning_rate: 5e-7
  num_epochs: 1
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  warmup_ratio: 0.1
  beta: 0.1
  max_length: 1024
  max_prompt_length: 512
  fp16: true
lora:
  r: 16
  alpha: 32
  dropout: 0.05
output_repo: "{ORG}/{MODEL_NAME}-dpo"
push_to_hub: true
```

## GRPO (Group Relative Policy Optimization)

```yaml
model_id: "{MODEL_ID}"
dataset_id: "{DATASET_ID}"
training_method: "grpo"
hardware_flavor: "a100-large"
hyperparameters:
  learning_rate: 1e-6
  num_epochs: 1
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  max_length: 2048
  max_prompt_length: 1024
  num_generations: 4
  fp16: true
lora:
  r: 16
  alpha: 32
  dropout: 0.05
output_repo: "{ORG}/{MODEL_NAME}-grpo"
push_to_hub: true
```

## Reward Model Training

```yaml
model_id: "{MODEL_ID}"
dataset_id: "{DATASET_ID}"
training_method: "reward_model"
hardware_flavor: "a10g-large"
hyperparameters:
  learning_rate: 1e-5
  num_epochs: 1
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  max_length: 512
  fp16: true
output_repo: "{ORG}/{MODEL_NAME}-rm"
push_to_hub: true
```
