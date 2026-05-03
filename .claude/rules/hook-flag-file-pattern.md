# Stop Hook Flag-File Pattern

When you need to trigger expensive work (compile, index, distill) only after specific producer turns — not every turn — use a flag-file gated by a Stop hook.

## When to Use

- Producer skill writes data that should be processed but not on every turn (e.g., KB ingest → wiki recompile)
- Work is idempotent and cheap enough to run inline once flag is set
- You want zero overhead on turns where nothing changed

## Pattern (proven 2x)

1. **Producer skill** writes data file AND `touch` a flag file at known path:
   - Example: `knowledge-bases/intelligence/.compile-pending`
2. **Stop hook** (registered in `.claude/settings.json` `hooks.Stop`) does:
   - Fast path: `if not flag_path.exists(): exit(0)` — zero cost
   - Slow path: read input JSON from stdin, run work, delete flag, exit 0
3. **Re-entry guard**: check `stop_hook_active` from stdin; if true, exit silently — Stop fires once per actual stop, hook itself counts as activity

## Boilerplate

```python
#!/usr/bin/env python3
import json, sys, subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]  # adjust depth!
FLAG = REPO_ROOT / "<producer-output-dir>" / ".your-flag"

def main() -> int:
    if not FLAG.exists():
        return 0  # fast path
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except Exception:
        payload = {}
    if payload.get("stop_hook_active"):
        return 0  # avoid re-entry
    subprocess.run(["python3", str(REPO_ROOT / "scripts/<work>.py")], timeout=120)
    FLAG.unlink(missing_ok=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Anti-Patterns

- Don't run work unconditionally on every Stop — adds latency to every turn
- Don't put long-running work (>30s) inline — schedule a background agent instead
- Don't write to flag from inside the hook — only from the producer skill
- Don't forget to delete flag after work — leads to perpetual re-runs

## Existing Examples

- `.claude/hooks/kb-intel-compile.py` — `.compile-pending` → `kb_auto_compile.py intelligence`
- `.claude/skills/jarvis/hooks/goal-continuation.py` — uses goal-state JSON files (similar idea, no separate flag — pursuing status IS the flag)
