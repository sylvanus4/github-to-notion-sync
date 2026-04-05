#!/usr/bin/env python3
"""Pika Video Generation via fal.ai API.

Supports text-to-video, image-to-video, pikascenes, pikaframes,
pikaffects, pikaswaps, and pikadditions endpoints.

Exit codes:
  0  Success (JSON with video URL printed to stdout)
  1  General error
  2  Missing required arguments or invalid input
  3  API / HTTP error
  4  Missing FAL_KEY environment variable
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

try:
    import fal_client
except ImportError:
    print(
        json.dumps({"error": "fal-client not installed. Run: pip install fal-client"}),
        file=sys.stderr,
    )
    raise SystemExit(1)


ENDPOINTS = {
    "text-to-video": "fal-ai/pika/v2.2/text-to-video",
    "image-to-video": "fal-ai/pika/v2.2/image-to-video",
    "pikascenes": "fal-ai/pika/v2.2/pikascenes",
    "pikaframes": "fal-ai/pika/v2.2/pikaframes",
    "pikaffects": "fal-ai/pika/v2.2/pikaffects",
    "pikaswaps": "fal-ai/pika/v2.2/pikaswaps",
    "pikadditions": "fal-ai/pika/v2.2/pikadditions",
}

PIKAFFECTS = [
    "Cake-ify", "Crumble", "Crush", "Decapitate", "Deflate", "Dissolve",
    "Explode", "Eye-pop", "Inflate", "Levitate", "Melt", "Peel",
    "Poke", "Squish", "Ta-da", "Tear",
]


def _upload_if_local(path: str) -> str:
    """Upload a local file to fal storage and return the URL."""
    if path.startswith(("http://", "https://", "data:")):
        return path
    p = Path(path)
    if not p.exists():
        print(json.dumps({"error": f"File not found: {path}"}), file=sys.stderr)
        raise SystemExit(2)
    url = fal_client.upload_file(p)
    return url


def _build_input(args: argparse.Namespace) -> dict[str, Any]:
    """Build the API input payload from parsed arguments."""
    mode = args.mode
    inp: dict[str, Any] = {}

    if args.prompt:
        inp["prompt"] = args.prompt
    if args.negative_prompt:
        inp["negative_prompt"] = args.negative_prompt
    if args.seed is not None:
        inp["seed"] = args.seed

    if mode == "text-to-video":
        if not args.prompt:
            print(json.dumps({"error": "--prompt is required for text-to-video"}), file=sys.stderr)
            raise SystemExit(2)
        inp["aspect_ratio"] = args.aspect_ratio
        inp["resolution"] = args.resolution
        inp["duration"] = int(args.duration)

    elif mode == "image-to-video":
        if not args.image:
            print(json.dumps({"error": "--image is required for image-to-video"}), file=sys.stderr)
            raise SystemExit(2)
        if not args.prompt:
            print(json.dumps({"error": "--prompt is required for image-to-video"}), file=sys.stderr)
            raise SystemExit(2)
        inp["image_url"] = _upload_if_local(args.image)
        inp["resolution"] = args.resolution
        inp["duration"] = int(args.duration)

    elif mode == "pikascenes":
        if not args.images or len(args.images) < 1:
            print(json.dumps({"error": "--images (1+) required for pikascenes"}), file=sys.stderr)
            raise SystemExit(2)
        if not args.prompt:
            print(json.dumps({"error": "--prompt is required for pikascenes"}), file=sys.stderr)
            raise SystemExit(2)
        inp["image_urls"] = [{"image_url": _upload_if_local(i)} for i in args.images]
        inp["aspect_ratio"] = args.aspect_ratio
        inp["resolution"] = args.resolution
        inp["duration"] = int(args.duration)
        if args.ingredients_mode:
            inp["ingredients_mode"] = args.ingredients_mode

    elif mode == "pikaframes":
        if not args.images or len(args.images) < 2:
            print(json.dumps({"error": "--images (2-5 keyframes) required for pikaframes"}), file=sys.stderr)
            raise SystemExit(2)
        inp["image_urls"] = [_upload_if_local(i) for i in args.images]
        inp["resolution"] = args.resolution

    elif mode == "pikaffects":
        if not args.image:
            print(json.dumps({"error": "--image is required for pikaffects"}), file=sys.stderr)
            raise SystemExit(2)
        if not args.effect:
            print(json.dumps({"error": f"--effect is required for pikaffects. Choose from: {', '.join(PIKAFFECTS)}"}), file=sys.stderr)
            raise SystemExit(2)
        inp["image_url"] = _upload_if_local(args.image)
        inp["pikaffect"] = args.effect

    elif mode == "pikaswaps":
        if not args.video_url:
            print(json.dumps({"error": "--video-url is required for pikaswaps"}), file=sys.stderr)
            raise SystemExit(2)
        inp["video_url"] = args.video_url
        if args.image:
            inp["image_url"] = _upload_if_local(args.image)
        if args.modify_region:
            inp["modify_region"] = args.modify_region

    elif mode == "pikadditions":
        if not args.video_url:
            print(json.dumps({"error": "--video-url is required for pikadditions"}), file=sys.stderr)
            raise SystemExit(2)
        if not args.image:
            print(json.dumps({"error": "--image is required for pikadditions"}), file=sys.stderr)
            raise SystemExit(2)
        inp["video_url"] = args.video_url
        inp["image_url"] = _upload_if_local(args.image)

    return inp


def _run(endpoint: str, inp: dict[str, Any], output_path: str | None) -> dict[str, Any]:
    """Submit request to fal.ai and wait for result."""
    logs: list[str] = []

    def on_update(update: Any) -> None:
        if hasattr(update, "logs") and update.logs:
            for log in update.logs:
                msg = log.message if hasattr(log, "message") else str(log)
                logs.append(msg)
                print(f"[pika] {msg}", file=sys.stderr)

    try:
        result = fal_client.subscribe(
            endpoint,
            arguments=inp,
            with_logs=True,
            on_queue_update=on_update,
        )
    except Exception as exc:
        print(json.dumps({"error": f"API call failed: {exc}"}), file=sys.stderr)
        raise SystemExit(3)

    video_url = result.get("video", {}).get("url", "")

    if output_path and video_url:
        import urllib.request
        try:
            urllib.request.urlretrieve(video_url, output_path)
        except Exception as exc:
            print(f"[pika] Warning: failed to download video: {exc}", file=sys.stderr)

    return {
        "video_url": video_url,
        "output_path": output_path or "",
        "logs": logs,
    }


def main() -> int:
    if not os.environ.get("FAL_KEY"):
        print(json.dumps({"error": "FAL_KEY environment variable not set"}), file=sys.stderr)
        return 4

    parser = argparse.ArgumentParser(description="Pika video generation via fal.ai")
    parser.add_argument("mode", choices=list(ENDPOINTS.keys()), help="Generation mode")
    parser.add_argument("--prompt", "-p", help="Text prompt")
    parser.add_argument("--negative-prompt", help="Negative prompt")
    parser.add_argument("--image", "-i", help="Input image (local path or URL)")
    parser.add_argument("--images", nargs="+", help="Multiple input images (for pikascenes/pikaframes)")
    parser.add_argument("--video-url", help="Input video URL (for pikaswaps/pikadditions)")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16", "1:1", "4:5", "5:4", "3:2", "2:3"])
    parser.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p"])
    parser.add_argument("--duration", default="5", choices=["5", "10"])
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--effect", choices=PIKAFFECTS, help="Pikaffect effect name")
    parser.add_argument("--modify-region", help="Region description for pikaswaps")
    parser.add_argument("--ingredients-mode", choices=["creative", "precise"], help="Pikascenes mode")
    parser.add_argument("--output", "-o", help="Download video to this local path")

    args = parser.parse_args()
    endpoint = ENDPOINTS[args.mode]
    inp = _build_input(args)

    result = _run(endpoint, inp, args.output)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
