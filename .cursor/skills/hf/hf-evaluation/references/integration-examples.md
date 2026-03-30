# HF Evaluation Integration Examples

## Python Script Integration

```python
import subprocess
import os

def update_model_evaluations(repo_id, readme_content):
    """Update model card with evaluations from README."""
    result = subprocess.run([
        "python", "scripts/evaluation_manager.py",
        "extract-readme",
        "--repo-id", repo_id,
        "--create-pr"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Successfully updated {repo_id}")
    else:
        print(f"Error: {result.stderr}")
```
