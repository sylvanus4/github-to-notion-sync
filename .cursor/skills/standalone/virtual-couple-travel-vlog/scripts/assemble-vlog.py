#!/usr/bin/env python3
"""Assemble video clips into a final vlog using FFmpeg.

Usage:
    python assemble-vlog.py --clips-dir videos/ --output videos/final_vlog.mp4 [--music audio/bgm.mp3]

Concatenates clip_01.mp4 through clip_04.mp4 in order. Optionally mixes in a
background music track. Falls back to re-encoding if direct stream copy fails
due to codec mismatches.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def find_clips(clips_dir: str) -> list[Path]:
    d = Path(clips_dir)
    clips = sorted(d.glob("clip_*.mp4"))
    if not clips:
        clips = sorted(d.glob("*.mp4"))
        clips = [c for c in clips if "final" not in c.name]
    return clips


def build_concat_file(clips: list[Path], tmp_dir: str) -> str:
    concat_path = Path(tmp_dir) / "concat_list.txt"
    with open(concat_path, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.resolve()}'\n")
    return str(concat_path)


def try_stream_copy(concat_file: str, output: str) -> bool:
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        output,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and Path(output).exists():
        return True
    Path(output).unlink(missing_ok=True)
    return False


def re_encode(concat_file: str, output: str) -> bool:
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        output,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def add_music(video: str, music: str, output: str) -> bool:
    cmd = [
        "ffmpeg", "-y",
        "-i", video,
        "-i", music,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest",
        output,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble video clips into final vlog.")
    parser.add_argument("--clips-dir", required=True, help="Directory containing clip_XX.mp4 files")
    parser.add_argument("--output", required=True, help="Output file path for final vlog")
    parser.add_argument("--music", default=None, help="Optional background music file path")
    args = parser.parse_args()

    clips = find_clips(args.clips_dir)
    if not clips:
        print(f"ERROR: No video clips found in {args.clips_dir}", file=sys.stderr)
        return 1

    print(f"Found {len(clips)} clips to assemble:")
    for c in clips:
        print(f"  - {c.name}")

    with tempfile.TemporaryDirectory() as tmp_dir:
        concat_file = build_concat_file(clips, tmp_dir)

        video_output = args.output if not args.music else str(Path(tmp_dir) / "no_music.mp4")

        print("\nAttempting stream copy concatenation...")
        if try_stream_copy(concat_file, video_output):
            print("  Stream copy succeeded.")
        else:
            print("  Stream copy failed (codec mismatch). Re-encoding...")
            if not re_encode(concat_file, video_output):
                print("ERROR: Re-encoding failed.", file=sys.stderr)
                return 1
            print("  Re-encoding succeeded.")

        if args.music:
            if not Path(args.music).exists():
                print(f"WARNING: Music file not found: {args.music}. Skipping music mux.")
                Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                Path(video_output).rename(args.output)
            else:
                print(f"\nMixing music: {args.music}")
                Path(args.output).parent.mkdir(parents=True, exist_ok=True)
                if add_music(video_output, args.music, args.output):
                    print("  Music mux succeeded.")
                else:
                    print("  Music mux failed. Using video without music.")
                    Path(video_output).rename(args.output)

    print(f"\nFinal vlog: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
