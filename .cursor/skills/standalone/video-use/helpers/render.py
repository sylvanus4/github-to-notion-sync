"""Render a video from an EDL.

Implements the render pipeline in the correct order:

  1. Per-segment extract with color grade + 30ms audio fades baked in
  2. Lossless -c copy concat into base.mp4
  3. If overlays or subtitles: single filter graph that overlays animations
     (with PTS shift so frame 0 lands at the overlay window start)
     and applies `subtitles` filter LAST -> final.mp4

Optionally builds a master SRT from the per-source transcripts + EDL
output-timeline offsets.

Usage:
    python helpers/render.py <edl.json> -o final.mp4
    python helpers/render.py <edl.json> -o preview.mp4 --preview
    python helpers/render.py <edl.json> -o final.mp4 --build-subtitles
    python helpers/render.py <edl.json> -o final.mp4 --no-subtitles
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from grade import get_preset, auto_grade_for_clip
except ImportError:
    def get_preset(name: str) -> str:
        return ""

    def auto_grade_for_clip(video, start=0.0, duration=None, verbose=False):  # type: ignore
        return "eq=contrast=1.03:saturation=0.98", {}


SUB_FORCE_STYLE = (
    "FontName=Helvetica,FontSize=18,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,"
    "BorderStyle=1,Outline=2,Shadow=0,"
    "Alignment=2,MarginV=35"
)


def ffrun(cmd: list[str], label: str = "") -> None:
    """Run an FFmpeg command and surface stderr on failure."""
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        stderr_text = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
        tag = f" [{label}]" if label else ""
        tail = "\n".join(stderr_text.splitlines()[-30:]) if stderr_text else "(no stderr)"
        print(f"\nFFmpeg failed{tag} (exit {exc.returncode}):\n{tail}\n", file=sys.stderr)
        raise


def run(cmd: list[str], quiet: bool = False) -> None:
    if not quiet:
        print(f"  $ {' '.join(str(c) for c in cmd[:6])}{' ...' if len(cmd) > 6 else ''}")
    subprocess.run(cmd, check=True)


def resolve_grade_filter(grade_field: str | None) -> str:
    if not grade_field:
        return ""
    if grade_field == "auto":
        return "__AUTO__"
    if re.fullmatch(r"[a-zA-Z0-9_\-]+", grade_field):
        try:
            return get_preset(grade_field)
        except KeyError:
            print(f"warning: unknown preset '{grade_field}', using as raw filter")
            return grade_field
    return grade_field


def resolve_path(maybe_path: str, base: Path) -> Path:
    p = Path(maybe_path)
    if p.is_absolute():
        return p
    return (base / p).resolve()


def extract_segment(
    source: Path,
    seg_start: float,
    duration: float,
    grade_filter: str,
    out_path: Path,
    preview: bool = False,
    draft: bool = False,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if draft:
        scale = "scale=1280:-2"
    else:
        scale = "scale=1920:-2"

    vf_parts = [scale]
    if grade_filter:
        vf_parts.append(grade_filter)
    vf = ",".join(vf_parts)

    fade_out_start = max(0.0, duration - 0.03)
    af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={fade_out_start:.3f}:d=0.03"

    if draft:
        preset, crf = "ultrafast", "28"
    elif preview:
        preset, crf = "medium", "22"
    else:
        preset, crf = "fast", "20"

    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{seg_start:.3f}",
        "-i", str(source),
        "-t", f"{duration:.3f}",
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out_path),
    ]
    ffrun(cmd, label="extract-segment")


def extract_all_segments(
    edl: dict,
    edit_dir: Path,
    preview: bool,
    draft: bool = False,
) -> list[Path]:
    resolved = resolve_grade_filter(edl.get("grade"))
    is_auto = resolved == "__AUTO__"
    clips_dir = edit_dir / (
        "clips_draft" if draft else ("clips_preview" if preview else "clips_graded")
    )
    clips_dir.mkdir(parents=True, exist_ok=True)

    ranges = edl["ranges"]
    sources = edl["sources"]

    seg_paths: list[Path] = []
    print(f"extracting {len(ranges)} segment(s) \u2192 {clips_dir.name}/")
    if is_auto:
        print("  (auto-grade per segment: analyzing each range)")
    for i, r in enumerate(ranges):
        src_name = r["source"]
        src_path = resolve_path(sources[src_name], edit_dir)
        start = float(r["start"])
        end = float(r["end"])
        duration = end - start
        out_path = clips_dir / f"seg_{i:02d}_{src_name}.mp4"

        if is_auto:
            seg_filter, _stats = auto_grade_for_clip(src_path, start=start, duration=duration, verbose=False)
        else:
            seg_filter = resolved

        note = r.get("beat") or r.get("note") or ""
        print(f"  [{i:02d}] {src_name}  {start:7.2f}-{end:7.2f}  ({duration:5.2f}s)  {note}")
        if is_auto:
            print(f"        grade: {seg_filter or '(none)'}")
        extract_segment(src_path, start, duration, seg_filter, out_path, preview=preview, draft=draft)
        seg_paths.append(out_path)

    return seg_paths


def concat_segments(segment_paths: list[Path], out_path: Path, edit_dir: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    concat_list = edit_dir / "_concat.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n" for p in segment_paths))

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"concat \u2192 {out_path.name}")
    ffrun(cmd, label="concat")
    concat_list.unlink(missing_ok=True)


PUNCT_BREAK = set(".,!?;:")


def _srt_timestamp(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    h, rem = divmod(total_ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _words_in_range(transcript: dict, t_start: float, t_end: float) -> list[dict]:
    out: list[dict] = []
    for w in transcript.get("words", []):
        if w.get("type") != "word":
            continue
        ws = w.get("start")
        we = w.get("end")
        if ws is None or we is None:
            continue
        if we <= t_start or ws >= t_end:
            continue
        out.append(w)
    return out


def build_master_srt(edl: dict, edit_dir: Path, out_path: Path) -> None:
    transcripts_dir = edit_dir / "transcripts"
    sources = edl["sources"]

    entries: list[tuple[float, float, str]] = []
    seg_offset = 0.0

    for r in edl["ranges"]:
        src_name = r["source"]
        seg_start = float(r["start"])
        seg_end = float(r["end"])
        seg_duration = seg_end - seg_start

        tr_path = transcripts_dir / f"{src_name}.json"
        if not tr_path.exists():
            print(f"  no transcript for {src_name}, skipping captions for this segment")
            seg_offset += seg_duration
            continue

        transcript = json.loads(tr_path.read_text())
        words_in_seg = _words_in_range(transcript, seg_start, seg_end)

        chunks: list[list[dict]] = []
        current: list[dict] = []
        for w in words_in_seg:
            text = (w.get("text") or "").strip()
            if not text:
                continue
            current.append(w)
            ends_in_punct = bool(text) and text[-1] in PUNCT_BREAK
            if len(current) >= 2 or ends_in_punct:
                chunks.append(current)
                current = []
        if current:
            chunks.append(current)

        for chunk in chunks:
            local_start = max(seg_start, chunk[0].get("start", seg_start))
            local_end = min(seg_end, chunk[-1].get("end", seg_end))
            out_start = max(0.0, local_start - seg_start) + seg_offset
            out_end = max(0.0, local_end - seg_start) + seg_offset
            if out_end <= out_start:
                out_end = out_start + 0.4
            text = " ".join((w.get("text") or "").strip() for w in chunk)
            text = re.sub(r"\s+", " ", text).strip()
            text = text.rstrip(",;:")
            text = text.upper()
            entries.append((out_start, out_end, text))

        seg_offset += seg_duration

    entries.sort(key=lambda e: e[0])
    lines: list[str] = []
    for i, (a, b, t) in enumerate(entries, start=1):
        lines.append(str(i))
        lines.append(f"{_srt_timestamp(a)} --> {_srt_timestamp(b)}")
        lines.append(t)
        lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"master SRT \u2192 {out_path.name} ({len(entries)} cues)")


LOUDNORM_I = -14.0
LOUDNORM_TP = -1.0
LOUDNORM_LRA = 11.0


def measure_loudness(video_path: Path) -> dict[str, str] | None:
    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}:print_format=json"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(video_path),
        "-af", filter_str,
        "-vn", "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stderr = proc.stderr

    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(stderr[start : end + 1])
    except json.JSONDecodeError:
        return None
    needed = {"input_i", "input_tp", "input_lra", "input_thresh", "target_offset"}
    if not needed.issubset(data.keys()):
        return None
    return data


def apply_loudnorm_two_pass(
    input_path: Path,
    output_path: Path,
    preview: bool = False,
) -> bool:
    if preview:
        filter_str = f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-nostats",
            "-i", str(input_path),
            "-c:v", "copy",
            "-af", filter_str,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            str(output_path),
        ]
        print(f"  loudnorm (1-pass preview) \u2192 {output_path.name}")
        ffrun(cmd, label="loudnorm-1pass")
        return True

    print(f"  loudnorm pass 1: measuring {input_path.name}")
    measurement = measure_loudness(input_path)
    if measurement is None:
        print("  loudnorm measurement failed \u2014 falling back to 1-pass")
        return apply_loudnorm_two_pass(input_path, output_path, preview=True)

    print(f"    measured: I={measurement['input_i']} LUFS  "
          f"TP={measurement['input_tp']}  LRA={measurement['input_lra']}")

    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        f":measured_I={measurement['input_i']}"
        f":measured_TP={measurement['input_tp']}"
        f":measured_LRA={measurement['input_lra']}"
        f":measured_thresh={measurement['input_thresh']}"
        f":offset={measurement['target_offset']}"
        f":linear=true"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(input_path),
        "-c:v", "copy",
        "-af", filter_str,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(output_path),
    ]
    print(f"  loudnorm pass 2: normalizing \u2192 {output_path.name}")
    ffrun(cmd, label="loudnorm-2pass")
    return True


def build_final_composite(
    base_path: Path,
    overlays: list[dict],
    subtitles_path: Path | None,
    out_path: Path,
    edit_dir: Path,
    *,
    preview: bool = False,
    draft: bool = False,
) -> None:
    has_overlays = bool(overlays)
    has_subs = subtitles_path is not None and subtitles_path.exists()

    if not has_overlays and not has_subs:
        run(["ffmpeg", "-y", "-i", str(base_path), "-c", "copy", str(out_path)], quiet=True)
        return

    if draft:
        preset, crf = "ultrafast", "28"
    elif preview:
        preset, crf = "veryfast", "22"
    else:
        preset, crf = "fast", "18"

    inputs: list[str] = ["-i", str(base_path)]
    for ov in overlays:
        ov_path = resolve_path(ov["file"], edit_dir)
        inputs += ["-i", str(ov_path)]

    filter_parts: list[str] = []
    for idx, ov in enumerate(overlays, start=1):
        t = float(ov["start_in_output"])
        filter_parts.append(f"[{idx}:v]setpts=PTS-STARTPTS+{t}/TB[a{idx}]")

    current = "[0:v]"
    for idx, ov in enumerate(overlays, start=1):
        t = float(ov["start_in_output"])
        dur = float(ov["duration"])
        end = t + dur
        next_label = f"[v{idx}]"
        filter_parts.append(
            f"{current}[a{idx}]overlay=enable='between(t,{t:.3f},{end:.3f})'{next_label}"
        )
        current = next_label

    if has_subs:
        subs_abs = str(subtitles_path.resolve()).replace(":", r"\:").replace("'", r"\'")
        filter_parts.append(
            f"{current}subtitles='{subs_abs}':force_style='{SUB_FORCE_STYLE}'[outv]"
        )
        out_label = "[outv]"
    else:
        if has_overlays:
            filter_parts.append(f"{current}null[outv]")
            out_label = "[outv]"
        else:
            out_label = "[0:v]"

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", out_label,
        "-map", "0:a",
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print(f"compositing \u2192 {out_path.name}")
    mode_tag = " [preview]" if preview else (" [draft]" if draft else "")
    print(f"  overlays: {len(overlays)}, subtitles: {'yes' if has_subs else 'no'}{mode_tag}")
    ffrun(cmd, label="composite")


def validate_edl(edl: dict, edit_dir: Path) -> list[str]:
    """Validate EDL structure and return a list of error messages (empty = valid)."""
    errors: list[str] = []

    if "sources" not in edl or not isinstance(edl.get("sources"), dict):
        errors.append("EDL missing 'sources' dict")
    if "ranges" not in edl or not isinstance(edl.get("ranges"), list):
        errors.append("EDL missing 'ranges' list")

    if errors:
        return errors

    sources = edl["sources"]
    ranges = edl["ranges"]

    if not ranges:
        errors.append("EDL 'ranges' is empty — nothing to render")
        return errors

    for i, r in enumerate(ranges):
        if "source" not in r:
            errors.append(f"range[{i}]: missing 'source' field")
            continue
        src_name = r["source"]
        if src_name not in sources:
            errors.append(f"range[{i}]: source '{src_name}' not found in 'sources' dict")
            continue

        src_path = resolve_path(sources[src_name], edit_dir)
        if not src_path.exists():
            errors.append(f"range[{i}]: source file not found: {src_path}")

        start = r.get("start")
        end = r.get("end")
        if start is None or end is None:
            errors.append(f"range[{i}]: missing 'start' or 'end'")
            continue

        try:
            s, e = float(start), float(end)
        except (TypeError, ValueError):
            errors.append(f"range[{i}]: 'start'/'end' must be numeric (got {start!r}/{end!r})")
            continue

        if e <= s:
            errors.append(f"range[{i}]: end ({e}) <= start ({s}) — zero or negative duration")
        if s < 0:
            errors.append(f"range[{i}]: negative start ({s})")

    for ov in edl.get("overlays") or []:
        if "file" not in ov:
            errors.append(f"overlay missing 'file' field")
        if "start_in_output" not in ov or "duration" not in ov:
            errors.append(f"overlay missing 'start_in_output' or 'duration'")

    return errors


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a video from an EDL")
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument("-o", "--output", type=Path, required=True, help="Output video path")
    ap.add_argument("--preview", action="store_true", help="Preview mode: 1080p, medium, CRF 22")
    ap.add_argument("--draft", action="store_true", help="Draft mode: 720p, ultrafast, CRF 28")
    ap.add_argument("--build-subtitles", action="store_true", help="Build master.srt from transcripts + EDL offsets")
    ap.add_argument("--no-subtitles", action="store_true", help="Skip subtitles even if the EDL references one")
    ap.add_argument("--no-loudnorm", action="store_true", help="Skip audio loudness normalization")
    ap.add_argument("--dry-run", action="store_true", help="Validate EDL without rendering; print segment plan and exit")
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"edl not found: {edl_path}")

    try:
        edl = json.loads(edl_path.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"invalid JSON in {edl_path}: {e}")

    edit_dir = edl_path.parent
    out_path = args.output.resolve()

    validation_errors = validate_edl(edl, edit_dir)
    if validation_errors:
        print("EDL validation failed:", file=sys.stderr)
        for err in validation_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        ranges = edl["ranges"]
        sources = edl["sources"]
        total_dur = 0.0
        print(f"dry-run: {len(ranges)} segment(s)")
        for i, r in enumerate(ranges):
            src_name = r["source"]
            s, e = float(r["start"]), float(r["end"])
            dur = e - s
            total_dur += dur
            note = r.get("beat") or r.get("note") or ""
            print(f"  [{i:02d}] {src_name}  {s:7.2f}-{e:7.2f}  ({dur:5.2f}s)  {note}")
        print(f"\ntotal estimated duration: {total_dur:.2f}s")
        grade_mode = edl.get("grade") or "(none)"
        overlays = edl.get("overlays") or []
        subs = edl.get("subtitles") or "(none)"
        print(f"grade: {grade_mode}  |  overlays: {len(overlays)}  |  subtitles: {subs}")
        print("\nEDL is valid. Use without --dry-run to render.")
        return

    segment_paths = extract_all_segments(
        edl, edit_dir, preview=args.preview, draft=args.draft
    )

    if not segment_paths:
        sys.exit("no segments were extracted — check EDL ranges and source files")

    if args.draft:
        base_name = "base_draft.mp4"
    elif args.preview:
        base_name = "base_preview.mp4"
    else:
        base_name = "base.mp4"
    base_path = edit_dir / base_name
    concat_segments(segment_paths, base_path, edit_dir)

    subs_path: Path | None = None
    if not args.no_subtitles:
        if args.build_subtitles:
            subs_path = edit_dir / "master.srt"
            build_master_srt(edl, edit_dir, subs_path)
        elif edl.get("subtitles"):
            subs_path = resolve_path(edl["subtitles"], edit_dir)
            if not subs_path.exists():
                print(f"warning: subtitles path in EDL does not exist: {subs_path}")
                subs_path = None

    overlays = edl.get("overlays") or []
    if args.no_loudnorm:
        build_final_composite(
            base_path, overlays, subs_path, out_path, edit_dir,
            preview=args.preview, draft=args.draft,
        )
    else:
        tmp_composite = out_path.with_suffix(".prenorm.mp4")
        build_final_composite(
            base_path, overlays, subs_path, tmp_composite, edit_dir,
            preview=args.preview, draft=args.draft,
        )
        print("loudness normalization \u2192 social-ready (-14 LUFS / -1 dBTP / LRA 11)")
        apply_loudnorm_two_pass(tmp_composite, out_path, preview=(args.preview or args.draft))
        tmp_composite.unlink(missing_ok=True)

    if not out_path.exists() or out_path.stat().st_size == 0:
        sys.exit(f"render failed: output file missing or empty — {out_path}")

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"\ndone: {out_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
