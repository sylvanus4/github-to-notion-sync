# Scheduled Jobs

Run jobs on a schedule using CRON expressions or predefined schedules.

## MCP Tool Examples

```python
# Schedule a UV script that runs every hour
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "@hourly",
    "flavor": "cpu-basic"
})

# Schedule with CRON syntax
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "0 9 * * 1",  # 9 AM every Monday
    "flavor": "cpu-basic"
})

# Schedule a Docker-based job
hf_jobs("scheduled run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Scheduled!')"],
    "schedule": "@daily",
    "flavor": "cpu-basic"
})
```

## Python API

```python
from huggingface_hub import create_scheduled_job, create_scheduled_uv_job

# Schedule a Docker job
create_scheduled_job(
    image="python:3.12",
    command=["python", "-c", "print('Running on schedule!')"],
    schedule="@hourly"
)

# Schedule a UV script
create_scheduled_uv_job("my_script.py", schedule="@daily", flavor="cpu-basic")

# Schedule with GPU
create_scheduled_uv_job(
    "ml_inference.py",
    schedule="0 */6 * * *",  # Every 6 hours
    flavor="a10g-small"
)
```

## Available Schedules

- `@annually`, `@yearly` - Once per year
- `@monthly` - Once per month
- `@weekly` - Once per week
- `@daily` - Once per day
- `@hourly` - Once per hour
- CRON expression - Custom schedule (e.g., `"*/5 * * * *"` for every 5 minutes)

## Manage Scheduled Jobs

**MCP Tool:**
```python
hf_jobs("scheduled ps")                              # List scheduled jobs
hf_jobs("scheduled inspect", {"job_id": "..."})     # Inspect details
hf_jobs("scheduled suspend", {"job_id": "..."})     # Pause
hf_jobs("scheduled resume", {"job_id": "..."})      # Resume
hf_jobs("scheduled delete", {"job_id": "..."})      # Delete
```

**Python API:**
```python
from huggingface_hub import (
    list_scheduled_jobs,
    inspect_scheduled_job,
    suspend_scheduled_job,
    resume_scheduled_job,
    delete_scheduled_job
)

scheduled = list_scheduled_jobs()
info = inspect_scheduled_job(scheduled_job_id)
suspend_scheduled_job(scheduled_job_id)
resume_scheduled_job(scheduled_job_id)
delete_scheduled_job(scheduled_job_id)
```
