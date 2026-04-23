"""Verify all external dependencies required by the video-use skill.

Checks: ffmpeg, ffprobe, yt-dlp, manim, ElevenLabs API key.
Reports each as PASS / FAIL / OPTIONAL with version info.

Usage:
    python helpers/healthcheck.py
    python helpers/healthcheck.py --strict   # exit 1 if any required dep missing
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _check_binary(name: str, version_flag: str = "--version") -> tuple[bool, str]:
    path = shutil.which(name)
    if not path:
        return False, "not found on PATH"
    try:
        proc = subprocess.run(
            [path, version_flag],
            capture_output=True, text=True, timeout=10,
        )
        first_line = (proc.stdout or proc.stderr).strip().split("\n")[0]
        return True, first_line[:120]
    except Exception as e:
        return True, f"found at {path} (version check failed: {e})"


def _check_python_package(name: str) -> tuple[bool, str]:
    try:
        mod = __import__(name)
        version = getattr(mod, "__version__", "unknown")
        return True, f"{name} {version}"
    except ImportError:
        return False, f"{name} not installed"


def _check_elevenlabs_key() -> tuple[bool, str]:
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    if key:
        return True, f"set ({len(key)} chars, starts with {key[:4]}...)"

    skill_root = Path(__file__).resolve().parent.parent
    search_paths = [
        skill_root / ".env",
        Path(".env"),
        Path.home() / ".env",
    ]
    for env_path in search_paths:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "ELEVENLABS_API_KEY":
                    val = v.strip().strip("'\"")
                    if val:
                        return True, f"found in {env_path}"

    return False, f"not set in env or .env (searched: {', '.join(str(p) for p in search_paths)})"


def main() -> None:
    ap = argparse.ArgumentParser(description="Video-use skill dependency health check")
    ap.add_argument("--strict", action="store_true", help="Exit 1 if any required check fails")
    args = ap.parse_args()

    checks: list[tuple[str, str, bool, str]] = []

    ok, info = _check_binary("ffmpeg")
    checks.append(("ffmpeg", "REQUIRED", ok, info))

    ok, info = _check_binary("ffprobe")
    checks.append(("ffprobe", "REQUIRED", ok, info))

    for pkg in ("requests", "PIL", "numpy"):
        pkg_import = "PIL" if pkg == "PIL" else pkg
        ok, info = _check_python_package(pkg_import)
        if pkg == "PIL":
            info = info.replace("PIL", "Pillow")
        checks.append((f"python:{pkg}", "REQUIRED", ok, info))

    ok, info = _check_elevenlabs_key()
    checks.append(("ELEVENLABS_API_KEY", "REQUIRED", ok, info))

    ok, info = _check_binary("yt-dlp")
    checks.append(("yt-dlp", "OPTIONAL", ok, info))

    ok, info = _check_binary("manim")
    checks.append(("manim", "OPTIONAL", ok, info))

    max_name = max(len(c[0]) for c in checks)
    required_failures = 0

    print("video-use skill health check")
    print("=" * 60)
    for name, level, ok, info in checks:
        status = "PASS" if ok else "FAIL"
        symbol = "\u2705" if ok else ("\u274c" if level == "REQUIRED" else "\u26a0\ufe0f")
        print(f"  {symbol} {name:<{max_name}}  [{level:>8}]  {status}  {info}")
        if not ok and level == "REQUIRED":
            required_failures += 1

    print("=" * 60)
    if required_failures:
        print(f"\n{required_failures} required dependency(ies) missing.")
        if args.strict:
            sys.exit(1)
    else:
        print("\nAll required dependencies OK.")


if __name__ == "__main__":
    main()
