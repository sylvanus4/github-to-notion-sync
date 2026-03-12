# Webhooks: Trigger Jobs on Events

Trigger jobs automatically when changes happen in Hugging Face repositories.

## Create Webhook

**Python API:**
```python
from huggingface_hub import create_webhook

webhook = create_webhook(
    job_id=job.id,
    watched=[
        {"type": "user", "name": "your-username"},
        {"type": "org", "name": "your-org-name"}
    ],
    domains=["repo", "discussion"],
    secret="your-secret"
)
```

## How It Works

1. Webhook listens for changes in watched repositories
2. When triggered, the job runs with `WEBHOOK_PAYLOAD` environment variable
3. Your script can parse the payload to understand what changed

## Use Cases

- Auto-process new datasets when uploaded
- Trigger inference when models are updated
- Run tests when code changes
- Generate reports on repository activity

## Access Webhook Payload in Script

```python
import os
import json

payload = json.loads(os.environ.get("WEBHOOK_PAYLOAD", "{}"))
print(f"Event type: {payload.get('event', {}).get('action')}")
```

## Documentation

See [Webhooks Documentation](https://huggingface.co/docs/huggingface_hub/guides/webhooks) for more details.
