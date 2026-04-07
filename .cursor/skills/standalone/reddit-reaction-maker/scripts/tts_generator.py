"""Korean TTS generator using gTTS."""

import os
import re
from pathlib import Path

from gtts import gTTS
from rich.console import Console

console = Console()

EMOJI_PATTERN = re.compile(
    "["
    "\U0001f600-\U0001f64f"
    "\U0001f300-\U0001f5ff"
    "\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff"
    "\U00002702-\U000027b0"
    "\U000024c2-\U0001f251"
    "\U0001f900-\U0001f9ff"
    "\U0001fa00-\U0001fa6f"
    "\U0001fa70-\U0001faff"
    "\U00002600-\U000026ff"
    "]+",
    flags=re.UNICODE,
)


def clean_text(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"r/\w+", "", text)
    text = re.sub(r"u/\w+", "", text)
    text = EMOJI_PATTERN.sub("", text)
    text = re.sub(r"[*_~`#>]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_audio(text: str, output_path: str, language: str = "ko", max_chars: int = 500) -> str | None:
    cleaned = clean_text(text)
    if not cleaned:
        return None

    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars].rsplit(" ", 1)[0] + "..."

    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        tts = gTTS(text=cleaned, lang=language, slow=False)
        tts.save(output_path)
        return output_path
    except Exception as e:
        console.print(f"[red]TTS error: {e}[/red]")
        return None


def generate_for_post(post, output_dir: str, language: str = "ko") -> list[dict]:
    """Generate TTS audio for all segments of a post.

    Returns list of dicts with text, audio_path, type, and optional author/score.
    """
    os.makedirs(output_dir, exist_ok=True)
    segments: list[dict] = []

    title_path = os.path.join(output_dir, "title.mp3")
    result = generate_audio(post.title, title_path, language)
    if result:
        segments.append(
            {
                "text": clean_text(post.title),
                "audio_path": result,
                "type": "title",
                "author": post.author,
                "score": post.score,
                "subreddit": post.subreddit,
            }
        )

    if post.body and post.body.strip() and len(post.body.strip()) <= 300:
        body_path = os.path.join(output_dir, "body.mp3")
        result = generate_audio(post.body, body_path, language)
        if result:
            segments.append(
                {
                    "text": clean_text(post.body),
                    "audio_path": result,
                    "type": "body",
                }
            )

    for i, comment in enumerate(post.comments):
        comment_path = os.path.join(output_dir, f"comment_{i}.mp3")
        result = generate_audio(comment.body, comment_path, language)
        if result:
            segments.append(
                {
                    "text": clean_text(comment.body),
                    "audio_path": result,
                    "type": "comment",
                    "author": comment.author,
                    "score": comment.score,
                }
            )

    console.print(f"  [green]✓[/green] Generated {len(segments)} audio segments")
    return segments
