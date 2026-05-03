#!/usr/bin/env python3
"""Stop-hook that auto-compiles the intelligence KB when new artifacts arrived.

Triggered after every Claude turn. Cheap fast-path: if the flag file
`knowledge-bases/intelligence/.compile-pending` does not exist, exit 0
immediately. This is the common case (most turns don't write to the KB).

When the flag IS present, run kb_auto_compile.py for the intelligence
topic, then delete the flag. Output is silent on success; errors print
to stderr but never block Claude (always exit 0).

Wired into settings.json `hooks.Stop[].hooks[]` array.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INTEL_DIR = REPO_ROOT / "knowledge-bases" / "intelligence"
FLAG = INTEL_DIR / ".compile-pending"
COMPILE_SCRIPT = REPO_ROOT / "scripts" / "kb_auto_compile.py"
LOG_PATH = REPO_ROOT / ".claude" / "skills" / "jarvis" / "state" / "kb-intel-compile.log"


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(msg.rstrip() + "\n")


def main() -> int:
    # Read hook input (Stop hook receives JSON on stdin per Claude Code spec)
    try:
        payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    except json.JSONDecodeError:
        payload = {}

    # Avoid re-entering when our own activity triggered the stop
    if payload.get("stop_hook_active"):
        return 0

    # Fast path: nothing to do
    if not FLAG.exists():
        return 0

    if not COMPILE_SCRIPT.exists():
        log(f"WARN: compile script missing at {COMPILE_SCRIPT}")
        return 0

    # Run mechanical compile (no LLM call)
    try:
        result = subprocess.run(
            ["python3", str(COMPILE_SCRIPT), "intelligence"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        log(f"compile rc={result.returncode}; stdout last 200ch: {result.stdout[-200:]!r}")
        if result.returncode == 0:
            try:
                FLAG.unlink()
                log("flag cleared")
            except OSError as e:
                log(f"WARN: could not clear flag: {e}")
        else:
            log(f"compile FAILED stderr: {result.stderr[-300:]!r}")
    except subprocess.TimeoutExpired:
        log("compile TIMEOUT after 60s — flag preserved for retry")
    except Exception as e:
        log(f"compile EXCEPTION: {e!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
