#!/usr/bin/env python3
"""
Virtual Couple Travel Vlog Generator v2.0
End-to-end pipeline: DALL-E 3 image generation → FFmpeg Ken Burns → Assembly with BGM.
Usage: python3 generate_vlog.py --destination "Tokyo" [--scenes 5] [--output-dir ./output]
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

try:
    import openai
except ImportError:
    sys.exit("ERROR: 'openai' package not installed. Run: pip install openai")

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: 'Pillow' package not installed. Run: pip install Pillow")


def check_prerequisites():
    """Verify ffmpeg and API key are available."""
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit("ERROR: ffmpeg not found. Install with: brew install ffmpeg")

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("ERROR: OPENAI_API_KEY not set. Export from .env or set directly.")

    print("[OK] Prerequisites verified: openai, Pillow, ffmpeg, OPENAI_API_KEY")


def generate_character_grid(client, boy_desc, girl_desc, output_dir):
    """Generate 2x2 character identity grid."""
    grid_path = output_dir / "character_grid.png"
    if grid_path.exists():
        print(f"[SKIP] Character grid already exists: {grid_path}")
        return grid_path

    prompt = (
        f"A 2x2 grid of 4 different poses of the same cute anime couple (boy and girl) "
        f"in casual travel outfits. Top-left: front view standing together smiling. "
        f"Top-right: side view walking hand in hand. Bottom-left: back view looking at scenery. "
        f"Bottom-right: sitting together at a cafe. Consistent character design: {boy_desc}, "
        f"{girl_desc}. Bright warm colors, illustration style. "
        f"White background separating each quadrant clearly."
    )

    print("[Step 2] Generating character grid via DALL-E 3...")
    response = client.images.generate(
        model="dall-e-3", prompt=prompt, size="1024x1024", quality="hd", n=1
    )
    url = response.data[0].url
    urllib.request.urlretrieve(url, str(grid_path))
    print(f"  Saved: {grid_path} ({grid_path.stat().st_size} bytes)")
    return grid_path


def split_grid(grid_path, output_dir):
    """Split 2x2 grid into 4 individual character poses."""
    chars_dir = output_dir / "characters"
    chars_dir.mkdir(parents=True, exist_ok=True)

    poses = ["front", "side", "back", "cafe"]
    first_pose = chars_dir / f"{poses[0]}.png"
    if first_pose.exists():
        print(f"[SKIP] Character poses already split in: {chars_dir}")
        return chars_dir

    print("[Step 2b] Splitting grid into 4 poses...")
    grid = Image.open(grid_path)
    w, h = grid.size
    hw, hh = w // 2, h // 2
    coords = [(0, 0, hw, hh), (hw, 0, w, hh), (0, hh, hw, h), (hw, hh, w, h)]

    for name, box in zip(poses, coords):
        crop = grid.crop(box)
        path = chars_dir / f"{name}.png"
        crop.save(path)
        print(f"  Saved: {path} ({crop.size[0]}x{crop.size[1]})")

    return chars_dir


def generate_scene_images(client, scenes, boy_desc, girl_desc, output_dir):
    """Generate landscape scene images."""
    scenes_dir = output_dir / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for i, scene in enumerate(scenes, 1):
        fname = f"scene_{i:02d}_{scene['slug']}.png"
        path = scenes_dir / fname
        if path.exists():
            print(f"[SKIP] Scene {i} already exists: {path}")
            generated.append(path)
            continue

        prompt = (
            f"A cute anime couple ({boy_desc}; {girl_desc}) "
            f"{scene['action']} in {scene['location']}. "
            f"{scene['mood']}. Illustration style, 16:9 cinematic composition."
        )

        print(f"[Step 3] Generating scene {i}/{len(scenes)}: {scene['slug']}...")
        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size="1792x1024", quality="hd", n=1
        )
        url = response.data[0].url
        urllib.request.urlretrieve(url, str(path))
        print(f"  Saved: {path} ({path.stat().st_size} bytes)")
        generated.append(path)
        time.sleep(1)

    return generated


def create_ken_burns_clips(scene_paths, output_dir, duration=5):
    """Convert scene images to video clips with Ken Burns effect."""
    clips_dir = output_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    clips = []
    frames = duration * 30

    for i, scene_path in enumerate(scene_paths, 1):
        clip_path = clips_dir / f"clip_{i:02d}.mp4"
        if clip_path.exists():
            print(f"[SKIP] Clip {i} already exists: {clip_path}")
            clips.append(clip_path)
            continue

        print(f"[Step 4] Creating Ken Burns clip {i}/{len(scene_paths)}...")
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(scene_path),
            "-vf", (
                f"zoompan=z='min(zoom+0.0015,1.5)':"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d={frames}:s=1920x1080:fps=30"
            ),
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(clip_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr[:200]}")
            continue
        clips.append(clip_path)
        print(f"  Saved: {clip_path}")

    return clips


def generate_bgm(output_dir, total_duration):
    """Generate synthetic ambient BGM using FFmpeg sine waves."""
    bgm_path = output_dir / "audio" / "bgm_ambient.m4a"
    bgm_path.parent.mkdir(parents=True, exist_ok=True)

    if bgm_path.exists():
        print(f"[SKIP] BGM already exists: {bgm_path}")
        return bgm_path

    fade_start = max(0, total_duration - 2)
    print(f"[Step 5] Generating {total_duration}s ambient BGM...")

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=220:duration={total_duration}",
        "-f", "lavfi", "-i", f"sine=frequency=277:duration={total_duration}",
        "-f", "lavfi", "-i", f"sine=frequency=330:duration={total_duration}",
        "-filter_complex", (
            f"[0:a]volume=0.15[a0];"
            f"[1:a]volume=0.12[a1];"
            f"[2:a]volume=0.10[a2];"
            f"[a0][a1][a2]amix=inputs=3:duration=first[mixed];"
            f"[mixed]afade=t=in:ss=0:d=2,afade=t=out:st={fade_start}:d=2,lowpass=f=800[out]"
        ),
        "-map", "[out]", "-c:a", "aac", "-b:a", "128k",
        str(bgm_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200]}")
        return None
    print(f"  Saved: {bgm_path}")
    return bgm_path


def assemble_video(clips, bgm_path, output_dir, clip_duration=5, fade_duration=0.5):
    """Concatenate clips with crossfade and mix BGM."""
    vlog_no_music = output_dir / "vlog_no_music.mp4"
    final_vlog = output_dir / "final_vlog.mp4"

    if final_vlog.exists():
        print(f"[SKIP] Final vlog already exists: {final_vlog}")
        return final_vlog

    n = len(clips)
    if n == 0:
        print("  ERROR: No clips to assemble")
        return None

    if n == 1:
        import shutil
        shutil.copy(str(clips[0]), str(vlog_no_music))
    else:
        print(f"[Step 6] Assembling {n} clips with crossfade transitions...")
        inputs = []
        for clip in clips:
            inputs.extend(["-i", str(clip)])

        filter_parts = []
        prev_label = "0:v"
        for i in range(1, n):
            offset = i * clip_duration - i * fade_duration
            out_label = f"v{''.join(str(j) for j in range(i+1))}"
            if i == 1:
                filter_parts.append(
                    f"[{prev_label}][{i}:v]xfade=transition=fade:duration={fade_duration}:offset={offset}[{out_label}]"
                )
            else:
                filter_parts.append(
                    f"[{prev_label}][{i}:v]xfade=transition=fade:duration={fade_duration}:offset={offset}[{out_label}]"
                )
            prev_label = out_label

        filter_complex = ";".join(filter_parts)
        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", filter_complex,
            "-map", f"[{prev_label}]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(vlog_no_music)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR concat: {result.stderr[:300]}")
            filelist = output_dir / "clips" / "filelist.txt"
            with open(filelist, "w") as f:
                for clip in clips:
                    f.write(f"file '{clip}'\n")
            cmd_fallback = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(filelist), "-c", "copy", str(vlog_no_music)
            ]
            subprocess.run(cmd_fallback, capture_output=True, text=True)

    if bgm_path and bgm_path.exists():
        print("[Step 6b] Mixing BGM into final video...")
        cmd_mix = [
            "ffmpeg", "-y",
            "-i", str(vlog_no_music), "-i", str(bgm_path),
            "-filter_complex", "[1:a]volume=0.6[bgm];[bgm]apad[bgmpad]",
            "-map", "0:v", "-map", "[bgmpad]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
            str(final_vlog)
        ]
        result = subprocess.run(cmd_mix, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ERROR mix: {result.stderr[:200]}")
            import shutil
            shutil.copy(str(vlog_no_music), str(final_vlog))
    else:
        import shutil
        shutil.copy(str(vlog_no_music), str(final_vlog))

    return final_vlog


def verify_output(final_path):
    """Run ffprobe to verify the final video."""
    print("\n[Step 7] Verification...")
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", str(final_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("  WARN: ffprobe failed")
        return

    info = json.loads(result.stdout)
    duration = float(info.get("format", {}).get("duration", 0))
    size_mb = int(info.get("format", {}).get("size", 0)) / (1024 * 1024)

    streams = info.get("streams", [])
    video_stream = next((s for s in streams if s["codec_type"] == "video"), None)
    audio_stream = next((s for s in streams if s["codec_type"] == "audio"), None)

    print(f"  Duration: {duration:.1f}s")
    print(f"  Size: {size_mb:.2f} MB")
    if video_stream:
        print(f"  Video: {video_stream.get('codec_name')} {video_stream.get('width')}x{video_stream.get('height')}")
    if audio_stream:
        print(f"  Audio: {audio_stream.get('codec_name')}")
    print(f"\n  Final video: {final_path}")


def main():
    parser = argparse.ArgumentParser(description="Virtual Couple Travel Vlog Generator")
    parser.add_argument("--destination", default="Tokyo", help="Travel destination")
    parser.add_argument("--scenes", type=int, default=5, help="Number of scenes (max 6)")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    parser.add_argument("--boy", default="boy has short dark hair, navy jacket",
                       help="Boy character description")
    parser.add_argument("--girl", default="girl has shoulder-length brown hair, beige cardigan",
                       help="Girl character description")
    parser.add_argument("--clip-duration", type=int, default=5, help="Duration per clip in seconds")
    args = parser.parse_args()

    check_prerequisites()

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        from datetime import date
        today = date.today().isoformat()
        output_dir = Path(f"outputs/vlog-{args.destination.lower()}/{today}")

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n{'='*60}")
    print(f"  Virtual Couple Travel Vlog Generator v2.0")
    print(f"  Destination: {args.destination}")
    print(f"  Scenes: {args.scenes}")
    print(f"  Output: {output_dir}")
    print(f"{'='*60}\n")

    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    default_scenes = [
        {"slug": "street", "action": "walking through a vibrant street", "location": f"{args.destination} with cherry blossoms and neon signs", "mood": "Warm sunset lighting"},
        {"slug": "cafe", "action": "sitting together sharing drinks", "location": f"a cozy cafe in {args.destination}", "mood": "Warm interior lighting, soft bokeh background"},
        {"slug": "temple", "action": "standing in front of a beautiful landmark", "location": f"a famous cultural site in {args.destination}", "mood": "Golden hour, autumn colors"},
        {"slug": "beach", "action": "walking on a serene waterfront at sunset", "location": f"a scenic waterfront near {args.destination}", "mood": "Orange and pink sky reflecting on water"},
        {"slug": "night_city", "action": "looking at city lights from a rooftop", "location": f"an observation deck overlooking {args.destination} at night", "mood": "Sparkling city below, starry sky, romantic atmosphere"},
        {"slug": "market", "action": "browsing colorful stalls together", "location": f"a traditional night market in {args.destination}", "mood": "Warm golden lamp light, lively and festive atmosphere"},
    ]
    scenes = default_scenes[: min(args.scenes, 6)]

    grid_path = generate_character_grid(client, args.boy, args.girl, output_dir)
    split_grid(grid_path, output_dir)
    scene_paths = generate_scene_images(client, scenes, args.boy, args.girl, output_dir)

    clips = create_ken_burns_clips(scene_paths, output_dir, duration=args.clip_duration)

    n = len(clips)
    fade = 0.5
    total_duration = n * args.clip_duration - (n - 1) * fade if n > 1 else args.clip_duration
    bgm_path = generate_bgm(output_dir, int(total_duration) + 1)

    final_path = assemble_video(clips, bgm_path, output_dir, args.clip_duration, fade)

    if final_path and final_path.exists():
        verify_output(final_path)
        cost = 0.08 + len(scenes) * 0.12
        print(f"\n  Estimated DALL-E 3 cost: ${cost:.2f}")
        print("  DONE")
    else:
        print("\n  FAILED: Final video was not created.")
        sys.exit(1)


if __name__ == "__main__":
    main()
