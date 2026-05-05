#!/usr/bin/env python3
"""Check required and optional dependencies for virtual-couple-travel-vlog."""

import argparse
import shutil
import subprocess
import sys


REQUIRED = {
    "python3": {
        "check": lambda: sys.version_info >= (3, 10),
        "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "hint": "Install Python 3.10+ from https://python.org",
    },
    "pillow": {
        "check": lambda: _try_import("PIL"),
        "hint": "pip install Pillow",
    },
    "ffmpeg": {
        "check": lambda: shutil.which("ffmpeg") is not None,
        "hint": "brew install ffmpeg  OR  apt install ffmpeg",
    },
    "ffprobe": {
        "check": lambda: shutil.which("ffprobe") is not None,
        "hint": "Included with ffmpeg installation",
    },
}

OPTIONAL = {
    "node": {
        "check": lambda: shutil.which("node") is not None,
        "hint": "brew install node  OR  https://nodejs.org",
    },
    "npm": {
        "check": lambda: shutil.which("npm") is not None,
        "hint": "Included with Node.js installation",
    },
    "npx": {
        "check": lambda: shutil.which("npx") is not None,
        "hint": "Included with Node.js installation",
    },
}


def _try_import(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def _get_version(cmd: str) -> str:
    try:
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip().split("\n")[0] if result.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check dependencies for virtual-couple-travel-vlog skill.")
    parser.add_argument("--show-install-hints", action="store_true", help="Show installation hints for missing tools")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    all_ok = True
    results = {"required": {}, "optional": {}}

    print("=== Required Dependencies ===\n")
    for name, info in REQUIRED.items():
        ok = info["check"]()
        status = "OK" if ok else "MISSING"
        version = info.get("version", _get_version(name) if ok and name not in ("pillow",) else "")
        print(f"  [{status}] {name}" + (f"  ({version})" if version else ""))
        if not ok:
            all_ok = False
            if args.show_install_hints:
                print(f"         Hint: {info['hint']}")
        results["required"][name] = {"ok": ok, "version": version}

    print("\n=== Optional Dependencies ===\n")
    for name, info in OPTIONAL.items():
        ok = info["check"]()
        status = "OK" if ok else "MISSING"
        version = _get_version(name) if ok else ""
        print(f"  [{status}] {name}" + (f"  ({version})" if version else ""))
        if not ok and args.show_install_hints:
            print(f"         Hint: {info['hint']}")
        results["optional"][name] = {"ok": ok, "version": version}

    if args.json:
        import json
        print(f"\n{json.dumps(results, indent=2)}")

    print()
    if all_ok:
        print("All required dependencies are available.")
        return 0
    else:
        print("Some required dependencies are missing. Fix them before running the skill.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
