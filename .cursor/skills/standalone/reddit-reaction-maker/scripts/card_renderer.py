"""Reddit-style card renderer using Pillow with Korean font support."""

import os
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

console = Console()

COLORS = {
    "card_bg": (26, 26, 27),
    "card_border": (52, 53, 54),
    "title_text": (215, 218, 220),
    "body_text": (215, 218, 220),
    "meta_text": (129, 131, 132),
    "upvote": (255, 69, 0),
    "score_text": (215, 218, 220),
    "divider": (52, 53, 54),
}

NOTO_SANS_KR_URL = (
    "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf"
)
NOTO_SANS_KR_BOLD_URL = (
    "https://cdn.jsdelivr.net/gh/spoqa/spoqa-han-sans@latest/Subset/SpoqaHanSansNeo/SpoqaHanSansNeo-Bold.ttf"
)


def _ensure_font(font_name: str, cache_dir: str = "assets/fonts") -> str:
    """Download NotoSansKR or SpoqaHanSans if not present. Returns path."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / font_name

    if target.exists():
        return str(target)

    mac_candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/Library/Fonts/NanumGothic.ttf",
    ]
    for candidate in mac_candidates:
        if os.path.exists(candidate):
            return candidate

    console.print(f"[cyan]Downloading Korean font ({font_name})...[/cyan]")
    try:
        urllib.request.urlretrieve(NOTO_SANS_KR_BOLD_URL, str(target))
        console.print(f"  [green]✓[/green] Font saved to {target}")
        return str(target)
    except Exception as e:
        console.print(f"[yellow]Font download failed ({e}), using system default[/yellow]")
        return ""


def _load_font(font_path: str, size: int) -> ImageFont.FreeTypeFont:
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass

    fallbacks = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for f in fallbacks:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                continue

    return ImageFont.load_default(size)


def _wrap_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            if draw.textbbox((0, 0), word, font=font)[2] > max_width:
                while word:
                    for i in range(len(word), 0, -1):
                        part = word[:i]
                        if draw.textbbox((0, 0), part, font=font)[2] <= max_width:
                            lines.append(part)
                            word = word[i:]
                            break
                    else:
                        lines.append(word)
                        word = ""
                current = ""
            else:
                current = word

    if current:
        lines.append(current)
    return lines if lines else [""]


def _format_score(score: int) -> str:
    if score >= 1000:
        return f"{score / 1000:.1f}k"
    return str(score)


def render_title_card(
    title: str,
    author: str,
    score: int,
    subreddit: str,
    card_width: int = 800,
    font_path: str = "",
) -> Image.Image:
    padding = 30
    content_width = card_width - padding * 2

    title_font = _load_font(font_path, 32)
    meta_font = _load_font(font_path, 20)
    score_font = _load_font(font_path, 22)

    tmp = Image.new("RGB", (card_width, 100))
    draw = ImageDraw.Draw(tmp)

    meta_text = f"r/{subreddit}  ·  u/{author}"
    meta_h = draw.textbbox((0, 0), meta_text, font=meta_font)[3]

    title_lines = _wrap_text(draw, title, title_font, content_width)
    line_h = 42
    title_block_h = len(title_lines) * line_h

    score_str = _format_score(score)
    score_h = draw.textbbox((0, 0), f"▲ {score_str}", font=score_font)[3]

    card_h = padding + meta_h + 20 + title_block_h + 25 + score_h + padding

    img = Image.new("RGBA", (card_width, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, card_width, card_h], radius=16, fill=COLORS["card_bg"])

    y = padding
    draw.text((padding, y), meta_text, fill=COLORS["meta_text"], font=meta_font)
    y += meta_h + 20

    for line in title_lines:
        draw.text((padding, y), line, fill=COLORS["title_text"], font=title_font)
        y += line_h

    y += 10
    draw.line([(padding, y), (card_width - padding, y)], fill=COLORS["divider"], width=1)
    y += 15

    draw.text((padding, y), "▲", fill=COLORS["upvote"], font=score_font)
    draw.text((padding + 22, y), f" {score_str}", fill=COLORS["score_text"], font=score_font)

    return img


def render_comment_card(
    body: str,
    author: str,
    score: int,
    card_width: int = 800,
    font_path: str = "",
) -> Image.Image:
    padding = 30
    accent_w = 4
    inner_pad = padding + accent_w + 12

    body_font = _load_font(font_path, 28)
    meta_font = _load_font(font_path, 20)
    score_font = _load_font(font_path, 20)

    tmp = Image.new("RGB", (card_width, 100))
    draw = ImageDraw.Draw(tmp)

    meta_text = f"u/{author}"
    meta_h = draw.textbbox((0, 0), meta_text, font=meta_font)[3]

    body_w = card_width - inner_pad - padding
    body_lines = _wrap_text(draw, body, body_font, body_w)

    max_lines = 10
    if len(body_lines) > max_lines:
        body_lines = body_lines[:max_lines]
        body_lines[-1] = body_lines[-1][:40] + "..."

    line_h = 38
    body_block_h = len(body_lines) * line_h

    score_str = _format_score(score)
    score_h = draw.textbbox((0, 0), f"▲ {score_str}", font=score_font)[3]

    card_h = padding + meta_h + 16 + body_block_h + 20 + score_h + padding

    img = Image.new("RGBA", (card_width, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, card_width, card_h], radius=16, fill=COLORS["card_bg"])

    draw.rectangle(
        [padding, padding, padding + accent_w, card_h - padding],
        fill=COLORS["card_border"],
    )

    y = padding
    draw.text((inner_pad, y), meta_text, fill=COLORS["meta_text"], font=meta_font)
    y += meta_h + 16

    for line in body_lines:
        draw.text((inner_pad, y), line, fill=COLORS["body_text"], font=body_font)
        y += line_h

    y += 8
    draw.text((inner_pad, y), "▲", fill=COLORS["upvote"], font=score_font)
    draw.text((inner_pad + 18, y), f" {score_str}", fill=COLORS["score_text"], font=score_font)

    return img


def render_cards_for_post(
    segments: list[dict],
    output_dir: str,
    video_width: int = 1080,
    font_name: str = "NotoSansKR-Bold.ttf",
) -> list[dict]:
    """Render all card images for a post's segments.

    Mutates segments in-place, adding 'card_path' to each entry.
    """
    card_width = int(video_width * 0.85)
    os.makedirs(output_dir, exist_ok=True)

    font_path = _ensure_font(font_name)

    for i, seg in enumerate(segments):
        seg_type = seg.get("type", "comment")

        if seg_type == "title":
            card = render_title_card(
                title=seg["text"],
                author=seg.get("author", "Author"),
                score=seg.get("score", 0),
                subreddit=seg.get("subreddit", "korea"),
                card_width=card_width,
                font_path=font_path,
            )
        else:
            card = render_comment_card(
                body=seg["text"],
                author=seg.get("author", "Anonymous"),
                score=seg.get("score", 0),
                card_width=card_width,
                font_path=font_path,
            )

        card_path = os.path.join(output_dir, f"card_{i:02d}.png")
        card.save(card_path, "PNG")
        seg["card_path"] = card_path

    console.print(f"  [green]✓[/green] Rendered {len(segments)} card images")
    return segments
