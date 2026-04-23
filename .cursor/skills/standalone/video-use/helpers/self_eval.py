"""Post-render quality evaluation for video-use skill.

Runs ffprobe on the rendered output to verify:
  - Container format and codecs
  - Duration matches EDL expected total
  - Audio loudness (LUFS)
  - Resolution and framerate

Usage:
    python helpers/self_eval.py <rendered.mp4> --edl <edl.json>
    python helpers/self_eval.py <rendered.mp4>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe_file(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr[:300]}")
    return json.loads(result.stdout)


def measure_loudness(path: Path) -> dict | None:
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(path),
        "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
        "-vn", "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stderr = proc.stderr
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(stderr[start:end + 1])
    except json.JSONDecodeError:
        return None


def edl_expected_duration(edl_path: Path) -> float:
    edl = json.loads(edl_path.read_text())
    total = 0.0
    for r in edl.get("ranges", []):
        total += float(r["end"]) - float(r["start"])
    return total


def main() -> None:
    ap = argparse.ArgumentParser(description="Post-render quality evaluation")
    ap.add_argument("video", type=Path, help="Rendered video file")
    ap.add_argument("--edl", type=Path, default=None, help="EDL JSON for duration comparison")
    ap.add_argument("--json", action="store_true", help="Output results as JSON")
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"file not found: {video}")

    if video.stat().st_size == 0:
        sys.exit(f"file is empty (0 bytes): {video}")

    results: dict = {"file": str(video), "checks": [], "pass": True}

    try:
        probe = probe_file(video)
    except RuntimeError as e:
        sys.exit(str(e))

    fmt = probe.get("format", {})
    try:
        actual_duration = float(fmt.get("duration", 0))
    except (ValueError, TypeError):
        actual_duration = 0.0
    try:
        file_size_mb = int(fmt.get("size", 0)) / (1024 * 1024)
    except (ValueError, TypeError):
        file_size_mb = video.stat().st_size / (1024 * 1024)

    if actual_duration <= 0:
        results["checks"].append({
            "name": "duration_positive",
            "pass": False,
            "detail": f"duration is {actual_duration}s — file may be corrupt",
        })
        results["pass"] = False

    results["duration_s"] = round(actual_duration, 2)
    results["size_mb"] = round(file_size_mb, 1)

    video_stream = None
    audio_stream = None
    for s in probe.get("streams", []):
        if s.get("codec_type") == "video" and video_stream is None:
            video_stream = s
        elif s.get("codec_type") == "audio" and audio_stream is None:
            audio_stream = s

    if video_stream:
        w = video_stream.get("width", 0)
        h = video_stream.get("height", 0)
        codec = video_stream.get("codec_name", "?")
        fps_raw = video_stream.get("r_frame_rate", "0/1")
        try:
            num, den = fps_raw.split("/")
            fps = round(int(num) / int(den), 1) if int(den) > 0 else 0
        except (ValueError, ZeroDivisionError):
            fps = 0
        results["video"] = {"codec": codec, "resolution": f"{w}x{h}", "fps": fps}
        results["checks"].append({
            "name": "video_stream",
            "pass": w > 0 and h > 0,
            "detail": f"{codec} {w}x{h} @ {fps}fps",
        })
    else:
        results["checks"].append({"name": "video_stream", "pass": False, "detail": "no video stream"})
        results["pass"] = False

    if audio_stream:
        a_codec = audio_stream.get("codec_name", "?")
        sample_rate = audio_stream.get("sample_rate", "?")
        results["audio"] = {"codec": a_codec, "sample_rate": sample_rate}
        results["checks"].append({
            "name": "audio_stream",
            "pass": True,
            "detail": f"{a_codec} @ {sample_rate}Hz",
        })
    else:
        results["checks"].append({"name": "audio_stream", "pass": False, "detail": "no audio stream"})
        results["pass"] = False

    if args.edl and args.edl.exists():
        expected = edl_expected_duration(args.edl)
        drift = abs(actual_duration - expected)
        drift_ok = drift < 1.0
        results["checks"].append({
            "name": "duration_match",
            "pass": drift_ok,
            "detail": f"expected {expected:.2f}s, got {actual_duration:.2f}s (drift {drift:.2f}s)",
        })
        if not drift_ok:
            results["pass"] = False

    loudness = measure_loudness(video)
    if loudness:
        input_i = float(loudness.get("input_i", -99))
        input_tp = float(loudness.get("input_tp", -99))
        lufs_ok = -16 <= input_i <= -12
        tp_ok = input_tp <= 0
        results["loudness"] = {"integrated_lufs": input_i, "true_peak_dbtp": input_tp}
        results["checks"].append({
            "name": "loudness_integrated",
            "pass": lufs_ok,
            "detail": f"{input_i:.1f} LUFS (target: -14 \u00b1 2)",
        })
        results["checks"].append({
            "name": "loudness_true_peak",
            "pass": tp_ok,
            "detail": f"{input_tp:.1f} dBTP (max: 0)",
        })
        if not lufs_ok or not tp_ok:
            results["pass"] = False
    else:
        results["checks"].append({
            "name": "loudness",
            "pass": False,
            "detail": "measurement failed",
        })

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        banner = "PASS" if results["pass"] else "FAIL"
        print(f"\nself-eval: {banner}")
        print(f"  file:     {video.name}")
        print(f"  duration: {actual_duration:.2f}s")
        print(f"  size:     {file_size_mb:.1f} MB")
        print()
        for c in results["checks"]:
            icon = "\u2705" if c["pass"] else "\u274c"
            print(f"  {icon} {c['name']}: {c['detail']}")
        print()


if __name__ == "__main__":
    main()
