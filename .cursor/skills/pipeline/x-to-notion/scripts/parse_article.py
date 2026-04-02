#!/usr/bin/env python3
"""Parse FxTwitter article JSON into structured Markdown.

Handles X Article block types: unstyled, header-two, ordered-list-item,
unordered-list-item, atomic. Supports inline styles (Bold, Italic),
entity types (LINK, MEDIA, MARKDOWN, DIVIDER, TWEET), and media lookups.

Usage:
    python parse_article.py <input.json> [output.md]
"""

import json
import sys
from pathlib import Path


def build_entity_lookup(entity_map_list: list) -> dict:
    return {str(e["key"]): e["value"] for e in entity_map_list}


def build_media_lookup(media_entities: list) -> dict:
    lookup = {}
    for me in media_entities:
        media_id = str(me.get("media_id", ""))
        info = me.get("media_info", {})
        typename = info.get("__typename", "")
        if typename == "ApiImage":
            lookup[media_id] = info.get("original_img_url", "")
        elif typename == "ApiVideo":
            preview = info.get("preview_image", {})
            lookup[media_id] = preview.get("original_img_url", "")
            for v in info.get("variants", []):
                if v.get("content_type") == "video/mp4":
                    lookup[f"{media_id}_video"] = v.get("url", "")
                    break
    return lookup


def _render_styled_segment(text: str, bold_flags: list, italic_flags: list) -> str:
    result = []
    n = len(text)
    i = 0
    while i < n:
        b, it = bold_flags[i], italic_flags[i]
        j = i
        while j < n and bold_flags[j] == b and italic_flags[j] == it:
            j += 1
        seg = text[i:j]
        if b and it:
            result.append(f"***{seg}***")
        elif b:
            result.append(f"**{seg}**")
        elif it:
            result.append(f"*{seg}*")
        else:
            result.append(seg)
        i = j
    return "".join(result)


def render_text(text: str, inline_styles: list, entity_ranges: list, entity_lookup: dict) -> str:
    if not text:
        return ""
    n = len(text)
    bold = [False] * n
    italic = [False] * n

    for style in inline_styles:
        start = style["offset"]
        end = min(start + style["length"], n)
        for i in range(start, end):
            if style["style"] == "Bold":
                bold[i] = True
            elif style["style"] == "Italic":
                italic[i] = True

    links = []
    for er in entity_ranges:
        entity = entity_lookup.get(str(er["key"]), {})
        if entity.get("type") == "LINK":
            url = entity.get("data", {}).get("url", "")
            links.append((er["offset"], er["offset"] + er["length"], url))
    links.sort()

    result = []
    i = 0
    link_idx = 0

    while i < n:
        if link_idx < len(links) and links[link_idx][0] == i:
            ls, le, lu = links[link_idx]
            link_text = _render_styled_segment(text[ls:le], bold[ls:le], italic[ls:le])
            result.append(f"[{link_text}]({lu})")
            i = le
            link_idx += 1
        else:
            seg_end = links[link_idx][0] if link_idx < len(links) else n
            result.append(_render_styled_segment(text[i:seg_end], bold[i:seg_end], italic[i:seg_end]))
            i = seg_end

    return "".join(result)


def render_atomic(entity: dict, media_lookup: dict) -> str:
    etype = entity.get("type", "")
    data = entity.get("data", {})

    if etype == "DIVIDER":
        return "---"

    if etype == "MARKDOWN":
        md = data.get("markdown", "")
        return md

    if etype == "MEDIA":
        caption = data.get("caption", "")
        parts = []
        for mi in data.get("mediaItems", []):
            mid = str(mi.get("mediaId", ""))
            url = media_lookup.get(mid, "")
            if not url:
                continue
            parts.append(f"![{caption}]({url})")
            video_url = media_lookup.get(f"{mid}_video")
            if video_url:
                parts.append(f"\n[▶ Video]({video_url})")
        return "\n".join(parts)

    if etype == "TWEET":
        tweet_id = data.get("tweetId", "")
        return f"> [Embedded Tweet](https://x.com/i/status/{tweet_id})"

    return ""


def parse_article(api_response: dict) -> str:
    tweet = api_response.get("tweet", {})
    article = tweet.get("article", {})
    author = tweet.get("author", {})
    content = article.get("content", {})
    blocks = content.get("blocks", [])
    entity_map_list = content.get("entityMap", [])
    media_entities = article.get("media_entities", [])

    entity_lookup = build_entity_lookup(entity_map_list)
    media_lookup = build_media_lookup(media_entities)

    lines = []

    title = article.get("title", "Untitled")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(
        f"**Author**: [{author.get('name', '')} (@{author.get('screen_name', '')})]"
        f"({author.get('url', '')})"
    )
    lines.append(f"**Published**: {article.get('created_at', '')}")
    lines.append(f"**Original**: {tweet.get('url', '')}")
    likes = tweet.get("likes", 0)
    rts = tweet.get("retweets", 0)
    views = tweet.get("views", 0)
    lines.append(f"**Engagement**: {likes:,} likes · {rts:,} retweets · {views:,} views")
    lines.append("")
    lines.append("---")
    lines.append("")

    ordered_counter = 0
    prev_was_list = False

    for block in blocks:
        btype = block.get("type", "unstyled")
        text = block.get("text", "")
        inline_styles = block.get("inlineStyleRanges", [])
        entity_ranges = block.get("entityRanges", [])

        if btype == "atomic":
            if prev_was_list:
                lines.append("")
                prev_was_list = False
            ordered_counter = 0
            if entity_ranges:
                key = str(entity_ranges[0]["key"])
                entity = entity_lookup.get(key, {})
                rendered = render_atomic(entity, media_lookup)
                if rendered:
                    lines.append(rendered)
                    lines.append("")
            continue

        rendered_text = render_text(text, inline_styles, entity_ranges, entity_lookup)

        if btype == "header-two":
            if prev_was_list:
                lines.append("")
                prev_was_list = False
            ordered_counter = 0
            lines.append(f"## {rendered_text}")
            lines.append("")

        elif btype == "unordered-list-item":
            ordered_counter = 0
            lines.append(f"- {rendered_text}")
            prev_was_list = True

        elif btype == "ordered-list-item":
            ordered_counter += 1
            lines.append(f"{ordered_counter}. {rendered_text}")
            prev_was_list = True

        elif btype == "unstyled":
            if prev_was_list:
                lines.append("")
                prev_was_list = False
            ordered_counter = 0
            if rendered_text.strip():
                lines.append(rendered_text)
                lines.append("")

    if prev_was_list:
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_article.py <input.json> [output.md]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    with open(input_path) as f:
        data = json.load(f)

    markdown = parse_article(data)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(markdown)
        print(f"Written to {output_path}", file=sys.stderr)
    else:
        print(markdown)
