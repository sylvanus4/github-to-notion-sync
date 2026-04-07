"""Reddit scraper using public .json endpoints (no API key required)."""

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests
from rich.console import Console

console = Console()

REDDIT_BASE = "https://www.reddit.com"
HEADERS = {
    "User-Agent": "RedditReactionMaker/1.0 (educational project)",
    "Accept": "application/json",
}


@dataclass
class Comment:
    id: str
    author: str
    body: str
    score: int


@dataclass
class RedditPost:
    id: str
    title: str
    body: str
    author: str
    score: int
    url: str
    subreddit: str
    comments: list[Comment] = field(default_factory=list)

    def all_text_segments(self) -> list[str]:
        segments = [self.title]
        if self.body and self.body.strip():
            segments.append(self.body)
        for c in self.comments:
            segments.append(c.body)
        return segments

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "author": self.author,
            "score": self.score,
            "url": self.url,
            "subreddit": self.subreddit,
            "comments": [
                {"id": c.id, "author": c.author, "body": c.body, "score": c.score}
                for c in self.comments
            ],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "RedditPost":
        return cls(
            id=d["id"],
            title=d["title"],
            body=d.get("body", ""),
            author=d.get("author", "Anonymous"),
            score=d.get("score", 0),
            url=d.get("url", ""),
            subreddit=d.get("subreddit", "korea"),
            comments=[
                Comment(
                    id=c["id"], author=c["author"], body=c["body"], score=c["score"]
                )
                for c in d.get("comments", [])
            ],
        )


class RedditScraper:
    def __init__(self, config: dict):
        self.subreddit = config.get("subreddit", "korea")
        self.post_limit = config.get("post_limit", 3)
        self.min_upvotes = config.get("min_upvotes", 50)
        self.min_comments_count = config.get("min_comments", 5)
        self.max_comment_length = config.get("max_comment_length", 300)
        self.top_comments = config.get("top_comments", 5)
        self._session = requests.Session()
        self._session.headers.update(HEADERS)
        self._session.verify = False
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _request_json(self, url: str, params: dict | None = None) -> dict | None:
        try:
            time.sleep(1.5)
            resp = self._session.get(url, params=params, timeout=15)
            if resp.status_code == 429:
                console.print("[yellow]Rate limited. Waiting 10s...[/yellow]")
                time.sleep(10)
                resp = self._session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            console.print(f"[red]Request error: {e}[/red]")
            return None

    def _parse_comments(self, comments_data: list) -> list[Comment]:
        comments: list[Comment] = []
        if not comments_data or len(comments_data) < 2:
            return comments

        listing = comments_data[1].get("data", {}).get("children", [])

        for child in listing[: self.top_comments * 2]:
            if child.get("kind") != "t1":
                continue
            data = child.get("data", {})
            body = data.get("body", "").strip()
            author = data.get("author", "Anonymous")

            if (
                body
                and body not in ("[deleted]", "[removed]")
                and len(body) <= self.max_comment_length
                and author not in ("[deleted]", "AutoModerator")
            ):
                comments.append(
                    Comment(
                        id=data.get("id", ""),
                        author=author,
                        body=body,
                        score=data.get("score", 0),
                    )
                )

            if len(comments) >= self.top_comments:
                break

        return comments

    def fetch_posts(self, time_filter: str = "week") -> list[RedditPost]:
        console.print(
            f"[cyan]Fetching posts from r/{self.subreddit} (public .json)...[/cyan]"
        )

        url = f"{REDDIT_BASE}/r/{self.subreddit}/top.json"
        params = {"t": time_filter, "limit": self.post_limit * 3}
        data = self._request_json(url, params)

        if not data:
            console.print("[red]Failed to fetch subreddit data.[/red]")
            return []

        posts: list[RedditPost] = []
        children = data.get("data", {}).get("children", [])

        for child in children:
            pd = child.get("data", {})
            post_id = pd.get("id", "")
            score = pd.get("score", 0)

            if score < self.min_upvotes:
                continue
            if pd.get("num_comments", 0) < self.min_comments_count:
                continue

            permalink = pd.get("permalink", "")
            if not permalink:
                continue

            comments_url = f"{REDDIT_BASE}{permalink}.json"
            comments_data = self._request_json(
                comments_url, {"sort": "top", "limit": self.top_comments * 2}
            )

            comments: list[Comment] = []
            if comments_data and isinstance(comments_data, list):
                comments = self._parse_comments(comments_data)

            if not comments:
                continue

            post = RedditPost(
                id=post_id,
                title=pd.get("title", ""),
                body=pd.get("selftext", ""),
                author=pd.get("author", "Anonymous"),
                score=score,
                url=pd.get("url", ""),
                subreddit=self.subreddit,
                comments=comments,
            )
            posts.append(post)
            console.print(
                f"  [green]✓[/green] {post.title[:60]}... "
                f"(+{score}, {len(comments)} comments)"
            )

            if len(posts) >= self.post_limit:
                break

        console.print(f"[cyan]Found {len(posts)} eligible posts.[/cyan]")
        return posts

    def save_posts(self, posts: list[RedditPost], output_path: str) -> str:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        data = {"posts": [p.to_dict() for p in posts]}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        console.print(f"  [green]✓[/green] Saved {len(posts)} posts → {output_path}")
        return output_path

    @staticmethod
    def load_posts(path: str) -> list[RedditPost]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [RedditPost.from_dict(p) for p in data.get("posts", [])]
