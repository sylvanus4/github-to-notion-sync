#!/usr/bin/env python3
"""Split a 4x4 photo grid into four 2x2 quadrant images.

Usage:
    python split-grid.py --input images/memory_grid_4x4.png --output-dir images/

Output:
    images/memory_sheet_01.png  (top-left 2x2)
    images/memory_sheet_02.png  (top-right 2x2)
    images/memory_sheet_03.png  (bottom-left 2x2)
    images/memory_sheet_04.png  (bottom-right 2x2)
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    raise SystemExit(1)


def split_grid(input_path: str, output_dir: str) -> list[str]:
    img = Image.open(input_path)
    w, h = img.size

    mid_x = w // 2
    mid_y = h // 2

    quadrants = [
        ("memory_sheet_01.png", (0, 0, mid_x, mid_y)),
        ("memory_sheet_02.png", (mid_x, 0, w, mid_y)),
        ("memory_sheet_03.png", (0, mid_y, mid_x, h)),
        ("memory_sheet_04.png", (mid_x, mid_y, w, h)),
    ]

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    saved = []
    for name, box in quadrants:
        cropped = img.crop(box)
        dest = out / name
        cropped.save(str(dest))
        saved.append(str(dest))
        print(f"  Saved: {dest} ({cropped.size[0]}x{cropped.size[1]})")

    return saved


def main() -> int:
    parser = argparse.ArgumentParser(description="Split a 4x4 grid image into four 2x2 quadrants.")
    parser.add_argument("--input", required=True, help="Path to the 4x4 grid image")
    parser.add_argument("--output-dir", required=True, help="Directory for output 2x2 images")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        return 1

    print(f"Splitting {args.input} into 2x2 quadrants...")
    saved = split_grid(args.input, args.output_dir)
    print(f"\nDone. {len(saved)} quadrant images created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
