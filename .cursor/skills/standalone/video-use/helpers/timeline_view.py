"""Filmstrip + waveform composite PNG for a time range of a video.

The only visual drill-down tool. Given a video and a [start, end] range,
extracts N evenly spaced frames via ffmpeg, composites them into a
horizontal filmstrip, and renders a waveform ribbon below with word
labels overlaid from the transcript (if available) and silence gaps
shaded.

Use this at decision points -- ambiguous pauses, retake disambiguation,
cut-point sanity checks. Do NOT call it in a scan loop over every
utterance; it's an on-demand drill-down, not a background index.

Usage:
    python helpers/timeline_view.py <video> <start> <end>
    python helpers/timeline_view.py <video> <start> <end> -o out.png
    python helpers/timeline_view.py <video> <start> <end> --n-frames 12
    python helpers/timeline_view.py <video> <start> <end> --transcript <path>
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def extract_frames(video: Path, start: float, end: float, n: int, dest_dir: Path) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    if n < 1:
        n = 1
    if n == 1:
        times = [(start + end) / 2.0]
    else:
        step = (end - start) / (n - 1)
        times = [start + i * step for i in range(n)]

    paths: list[Path] = []
    for i, t in enumerate(times):
        seek = min(t, max(end - 0.05, start))
        out = dest_dir / f"f_{i:03d}.jpg"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{seek:.3f}",
            "-i", str(video),
            "-frames:v", "1",
            "-q:v", "4",
            "-vf", "scale=320:-2",
            str(out),
        ]
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r.returncode != 0 and not out.exists():
            continue
        paths.append(out)
    return paths


def compute_envelope(video: Path, start: float, end: float, samples: int = 2000) -> np.ndarray:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav = Path(f.name)
    try:
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{start:.3f}",
            "-i", str(video),
            "-t", f"{(end - start):.3f}",
            "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
            str(wav),
        ]
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r.returncode != 0 or not wav.exists() or wav.stat().st_size == 0:
            return np.zeros(samples)

        with wave.open(str(wav), "rb") as w:
            frames = w.readframes(w.getnframes())
        pcm = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        if pcm.size == 0:
            return np.zeros(samples)

        n = pcm.size
        window = max(1, n // samples)
        usable = (n // window) * window
        reshaped = pcm[:usable].reshape(-1, window)
        env = np.sqrt(np.mean(reshaped ** 2, axis=1))
        if env.size < samples:
            env = np.pad(env, (0, samples - env.size))
        elif env.size > samples:
            env = env[:samples]
        if env.max() > 0:
            env = env / env.max()
        return env
    finally:
        wav.unlink(missing_ok=True)


def words_in_range(transcript_path: Path, start: float, end: float) -> list[dict]:
    if not transcript_path.exists():
        return []
    data = json.loads(transcript_path.read_text())
    out: list[dict] = []
    for w in data.get("words", []):
        ws = w.get("start")
        we = w.get("end")
        if ws is None or we is None:
            continue
        if we <= start or ws >= end:
            continue
        out.append(w)
    return out


def find_silences(words: list[dict], start: float, end: float, threshold: float = 0.4) -> list[tuple[float, float]]:
    gaps: list[tuple[float, float]] = []
    prev_end = start
    for w in words:
        if w.get("type") == "spacing":
            continue
        ws = max(start, w.get("start", start))
        if ws - prev_end >= threshold:
            gaps.append((prev_end, ws))
        prev_end = max(prev_end, w.get("end", ws))
    if end - prev_end >= threshold:
        gaps.append((prev_end, end))
    return gaps


FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]


def load_font(size: int) -> ImageFont.ImageFont:
    for fp in FONT_CANDIDATES:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


BG = (18, 18, 22)
FG = (235, 235, 235)
DIM = (110, 110, 120)
ACCENT = (255, 140, 60)
SILENCE = (50, 80, 120, 120)
WAVE = (140, 180, 255)


def render_timeline(
    video: Path,
    start: float,
    end: float,
    out_path: Path,
    n_frames: int,
    transcript: Path | None,
) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        print(f"extracting {n_frames} frames from {start:.2f}s to {end:.2f}s")
        frame_paths = extract_frames(video, start, end, n_frames, tmp_dir)

        canvas_width = 1920
        frame_h = 180
        filmstrip_y = 50
        filmstrip_h = frame_h
        wave_y = filmstrip_y + filmstrip_h + 20
        wave_h = 220
        label_y = wave_y + wave_h + 10
        canvas_height = label_y + 60

        imgs: list[Image.Image] = []
        for fp in frame_paths:
            img = Image.open(fp).convert("RGB")
            aspect = img.width / img.height
            new_w = int(frame_h * aspect)
            imgs.append(img.resize((new_w, frame_h), Image.LANCZOS))

        total_frame_w = sum(img.width for img in imgs) + (len(imgs) - 1) * 4
        content_w = max(1400, total_frame_w)
        canvas_width = max(canvas_width, content_w + 100)

        canvas = Image.new("RGB", (canvas_width, canvas_height), BG)
        draw = ImageDraw.Draw(canvas, "RGBA")

        header_font = load_font(22)
        label_font = load_font(14)
        small_font = load_font(12)

        draw.text(
            (50, 12),
            f"{video.name}   {start:.2f}s \u2192 {end:.2f}s   ({(end - start):.2f}s, {n_frames} frames)",
            fill=FG,
            font=header_font,
        )

        strip_width = canvas_width - 100
        if total_frame_w <= strip_width:
            cursor = 50
            for img in imgs:
                canvas.paste(img, (cursor, filmstrip_y))
                cursor += img.width + 4
            draw_width = cursor - 50
        else:
            scale = strip_width / total_frame_w
            new_h = int(frame_h * scale)
            cursor = 50
            for img in imgs:
                new_w = int(img.width * scale)
                scaled = img.resize((new_w, new_h), Image.LANCZOS)
                canvas.paste(scaled, (cursor, filmstrip_y + (filmstrip_h - new_h) // 2))
                cursor += new_w + max(2, int(4 * scale))
            draw_width = cursor - 50

        strip_x0 = 50
        strip_x1 = 50 + draw_width
        strip_span = strip_x1 - strip_x0

        def time_to_x(t: float) -> int:
            frac = (t - start) / max(1e-6, (end - start))
            return int(strip_x0 + frac * strip_span)

        draw.rectangle((strip_x0, wave_y, strip_x1, wave_y + wave_h), fill=(28, 28, 34))

        words = words_in_range(transcript, start, end) if transcript else []
        silences = find_silences(words, start, end, threshold=0.4) if words else []
        for a, b in silences:
            xa = time_to_x(a)
            xb = time_to_x(b)
            draw.rectangle((xa, wave_y, xb, wave_y + wave_h), fill=SILENCE)

        env = compute_envelope(video, start, end, samples=max(strip_span, 200))
        mid_y = wave_y + wave_h // 2
        max_amp = wave_h // 2 - 8
        points_top: list[tuple[int, int]] = []
        points_bot: list[tuple[int, int]] = []
        for i, v in enumerate(env):
            xi = strip_x0 + int(i * strip_span / max(1, len(env) - 1))
            a = int(v * max_amp)
            points_top.append((xi, mid_y - a))
            points_bot.append((xi, mid_y + a))
        if points_top:
            draw.line(points_top, fill=WAVE, width=1, joint="curve")
            draw.line(points_bot, fill=WAVE, width=1, joint="curve")
            poly = points_top + list(reversed(points_bot))
            draw.polygon(poly, fill=(*WAVE, 60))

        last_label_x = -9999
        for w in words:
            if w.get("type") != "word":
                continue
            ws = w.get("start")
            we = w.get("end")
            text = (w.get("text") or "").strip()
            if not text or ws is None or we is None:
                continue
            if (we - ws) < 0.05:
                continue
            cx = (time_to_x(ws) + time_to_x(we)) // 2
            if cx - last_label_x < 28:
                continue
            draw.line((cx, wave_y - 4, cx, wave_y), fill=DIM, width=1)
            draw.text((cx + 2, wave_y - 18), text, fill=FG, font=small_font)
            last_label_x = cx

        ruler_y = wave_y + wave_h + 2
        n_ticks = 6
        for i in range(n_ticks + 1):
            frac = i / n_ticks
            t = start + frac * (end - start)
            xi = strip_x0 + int(frac * strip_span)
            draw.line((xi, ruler_y, xi, ruler_y + 6), fill=DIM, width=1)
            draw.text((xi - 20, ruler_y + 8), f"{t:.2f}s", fill=DIM, font=label_font)

        if silences:
            txt = f"shaded bands = silences \u2265 400ms ({len(silences)} gap(s))"
            draw.text((strip_x0, label_y + 30), txt, fill=DIM, font=label_font)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(out_path, "PNG", optimize=True)
        print(f"saved: {out_path}  ({out_path.stat().st_size // 1024} KB)")


def _resolve_edl_path(raw: str, edit_dir: Path) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    return (edit_dir / p).resolve()


def render_edl_timeline(
    edl_path: Path,
    out_path: Path | None,
    n_frames_per_seg: int,
) -> None:
    """Generate a multi-segment composite from an EDL JSON.

    Each range in the EDL gets its own filmstrip row with waveform,
    stacked vertically with segment labels and boundary markers.
    """
    edl_path = edl_path.resolve()
    if not edl_path.exists():
        sys.exit(f"EDL not found: {edl_path}")

    try:
        edl = json.loads(edl_path.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"invalid JSON in {edl_path}: {e}")

    sources = edl.get("sources", {})
    ranges = edl.get("ranges", [])
    if not ranges:
        sys.exit("EDL has no ranges to visualize")

    edit_dir = edl_path.parent
    transcripts_dir = edit_dir / "transcripts"

    header_font = load_font(22)
    label_font = load_font(16)
    small_font = load_font(12)

    canvas_width = 1920
    seg_strip_h = 120
    seg_wave_h = 140
    seg_label_h = 34
    seg_gap = 16
    row_h = seg_label_h + seg_strip_h + 8 + seg_wave_h + seg_gap

    top_margin = 60
    bottom_margin = 40
    canvas_height = top_margin + len(ranges) * row_h + bottom_margin

    canvas = Image.new("RGB", (canvas_width, canvas_height), BG)
    draw = ImageDraw.Draw(canvas, "RGBA")

    total_dur = sum(float(r["end"]) - float(r["start"]) for r in ranges)
    draw.text(
        (50, 16),
        f"EDL Timeline: {len(ranges)} segments, {total_dur:.1f}s total",
        fill=FG,
        font=header_font,
    )

    SEG_COLORS = [
        (80, 140, 220),
        (220, 140, 80),
        (80, 200, 120),
        (200, 80, 140),
        (140, 100, 220),
        (220, 200, 80),
    ]

    strip_x0 = 50
    strip_x1 = canvas_width - 50
    strip_span = strip_x1 - strip_x0

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        for idx, r in enumerate(ranges):
            row_y = top_margin + idx * row_h
            src_name = r.get("source", "?")
            seg_start = float(r.get("start", 0))
            seg_end = float(r.get("end", 0))
            duration = seg_end - seg_start
            note = r.get("beat") or r.get("note") or ""
            color = SEG_COLORS[idx % len(SEG_COLORS)]

            draw.rectangle((strip_x0 - 6, row_y, strip_x0 - 2, row_y + seg_label_h), fill=color)
            label_text = (
                f"[{idx:02d}] {src_name}  "
                f"{seg_start:.2f}s \u2192 {seg_end:.2f}s  ({duration:.2f}s)"
            )
            if note:
                label_text += f"  \u2014 {note}"
            draw.text((strip_x0 + 4, row_y + 6), label_text, fill=FG, font=label_font)

            filmstrip_y = row_y + seg_label_h
            wave_y = filmstrip_y + seg_strip_h + 8

            src_path_raw = sources.get(src_name)
            if not src_path_raw:
                draw.text((strip_x0, filmstrip_y + 20), f"source '{src_name}' not in EDL sources", fill=ACCENT, font=label_font)
                continue
            src_path = _resolve_edl_path(src_path_raw, edit_dir)
            if not src_path.exists():
                draw.text((strip_x0, filmstrip_y + 20), f"file not found: {src_path.name}", fill=ACCENT, font=label_font)
                continue

            seg_frames_dir = tmp_dir / f"seg_{idx}"
            frame_paths = extract_frames(src_path, seg_start, seg_end, n_frames_per_seg, seg_frames_dir)

            imgs: list[Image.Image] = []
            for fp in frame_paths:
                img = Image.open(fp).convert("RGB")
                aspect = img.width / img.height
                new_w = int(seg_strip_h * aspect)
                imgs.append(img.resize((new_w, seg_strip_h), Image.LANCZOS))

            if imgs:
                total_frame_w = sum(img.width for img in imgs) + (len(imgs) - 1) * 3
                if total_frame_w <= strip_span:
                    cursor = strip_x0
                    for img in imgs:
                        canvas.paste(img, (cursor, filmstrip_y))
                        cursor += img.width + 3
                else:
                    scale = strip_span / total_frame_w
                    new_h = int(seg_strip_h * scale)
                    cursor = strip_x0
                    for img in imgs:
                        new_w = int(img.width * scale)
                        scaled = img.resize((new_w, new_h), Image.LANCZOS)
                        canvas.paste(scaled, (cursor, filmstrip_y + (seg_strip_h - new_h) // 2))
                        cursor += new_w + max(1, int(3 * scale))

            draw.rectangle((strip_x0, wave_y, strip_x1, wave_y + seg_wave_h), fill=(28, 28, 34))

            tr_path = transcripts_dir / f"{src_name}.json"
            words: list[dict] = []
            if tr_path.exists():
                words = words_in_range(tr_path, seg_start, seg_end)
            silences = find_silences(words, seg_start, seg_end) if words else []

            def time_to_x(t: float, _start: float = seg_start, _dur: float = duration) -> int:
                frac = (t - _start) / max(1e-6, _dur)
                return int(strip_x0 + frac * strip_span)

            for a, b in silences:
                xa, xb = time_to_x(a), time_to_x(b)
                draw.rectangle((xa, wave_y, xb, wave_y + seg_wave_h), fill=SILENCE)

            env = compute_envelope(src_path, seg_start, seg_end, samples=max(strip_span, 200))
            mid_y = wave_y + seg_wave_h // 2
            max_amp = seg_wave_h // 2 - 6
            pts_top: list[tuple[int, int]] = []
            pts_bot: list[tuple[int, int]] = []
            for i, v in enumerate(env):
                xi = strip_x0 + int(i * strip_span / max(1, len(env) - 1))
                a = int(v * max_amp)
                pts_top.append((xi, mid_y - a))
                pts_bot.append((xi, mid_y + a))
            if pts_top:
                wave_color = color
                draw.line(pts_top, fill=wave_color, width=1, joint="curve")
                draw.line(pts_bot, fill=wave_color, width=1, joint="curve")
                poly = pts_top + list(reversed(pts_bot))
                draw.polygon(poly, fill=(*wave_color, 50))

            n_ticks = 4
            for ti in range(n_ticks + 1):
                frac = ti / n_ticks
                t = seg_start + frac * duration
                xi = strip_x0 + int(frac * strip_span)
                tick_y = wave_y + seg_wave_h
                draw.line((xi, tick_y, xi, tick_y + 4), fill=DIM, width=1)
                draw.text((xi - 16, tick_y + 5), f"{t:.1f}s", fill=DIM, font=small_font)

    if out_path is None:
        out_dir = edit_dir / "verify"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"edl_timeline_{edl_path.stem}.png"

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "PNG", optimize=True)
    print(f"EDL timeline saved: {out_path}  ({out_path.stat().st_size // 1024} KB)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Filmstrip + waveform composite for a video range")
    ap.add_argument("video", type=Path, nargs="?", help="Source video")
    ap.add_argument("start", type=float, nargs="?", help="Start time in seconds")
    ap.add_argument("end", type=float, nargs="?", help="End time in seconds")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Output PNG path")
    ap.add_argument("--n-frames", type=int, default=10, help="Number of frames (default 10)")
    ap.add_argument(
        "--transcript",
        type=Path,
        default=None,
        help="Path to transcript.json for word labels + silence shading",
    )
    ap.add_argument(
        "--edl", type=Path, default=None,
        help="EDL JSON file. Generates a multi-segment composite with per-segment filmstrips.",
    )
    args = ap.parse_args()

    if args.edl:
        render_edl_timeline(args.edl, args.output, args.n_frames)
        return

    if not args.video or args.start is None or args.end is None:
        ap.error("video, start, and end are required (or use --edl <file>)")

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"video not found: {video}")

    if args.end <= args.start:
        sys.exit("end must be > start")

    transcript = args.transcript
    if transcript is None:
        auto = video.parent / "edit" / "transcripts" / f"{video.stem}.json"
        if auto.exists():
            transcript = auto

    out_path = args.output
    if out_path is None:
        out_dir = video.parent / "edit" / "verify"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{video.stem}_{args.start:.2f}-{args.end:.2f}.png"

    render_timeline(
        video=video,
        start=args.start,
        end=args.end,
        out_path=out_path,
        n_frames=args.n_frames,
        transcript=transcript,
    )


if __name__ == "__main__":
    main()
