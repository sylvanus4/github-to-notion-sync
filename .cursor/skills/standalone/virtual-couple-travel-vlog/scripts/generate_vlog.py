#!/usr/bin/env python3
"""
Virtual Couple Travel Vlog Generator v5.0
ALL Google Latest Models (2026-05):
  - Image: Imagen 4 (imagen-4.0-generate-001)
  - Video: Veo 3.1 (veo-3.1-generate-preview)
Zero OpenAI dependency.
Usage: python3 generate_vlog.py --destination "Tokyo" [--scenes 5] [--output-dir ./output]
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("ERROR: 'Pillow' package not installed. Run: pip install Pillow")

try:
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit("ERROR: 'google-genai' package not installed. Run: pip install google-genai")


def check_prerequisites():
    """Verify ffmpeg and API key."""
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit("ERROR: ffmpeg not found. Install with: brew install ffmpeg")

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("ERROR: GEMINI_API_KEY not set.")

    print("[OK] Prerequisites: google-genai, Pillow, ffmpeg, GEMINI_API_KEY")


def generate_character_grid(client, boy_desc, girl_desc, output_dir):
    """Generate 2x2 character identity grid using Imagen 3."""
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

    print("[Step 2] Generating character grid via Imagen 3...")
    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        ),
    )

    if response.generated_images:
        img = response.generated_images[0]
        img.image.save(str(grid_path))
        print(f"  Saved: {grid_path} ({grid_path.stat().st_size} bytes)")
    else:
        sys.exit("ERROR: Imagen 3 returned no images for character grid.")

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
    """Generate landscape scene images using Imagen 3."""
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
            f"{scene['mood']}. Illustration style, 16:9 cinematic composition, "
            f"highly detailed background, beautiful lighting."
        )

        print(f"[Step 3] Generating scene {i}/{len(scenes)}: {scene['slug']} (Imagen 3)...")
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
            ),
        )

        if response.generated_images:
            img = response.generated_images[0]
            img.image.save(str(path))
            print(f"  Saved: {path} ({path.stat().st_size} bytes)")
            generated.append(path)
        else:
            print(f"  WARNING: Imagen 3 returned no image for scene {i}")

        time.sleep(2)

    return generated


def generate_video_clips_veo(client, scenes, boy_desc, girl_desc, output_dir):
    """Generate actual AI video clips using Google Veo 3.1."""
    clips_dir = output_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)

    clips = []

    for i, scene in enumerate(scenes, 1):
        clip_path = clips_dir / f"clip_{i:02d}.mp4"
        if clip_path.exists():
            print(f"[SKIP] Clip {i} already exists: {clip_path}")
            clips.append(clip_path)
            continue

        video_prompt = (
            f"A cute anime couple ({boy_desc}; {girl_desc}) "
            f"{scene['action']} in {scene['location']}. "
            f"{scene['mood']}. Smooth camera movement, cinematic, "
            f"anime illustration style, warm colors, gentle ambient sounds."
        )

        print(f"[Step 4] Generating Veo 3.1 video clip {i}/{len(scenes)}: {scene['slug']}...")
        try:
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=video_prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio="16:9",
                    number_of_videos=1,
                ),
            )

            poll_count = 0
            max_polls = 60
            while not operation.done:
                poll_count += 1
                if poll_count > max_polls:
                    print(f"  TIMEOUT: Veo 3.1 took too long for clip {i}, skipping.")
                    break
                if poll_count % 6 == 0:
                    print(f"    ...waiting ({poll_count * 10}s elapsed)")
                time.sleep(10)
                operation = client.operations.get(operation)

            if operation.done and operation.response:
                generated_video = operation.response.generated_videos[0]
                client.files.download(file=generated_video.video)
                generated_video.video.save(str(clip_path))
                print(f"  Saved: {clip_path} ({clip_path.stat().st_size} bytes)")
                clips.append(clip_path)
            else:
                print(f"  WARNING: Veo 3.1 failed for clip {i}, falling back to Ken Burns.")
                clips.append(None)

        except Exception as e:
            print(f"  ERROR Veo 3.1 clip {i}: {e}")
            print(f"  Falling back to Ken Burns for this clip.")
            clips.append(None)

        time.sleep(2)

    return clips


def create_ken_burns_fallback(scene_path, clip_path, duration=5):
    """Fallback: Ken Burns zoom on a static image."""
    frames = duration * 30
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
    return result.returncode == 0


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


def assemble_video(clips, bgm_path, output_dir):
    """Concatenate clips and mix BGM."""
    final_vlog = output_dir / "final_vlog.mp4"

    if final_vlog.exists():
        print(f"[SKIP] Final vlog already exists: {final_vlog}")
        return final_vlog

    valid_clips = [c for c in clips if c and c.exists()]
    n = len(valid_clips)
    if n == 0:
        print("  ERROR: No clips to assemble")
        return None

    print(f"[Step 6] Assembling {n} video clips...")

    filelist = output_dir / "clips" / "filelist.txt"
    with open(filelist, "w") as f:
        for clip in valid_clips:
            f.write(f"file '{clip.resolve()}'\n")

    vlog_no_music = output_dir / "vlog_no_music.mp4"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(filelist), "-c", "copy", str(vlog_no_music)
    ]
    result = subprocess.run(cmd_concat, capture_output=True, text=True)
    if result.returncode != 0:
        cmd_concat_reencode = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(filelist),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            str(vlog_no_music)
        ]
        subprocess.run(cmd_concat_reencode, capture_output=True, text=True)

    if bgm_path and bgm_path.exists() and vlog_no_music.exists():
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
            import shutil
            shutil.copy(str(vlog_no_music), str(final_vlog))
    elif vlog_no_music.exists():
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
    parser = argparse.ArgumentParser(description="Virtual Couple Travel Vlog Generator v4.0")
    parser.add_argument("--destination", default="Tokyo", help="Travel destination")
    parser.add_argument("--scenes", type=int, default=5, help="Number of scenes (max 6)")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    parser.add_argument("--boy", default="boy has short dark hair, navy jacket",
                       help="Boy character description")
    parser.add_argument("--girl", default="girl has shoulder-length brown hair, beige cardigan",
                       help="Girl character description")
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
    print(f"  Virtual Couple Travel Vlog Generator v4.0")
    print(f"  Image: Google Imagen 3 (imagen-4.0-generate-001)")
    print(f"  Video: Google Veo 3.1 (veo-3.1-generate-preview)")
    print(f"  Destination: {args.destination}")
    print(f"  Scenes: {args.scenes}")
    print(f"  Output: {output_dir}")
    print(f"{'='*60}\n")

    gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    default_scenes = [
        {"slug": "street", "action": "walking through a vibrant street", "location": f"{args.destination} with cherry blossoms and neon signs", "mood": "Warm sunset lighting, bustling atmosphere"},
        {"slug": "cafe", "action": "sitting together sharing drinks", "location": f"a cozy cafe in {args.destination}", "mood": "Warm interior lighting, soft bokeh background"},
        {"slug": "temple", "action": "standing in front of a beautiful landmark", "location": f"a famous cultural site in {args.destination}", "mood": "Golden hour, autumn colors"},
        {"slug": "beach", "action": "walking on a serene waterfront at sunset", "location": f"a scenic waterfront near {args.destination}", "mood": "Orange and pink sky reflecting on water"},
        {"slug": "night_city", "action": "looking at city lights from a rooftop", "location": f"an observation deck overlooking {args.destination} at night", "mood": "Sparkling city below, starry sky, romantic atmosphere"},
        {"slug": "market", "action": "browsing colorful stalls together", "location": f"a traditional night market in {args.destination}", "mood": "Warm golden lamp light, lively and festive atmosphere"},
    ]

    num_scenes = min(args.scenes, len(default_scenes))
    scenes = default_scenes[:num_scenes]

    print(f"[Step 1] Planning {num_scenes} scenes for {args.destination}...")
    for i, s in enumerate(scenes, 1):
        print(f"  {i}. {s['slug']}: {s['action']}")

    grid_path = generate_character_grid(gemini_client, args.boy, args.girl, output_dir)
    chars_dir = split_grid(grid_path, output_dir)
    scene_images = generate_scene_images(gemini_client, scenes, args.boy, args.girl, output_dir)

    veo_clips = generate_video_clips_veo(gemini_client, scenes, args.boy, args.girl, output_dir)

    final_clips = []
    for i, (clip, scene) in enumerate(zip(veo_clips, scenes)):
        if clip and clip.exists():
            final_clips.append(clip)
        elif i < len(scene_images) and scene_images[i].exists():
            fallback_path = output_dir / "clips" / f"clip_{i+1:02d}.mp4"
            if not fallback_path.exists():
                print(f"  Creating Ken Burns fallback for scene {i+1}...")
                create_ken_burns_fallback(scene_images[i], fallback_path, duration=5)
            if fallback_path.exists():
                final_clips.append(fallback_path)

    total_duration = len(final_clips) * 5
    bgm_path = generate_bgm(output_dir, total_duration)
    final_vlog = assemble_video(final_clips, bgm_path, output_dir)

    if final_vlog and final_vlog.exists():
        verify_output(final_vlog)
        print("\n" + "=" * 60)
        print("  DONE! Vlog generated successfully.")
        print(f"  {final_vlog}")
        print("=" * 60)
    else:
        print("\n  ERROR: Final video generation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
