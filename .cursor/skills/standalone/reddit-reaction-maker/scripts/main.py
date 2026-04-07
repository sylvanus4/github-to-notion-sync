#!/usr/bin/env python3
"""Reddit Reaction Video Maker — CLI entry point.

6-phase pipeline:
  1. Scrape Reddit posts     → phase-1-posts.json
  2. Generate TTS audio      → phase-2-audio/
  3. Render card images      → phase-3-cards/
  4. Download backgrounds    → assets/backgrounds/
  5. Compose final video     → final-*.mp4
  6. Distribution (Slack)    → (optional, handled by Cursor skill)
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

from rich.console import Console

console = Console()

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = SKILL_DIR / "config.json"


def load_config(config_path: str | None = None) -> dict:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def run_pipeline(
    config: dict,
    output_base: str,
    skip_scrape: bool = False,
    skip_tts: bool = False,
    skip_cards: bool = False,
    skip_bg: bool = False,
    skip_compose: bool = False,
    subreddit: str | None = None,
    time_filter: str = "week",
) -> list[str]:
    """Run the full pipeline and return list of output video paths."""

    today = date.today().isoformat()
    output_dir = os.path.join(output_base, today)
    os.makedirs(output_dir, exist_ok=True)

    if subreddit:
        config["subreddit"] = subreddit

    language = config.get("language", "ko")
    font_name = config.get("font", "NotoSansKR-Bold.ttf")

    posts_file = os.path.join(output_dir, "phase-1-posts.json")
    audio_dir = os.path.join(output_dir, "phase-2-audio")
    cards_dir = os.path.join(output_dir, "phase-3-cards")
    bg_dir = config.get("background_dir", "assets/backgrounds")

    # ── Phase 1: Scrape Reddit ──
    from .reddit_scraper import RedditScraper, RedditPost

    if skip_scrape and os.path.exists(posts_file):
        console.print("[dim]Phase 1: Skipped (using cached posts)[/dim]")
        posts = RedditScraper.load_posts(posts_file)
    else:
        console.rule("[bold cyan]Phase 1: Reddit Scrape[/bold cyan]")
        scraper = RedditScraper(config)
        posts = scraper.fetch_posts(time_filter=time_filter)
        if not posts:
            console.print("[red]No posts found. Aborting.[/red]")
            return []
        scraper.save_posts(posts, posts_file)

    # ── Phase 2: TTS Audio ──
    from .tts_generator import generate_for_post

    all_segments: dict[str, list[dict]] = {}

    if skip_tts:
        console.print("[dim]Phase 2: Skipped (--skip-tts)[/dim]")
        segments_file = os.path.join(output_dir, "phase-2-segments.json")
        if os.path.exists(segments_file):
            with open(segments_file, "r", encoding="utf-8") as f:
                all_segments = json.load(f)
    else:
        console.rule("[bold cyan]Phase 2: TTS Audio[/bold cyan]")
        for post in posts:
            post_audio_dir = os.path.join(audio_dir, post.id)
            segments = generate_for_post(post, post_audio_dir, language)
            all_segments[post.id] = segments

        segments_file = os.path.join(output_dir, "phase-2-segments.json")
        with open(segments_file, "w", encoding="utf-8") as f:
            json.dump(all_segments, f, ensure_ascii=False, indent=2)

    # ── Phase 3: Card Rendering ──
    from .card_renderer import render_cards_for_post

    if skip_cards:
        console.print("[dim]Phase 3: Skipped (--skip-cards)[/dim]")
    else:
        console.rule("[bold cyan]Phase 3: Card Rendering[/bold cyan]")
        video_width = config.get("video_width", 1080)
        for post_id, segments in all_segments.items():
            post_cards_dir = os.path.join(cards_dir, post_id)
            render_cards_for_post(segments, post_cards_dir, video_width, font_name)

        segments_file = os.path.join(output_dir, "phase-2-segments.json")
        with open(segments_file, "w", encoding="utf-8") as f:
            json.dump(all_segments, f, ensure_ascii=False, indent=2)

    # ── Phase 4: Background Assets ──
    from .background_downloader import setup_backgrounds

    if skip_bg:
        console.print("[dim]Phase 4: Skipped (--skip-bg)[/dim]")
    else:
        console.rule("[bold cyan]Phase 4: Background Assets[/bold cyan]")
        setup_backgrounds(bg_dir)

    # ── Phase 5: Video Composition ──
    from .video_composer import VideoComposer

    videos: list[str] = []

    if skip_compose:
        console.print("[dim]Phase 5: Skipped (--skip-compose)[/dim]")
    else:
        console.rule("[bold cyan]Phase 5: Video Composition[/bold cyan]")
        composer = VideoComposer(config)

        posts_by_id = {p.id: p for p in posts}
        for post_id, segments in all_segments.items():
            post = posts_by_id.get(post_id)
            if not post:
                continue

            if not segments:
                console.print(f"  [yellow]No segments for {post_id}, skipping[/yellow]")
                continue

            video_path = composer.compose(
                post_id=post.id,
                post_title=post.title,
                segments=segments,
                output_dir=output_dir,
            )
            if video_path:
                videos.append(video_path)

    # ── Summary ──
    console.rule("[bold green]Pipeline Complete[/bold green]")
    console.print(f"  Output directory: {output_dir}")
    console.print(f"  Videos generated: {len(videos)}")
    for v in videos:
        size_mb = os.path.getsize(v) / (1024 * 1024)
        console.print(f"    • {v} ({size_mb:.1f}MB)")

    return videos


def main():
    parser = argparse.ArgumentParser(description="Reddit Reaction Video Maker")
    parser.add_argument("--config", help="Config JSON path")
    parser.add_argument("--subreddit", "-s", help="Override subreddit")
    parser.add_argument("--time-filter", "-t", default="week", choices=["hour", "day", "week", "month", "year", "all"])
    parser.add_argument("--output", "-o", default="outputs/reddit-reaction", help="Output base directory")
    parser.add_argument("--skip-scrape", action="store_true")
    parser.add_argument("--skip-tts", action="store_true")
    parser.add_argument("--skip-cards", action="store_true")
    parser.add_argument("--skip-bg", action="store_true")
    parser.add_argument("--skip-compose", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)

    videos = run_pipeline(
        config=config,
        output_base=args.output,
        skip_scrape=args.skip_scrape,
        skip_tts=args.skip_tts,
        skip_cards=args.skip_cards,
        skip_bg=args.skip_bg,
        skip_compose=args.skip_compose,
        subreddit=args.subreddit,
        time_filter=args.time_filter,
    )

    sys.exit(0 if videos else 1)


if __name__ == "__main__":
    main()
