#!/usr/bin/env python3
"""Wrapper for Topview Omni Reference video generation.

Finds the Topview skill's video_gen.py and invokes it with standardized
arguments for the virtual-couple-travel-vlog workflow.

Usage:
    python run-topview-omni.py \
        --prompt "A couple walking along Barcelona's Gothic Quarter..." \
        --images images/memory_sheet_01.png images/character_male.png images/character_female.png \
        --output videos/clip_01.mp4 \
        [--aspect 9:16] [--duration 15] [--model standard]
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def find_topview_script() -> str | None:
    env_skill = os.environ.get("TOPVIEW_SKILL")
    if env_skill:
        script = Path(env_skill) / "scripts" / "video_gen.py"
        if script.exists():
            return str(script)

    home = Path.home()
    candidates = [
        home / ".agents" / "skills" / "topview" / "scripts" / "video_gen.py",
        home / ".codex" / "skills" / "topview" / "scripts" / "video_gen.py",
        home / ".cursor" / "skills" / "topview" / "scripts" / "video_gen.py",
    ]

    for c in candidates:
        if c.exists():
            return str(c)

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Topview Omni Reference video generation.")
    parser.add_argument("--prompt", required=True, help="Video generation prompt text")
    parser.add_argument("--images", nargs="+", required=True, help="Reference image paths (memory sheet + character cards)")
    parser.add_argument("--output", required=True, help="Output video file path")
    parser.add_argument("--aspect", default="9:16", help="Aspect ratio (default: 9:16)")
    parser.add_argument("--duration", type=int, default=15, help="Duration in seconds (default: 15)")
    parser.add_argument("--model", default="standard", help="Model tier (default: standard)")
    parser.add_argument("--dry-run", action="store_true", help="Print command without executing")
    args = parser.parse_args()

    script = find_topview_script()
    if not script:
        print("ERROR: Topview skill video_gen.py not found.", file=sys.stderr)
        print("Set TOPVIEW_SKILL env var or install Topview skill.", file=sys.stderr)
        return 1

    for img in args.images:
        if not Path(img).exists():
            print(f"WARNING: Image not found: {img}", file=sys.stderr)

    images_json = json.dumps(args.images)

    cmd = [
        sys.executable, script,
        "--mode", "omni-reference",
        "--model", args.model,
        "--aspect", args.aspect,
        "--duration", str(args.duration),
        "--sound", "off",
        "--images", images_json,
        "--prompt", args.prompt,
        "--output", args.output,
    ]

    if args.dry_run:
        print("Dry-run command:")
        print(" ".join(cmd))
        return 0

    print(f"Running Topview Omni Reference:")
    print(f"  Script:   {script}")
    print(f"  Aspect:   {args.aspect}")
    print(f"  Duration: {args.duration}s")
    print(f"  Model:    {args.model}")
    print(f"  Images:   {len(args.images)} reference(s)")
    print(f"  Output:   {args.output}")
    print()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print(f"ERROR: Topview script exited with code {result.returncode}", file=sys.stderr)
        return result.returncode

    if Path(args.output).exists():
        size_mb = Path(args.output).stat().st_size / (1024 * 1024)
        print(f"\nSuccess: {args.output} ({size_mb:.1f} MB)")
    else:
        print("WARNING: Output file not found after execution. Check Topview logs.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
