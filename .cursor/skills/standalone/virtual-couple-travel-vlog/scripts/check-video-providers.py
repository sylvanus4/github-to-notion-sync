#!/usr/bin/env python3
"""Detect available video generation providers and report status.

Checks for:
  - Topview skill (via env var or known skill paths)
  - Remotion (via npx availability)
  - Generic API providers (via env vars)
"""

import os
import shutil
import sys
from pathlib import Path


def check_topview() -> dict:
    candidates = []
    env_skill = os.environ.get("TOPVIEW_SKILL")
    if env_skill:
        candidates.append(Path(env_skill) / "scripts" / "video_gen.py")

    home = Path.home()
    candidates.extend([
        home / ".agents" / "skills" / "topview" / "scripts" / "video_gen.py",
        home / ".codex" / "skills" / "topview" / "scripts" / "video_gen.py",
        home / ".cursor" / "skills" / "topview" / "scripts" / "video_gen.py",
    ])

    for c in candidates:
        if c.exists():
            return {"available": True, "path": str(c), "mode": "omni-reference"}

    return {"available": False, "path": None, "mode": None}


def check_remotion() -> dict:
    npx = shutil.which("npx")
    if npx:
        return {"available": True, "tool": "npx remotion render"}
    return {"available": False, "tool": None}


def check_env_providers() -> list[dict]:
    providers = []
    env_keys = {
        "SEEDANCE_API_KEY": "Seedance",
        "KREA_API_KEY": "Krea",
        "LOVART_API_KEY": "Lovart",
        "RUNWAY_API_KEY": "Runway",
        "PIKA_API_KEY": "Pika",
    }
    for key, name in env_keys.items():
        if os.environ.get(key):
            providers.append({"name": name, "env_key": key, "available": True})
    return providers


def main() -> int:
    print("=== Video Provider Check ===\n")

    topview = check_topview()
    print(f"  Topview:  {'AVAILABLE' if topview['available'] else 'NOT FOUND'}")
    if topview["available"]:
        print(f"            Path: {topview['path']}")
        print(f"            Mode: {topview['mode']}")

    remotion = check_remotion()
    print(f"  Remotion: {'AVAILABLE' if remotion['available'] else 'NOT FOUND'}")
    if remotion["available"]:
        print(f"            Tool: {remotion['tool']}")

    env_providers = check_env_providers()
    if env_providers:
        print(f"\n  API Providers ({len(env_providers)} detected):")
        for p in env_providers:
            print(f"    - {p['name']} ({p['env_key']})")
    else:
        print("\n  No additional API provider keys detected in environment.")

    print()
    available_count = (1 if topview["available"] else 0) + (1 if remotion["available"] else 0) + len(env_providers)
    if available_count == 0:
        print("No video providers available. Manual mode will be used.")
        print("Prompts and reference images will still be generated for manual upload.")
        return 1
    else:
        print(f"{available_count} provider(s) available.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
