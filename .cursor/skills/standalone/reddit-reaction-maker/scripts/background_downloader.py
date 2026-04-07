"""Background video and audio asset manager with yt-dlp auto-download."""

import json
import os
import random
from pathlib import Path

import requests
from rich.console import Console

console = Console()

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a"}

SKILL_DIR = Path(__file__).resolve().parent.parent

DEFAULT_VIDEOS = {
    "satisfying-gameplay": {
        "url": "https://www.youtube.com/watch?v=n_Dv4JMiwK8",
        "filename": "satisfying-gameplay.mp4",
        "credit": "bbswitzer",
        "label": "Minecraft Parkour",
    },
    "subway-surfers": {
        "url": "https://www.youtube.com/watch?v=DSCEjJpJcbg",
        "filename": "subway-surfers.mp4",
        "credit": "Gameplay",
        "label": "Subway Surfers",
    },
}

DEFAULT_AUDIOS = {
    "lofi-chill": {
        "url": "https://cdn.pixabay.com/audio/2024/11/01/audio_1f6a4e0e70.mp3",
        "filename": "lofi-chill.mp3",
        "credit": "Pixabay",
        "license": "Pixabay Content License (free)",
        "title": "Lofi Chill",
    },
    "good-night": {
        "url": "https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3",
        "filename": "good-night.mp3",
        "credit": "FASSounds (Pixabay)",
        "license": "Pixabay Content License (free)",
        "title": "Good Night",
    },
}


def _download_ytdlp(url: str, output_path: str, is_audio: bool = False) -> bool:
    try:
        import yt_dlp
    except ImportError:
        console.print("[red]yt-dlp not installed. Run: pip install yt-dlp[/red]")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_template = os.path.splitext(output_path)[0]

    ydl_opts: dict = {
        "outtmpl": output_template + ".%(ext)s",
        "retries": 5,
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
    }

    if is_audio:
        ydl_opts.update(
            {
                "format": "bestaudio/best",
                "extract_audio": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
    else:
        ydl_opts.update(
            {
                "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
                "merge_output_format": "mp4",
            }
        )

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        console.print(f"[red]yt-dlp download error: {e}[/red]")
        return False


def _download_direct(url: str, output_path: str) -> bool:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        resp = requests.get(url, stream=True, timeout=60, verify=False)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        console.print(f"[red]Direct download error: {e}[/red]")
        return False


def _load_json_catalog(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def download_videos(background_dir: str) -> list[str]:
    video_dir = Path(background_dir) / "video"
    video_dir.mkdir(parents=True, exist_ok=True)

    catalog_path = SKILL_DIR / "assets" / "background_videos.json"
    catalog = _load_json_catalog(catalog_path).get("videos", DEFAULT_VIDEOS)

    downloaded: list[str] = []

    for key, info in catalog.items():
        filename = info.get("filename", f"{key}.mp4")
        output_path = str(video_dir / filename)

        if os.path.exists(output_path):
            downloaded.append(output_path)
            continue

        url = info.get("url", "")
        if not url:
            continue

        console.print(f"  [cyan]Downloading video: {info.get('label', key)}...[/cyan]")
        if _download_ytdlp(url, output_path, is_audio=False):
            found = _find_downloaded(output_path, [".mp4", ".webm", ".mkv"])
            if found:
                downloaded.append(found)
                console.print(f"    [green]✓[/green] {info.get('label', key)}")
            else:
                console.print(f"    [yellow]File not found after download: {key}[/yellow]")

    for f in video_dir.iterdir():
        full = str(f)
        if f.suffix.lower() in VIDEO_EXTENSIONS and full not in downloaded:
            downloaded.append(full)

    return downloaded


def download_audios(background_dir: str) -> list[str]:
    audio_dir = Path(background_dir) / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    catalog_path = SKILL_DIR / "assets" / "background_audios.json"
    catalog = _load_json_catalog(catalog_path).get("audios", DEFAULT_AUDIOS)

    downloaded: list[str] = []

    for key, info in catalog.items():
        filename = info.get("filename", f"{key}.mp3")
        output_path = str(audio_dir / filename)

        if os.path.exists(output_path):
            downloaded.append(output_path)
            continue

        url = info.get("url", "")
        if not url:
            continue

        console.print(f"  [cyan]Downloading audio: {info.get('title', key)}...[/cyan]")
        is_yt = "youtube.com" in url or "youtu.be" in url
        success = _download_ytdlp(url, output_path, is_audio=True) if is_yt else _download_direct(url, output_path)

        if success and os.path.exists(output_path):
            downloaded.append(output_path)
            console.print(f"    [green]✓[/green] {info.get('title', key)}")
        else:
            found = _find_downloaded(output_path, [".mp3", ".m4a", ".ogg", ".wav"])
            if found:
                downloaded.append(found)
                console.print(f"    [green]✓[/green] {info.get('title', key)}")
            else:
                console.print(f"    [yellow]Failed: {key}[/yellow]")

    for f in audio_dir.iterdir():
        full = str(f)
        if f.suffix.lower() in AUDIO_EXTENSIONS and full not in downloaded:
            downloaded.append(full)

    return downloaded


def setup_backgrounds(background_dir: str) -> dict:
    console.print("[cyan]Setting up background assets...[/cyan]")
    videos = download_videos(background_dir)
    audios = download_audios(background_dir)
    console.print(f"  [green]Ready:[/green] {len(videos)} video(s), {len(audios)} audio(s)")
    return {"videos": videos, "audios": audios}


def select_random_video(background_dir: str) -> str | None:
    video_dir = Path(background_dir) / "video"
    dirs = [video_dir, Path(background_dir)]
    all_vids = []
    for d in dirs:
        if d.exists():
            all_vids.extend(
                str(f) for f in d.iterdir() if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS
            )
    return random.choice(all_vids) if all_vids else None


def select_random_audio(background_dir: str) -> str | None:
    audio_dir = Path(background_dir) / "audio"
    if not audio_dir.exists():
        return None
    audios = [str(f) for f in audio_dir.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS]
    return random.choice(audios) if audios else None


def random_start_time(video_duration: float, clip_duration: float) -> float:
    mx = max(0, video_duration - clip_duration - 1)
    return random.uniform(0, mx) if mx > 0 else 0


def _find_downloaded(expected: str, extensions: list[str]) -> str | None:
    if os.path.exists(expected):
        return expected
    base = os.path.splitext(expected)[0]
    for ext in extensions:
        candidate = base + ext
        if os.path.exists(candidate):
            return candidate
    return None
