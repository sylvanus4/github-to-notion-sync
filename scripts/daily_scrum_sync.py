#!/usr/bin/env python3
"""
Daily Scrum synchronization script.
Collects yesterday and today's work data from GitHub Projects and creates
a summary page in Notion's DailyScrum page with per-person breakdown.
Includes AI-powered summaries using Claude API.
"""

import sys
import os
import asyncio
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yaml

from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)

# Claude API
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    logger.warning("anthropic package not installed. AI summaries will be disabled.")


def load_user_mappings() -> tuple[dict, dict]:
    """Load user mappings from config/field_mappings.yml.

    Returns:
        Tuple of (display_names, user_ids) dictionaries
    """
    config_path = Path(__file__).parent.parent / "config" / "field_mappings.yml"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        display_names = config.get("github_to_display_name", {})
        user_ids = config.get("github_to_notion", {}).get("assignees", {}).get("value_mappings", {})
        return display_names, user_ids
    except Exception as e:
        logger.warning(f"Failed to load user mappings from config: {e}")
        return {}, {}


# Load user mappings from config file
GITHUB_TO_NOTION_NAME, GITHUB_TO_NOTION_USER_ID = load_user_mappings()

# Bot users to ignore
BOT_USERS = {"coderabbitai", "dependabot[bot]", "github-actions[bot]"}


class DailyScrumSyncService:
    """Service for collecting daily work data and syncing to Notion DailyScrum page."""

    def __init__(self, notion_parent_id: str, days: int = 2, sprint_filter: Optional[str] = None,
                 anthropic_api_key: Optional[str] = None):
        """Initialize daily scrum sync service.

        Args:
            notion_parent_id: Notion parent page ID for DailyScrum
            days: Number of days to look back (default: 2 for yesterday + today)
            sprint_filter: Optional sprint name to filter items
            anthropic_api_key: Claude API key for AI summaries
        """
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        self.notion_parent_id = notion_parent_id
        self.days = days
        self.sprint_filter = sprint_filter

        # Claude API client
        self.anthropic_client = None
        if CLAUDE_AVAILABLE and anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
            logger.info("Claude API client initialized")

        # Calculate date range
        self.end_date = datetime.now(timezone.utc)
        self.start_date = self.end_date - timedelta(days=days - 1)
        # Set start of day for start_date
        self.start_date = self.start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Track statistics
        self.stats = {
            "start_time": None,
            "end_time": None,
            "date_range": {
                "start": self.start_date.isoformat(),
                "end": self.end_date.isoformat()
            },
            "total_issues": 0,
            "total_prs": 0,
            "total_reviews": 0,
            "users": {},
            "notion_page_id": None
        }

    def get_notion_display_name(self, github_username: str) -> str:
        """Convert GitHub username to Notion display name."""
        return GITHUB_TO_NOTION_NAME.get(github_username, github_username)

    def get_notion_user_id(self, github_username: str) -> Optional[str]:
        """Convert GitHub username to Notion User ID."""
        return GITHUB_TO_NOTION_USER_ID.get(github_username)

    async def collect_sprint_items(self) -> List[Any]:
        """Collect project items for the current sprint."""
        logger.info(f"Collecting project items{f' for sprint: {self.sprint_filter}' if self.sprint_filter else ''}...")

        try:
            items = self.github_service.get_all_project_items(sprint_filter=self.sprint_filter)
            logger.info(f"Found {len(items)} project items")
            return items
        except Exception as e:
            logger.error(f"Error collecting sprint items: {e}")
            return []

    async def collect_pr_reviews(self) -> List[Dict[str, Any]]:
        """Collect PR reviews for the date range."""
        logger.info(f"Collecting PR reviews from {self.start_date.date()} to {self.end_date.date()}...")

        try:
            reviews = self.github_service.get_all_organization_pr_reviews(self.start_date, self.end_date)
            logger.info(f"Found {len(reviews)} PR reviews")
            return reviews
        except Exception as e:
            logger.error(f"Error collecting PR reviews: {e}")
            return []

    def _parse_datetime(self, dt_value) -> Optional[datetime]:
        """Parse datetime from various formats."""
        if dt_value is None:
            return None
        if isinstance(dt_value, datetime):
            return dt_value
        if isinstance(dt_value, str):
            try:
                return datetime.fromisoformat(dt_value.replace("Z", "+00:00"))
            except Exception:
                return None
        return None

    def filter_items_by_date(self, items: List[Any]) -> List[Any]:
        """Filter items by date range (updated, created, closed, or merged within the date range).

        Args:
            items: List of GitHub project items

        Returns:
            Filtered list of items
        """
        filtered = []
        for item in items:
            try:
                # Check project item dates
                updated_at = self._parse_datetime(getattr(item, 'updated_at', None))
                created_at = self._parse_datetime(getattr(item, 'created_at', None))

                # Check content dates (actual issue/PR dates)
                content = getattr(item, 'content', None)
                content_created_at = None
                content_closed_at = None
                content_merged_at = None

                if content:
                    content_created_at = self._parse_datetime(getattr(content, 'created_at', None))
                    content_closed_at = self._parse_datetime(getattr(content, 'closed_at', None))
                    content_merged_at = self._parse_datetime(getattr(content, 'merged_at', None))

                # Check if any date is within range
                dates_to_check = [updated_at, created_at, content_created_at, content_closed_at, content_merged_at]

                for dt in dates_to_check:
                    if dt and dt >= self.start_date:
                        filtered.append(item)
                        break

            except Exception as e:
                logger.warning(f"Error filtering item {getattr(item, 'id', 'unknown')}: {e}")
                continue

        logger.info(f"Filtered {len(filtered)} items from {len(items)} total (activity since {self.start_date.date()})")
        return filtered

    def _extract_repo_info(self, url: str) -> Optional[Tuple[str, str, int]]:
        """Extract repository owner, name, and number from GitHub URL.

        Args:
            url: GitHub URL (e.g., https://github.com/owner/repo/issues/123)

        Returns:
            Tuple of (owner, repo_name, number) or None
        """
        if not url:
            return None
        try:
            parts = url.split('/')
            if len(parts) >= 7 and 'github.com' in url:
                owner = parts[3]
                repo = parts[4]
                number = int(parts[-1])
                return (owner, repo, number)
        except Exception:
            pass
        return None

    async def collect_item_details(self, items: List[Any]) -> Dict[str, Dict[str, Any]]:
        """Collect detailed information (body, comments) for each item.

        Args:
            items: List of GitHub project items

        Returns:
            Dictionary mapping item_id to details (body, comments)
        """
        logger.info("Collecting detailed information for items...")
        details = {}

        for item in items:
            try:
                item_id = getattr(item, 'id', None)
                if not item_id:
                    continue

                content = getattr(item, 'content', None)
                if not content:
                    continue

                url = item.get_url() if hasattr(item, 'get_url') else None
                repo_info = self._extract_repo_info(url)

                body = getattr(content, 'body', None) or ""
                comments = []

                # Get comments if we have repo info
                if repo_info:
                    owner, repo, number = repo_info
                    item_type = item.type.value if hasattr(item.type, 'value') else str(item.type)

                    try:
                        if item_type == "ISSUE":
                            gh_comments = self.github_service.get_issue_comments(owner, repo, number)
                        elif item_type == "PULL_REQUEST":
                            gh_comments = self.github_service.get_pull_request_comments(owner, repo, number)
                        else:
                            gh_comments = []

                        for c in gh_comments:
                            comment_body = getattr(c, 'body', '') or ""
                            comment_author = ""
                            if hasattr(c, 'author') and c.author:
                                comment_author = getattr(c.author, 'login', 'Unknown')
                            comments.append({
                                "author": comment_author,
                                "body": comment_body[:500]  # Truncate long comments
                            })
                    except Exception as e:
                        logger.warning(f"Failed to get comments for {url}: {e}")

                details[item_id] = {
                    "body": body[:2000] if body else "",  # Truncate long body
                    "comments": comments[:10]  # Limit comments
                }

            except Exception as e:
                logger.warning(f"Error collecting details for item: {e}")
                continue

        logger.info(f"Collected details for {len(details)} items")
        return details

    def collect_user_data(self, items: List[Any], reviews: List[Dict[str, Any]],
                          item_details: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, List]]:
        """Collect and organize data by user.

        Args:
            items: List of GitHub project items
            reviews: List of PR reviews
            item_details: Detailed information for each item

        Returns:
            Dictionary mapping username to their issues, PRs, and reviews
        """
        logger.info("Organizing data by user...")

        user_data = defaultdict(lambda: {"issues": [], "prs": [], "reviews": []})
        seen_prs = {}  # Track PRs by repo/number to avoid duplicates

        # Process project items (issues and PRs)
        for item in items:
            try:
                item_id = getattr(item, 'id', None)
                item_type = item.type.value if hasattr(item.type, 'value') else str(item.type)
                assignees = item.get_assignees() if hasattr(item, 'get_assignees') else []
                title = item.get_title() if hasattr(item, 'get_title') else "Unknown"
                url = item.get_url() if hasattr(item, 'get_url') else None
                number = item.get_number() if hasattr(item, 'get_number') else None

                # Get status from field values
                status = "Unknown"
                for field_value in getattr(item, 'field_values', []):
                    field_name = getattr(field_value.field, 'name', '')
                    if field_name == 'Status' and hasattr(field_value, 'name'):
                        status = field_value.name
                        break

                # Get body and comments
                details = item_details.get(item_id, {})
                body = details.get("body", "")
                comments = details.get("comments", [])

                item_info = {
                    "title": title,
                    "number": number,
                    "url": url,
                    "status": status,
                    "type": item_type,
                    "body": body,
                    "comments": comments
                }

                if item_type == "ISSUE":
                    for assignee in assignees:
                        username = assignee.login if hasattr(assignee, 'login') else str(assignee)
                        if username in BOT_USERS:
                            continue
                        user_data[username]["issues"].append(item_info)
                        self.stats["total_issues"] += 1

                elif item_type == "PULL_REQUEST":
                    # Get PR author from content
                    content = getattr(item, 'content', None)
                    author = None
                    if content and hasattr(content, 'author') and content.author:
                        author = content.author.login

                    if author and author not in BOT_USERS:
                        # Track this PR
                        repo_info = self._extract_repo_info(url)
                        if repo_info:
                            pr_key = f"{repo_info[0]}/{repo_info[1]}#{repo_info[2]}"
                            if pr_key not in seen_prs:
                                seen_prs[pr_key] = author
                                user_data[author]["prs"].append(item_info)
                                self.stats["total_prs"] += 1

            except Exception as e:
                logger.warning(f"Error processing item: {e}")
                continue

        # Process PR reviews - also extract PR author from review data
        for review in reviews:
            try:
                reviewer = review.get("reviewer")
                pr_info = review.get("pr", {})
                pr_author = pr_info.get("author")
                pr_number = pr_info.get("number")
                repository = pr_info.get("repository")
                pr_title = pr_info.get("title")

                # Add PR to author's list if not already tracked
                if pr_author and pr_author not in BOT_USERS and repository and pr_number:
                    pr_key = f"{repository}#{pr_number}"
                    if pr_key not in seen_prs:
                        seen_prs[pr_key] = pr_author
                        pr_url = f"https://github.com/{repository}/pull/{pr_number}"
                        user_data[pr_author]["prs"].append({
                            "title": pr_title,
                            "number": pr_number,
                            "url": pr_url,
                            "status": "Open" if not pr_info.get("mergedAt") else "Merged",
                            "type": "PULL_REQUEST",
                            "body": "",
                            "comments": []
                        })
                        self.stats["total_prs"] += 1

                # Add review to reviewer's list
                if reviewer and reviewer not in BOT_USERS:
                    review_info = {
                        "pr_title": pr_title,
                        "pr_number": pr_number,
                        "pr_url": f"https://github.com/{repository}/pull/{pr_number}" if repository else None,
                        "repository": repository,
                        "state": review.get("state"),
                        "submitted_at": review.get("submittedAt")
                    }

                    user_data[reviewer]["reviews"].append(review_info)
                    self.stats["total_reviews"] += 1

            except Exception as e:
                logger.warning(f"Error processing review: {e}")
                continue

        # Update stats
        self.stats["users"] = {
            username: {
                "issues": len(data["issues"]),
                "prs": len(data["prs"]),
                "reviews": len(data["reviews"])
            }
            for username, data in user_data.items()
        }

        logger.info(f"Collected data for {len(user_data)} users")
        return dict(user_data)

    def _extract_repo_name_from_url(self, url: str) -> str:
        """Extract repository name from GitHub URL."""
        if not url:
            return "Unknown"
        try:
            parts = url.split('/')
            if len(parts) >= 5 and 'github.com' in url:
                return parts[4]  # repo name
        except Exception:
            pass
        return "Unknown"

    async def summarize_user_work(self, username: str, data: Dict[str, List]) -> Dict[str, str]:
        """Generate AI summary of user's work using Claude.

        Args:
            username: GitHub username
            data: User's issues, PRs, and reviews data

        Returns:
            Dictionary with 'narrative' (3-5 sentence summary) and 'tree' (hierarchical task breakdown)
        """
        result = {"narrative": "", "tree": ""}

        if not self.anthropic_client:
            return result

        display_name = self.get_notion_display_name(username)

        # Build context from user data - group by repository
        context_parts = []

        if data["issues"]:
            context_parts.append("## 담당 이슈:")
            for issue in data["issues"]:
                repo_name = self._extract_repo_name_from_url(issue.get('url', ''))
                status = issue['status']
                # Determine if done (completed statuses)
                is_done = status.lower() in ['done', 'closed', 'merged', '완료', 'archived']
                context_parts.append(f"- [리포지토리: {repo_name}] #{issue['number']} {issue['title']} [상태: {status}] [완료여부: {'완료' if is_done else '진행중'}]")
                if issue.get('body'):
                    context_parts.append(f"  본문: {issue['body'][:300]}...")

        if data["prs"]:
            context_parts.append("\n## PR:")
            for pr in data["prs"]:
                repo_name = self._extract_repo_name_from_url(pr.get('url', ''))
                status = pr['status']
                is_done = status.lower() in ['done', 'closed', 'merged', '완료']
                context_parts.append(f"- [리포지토리: {repo_name}] #{pr['number']} {pr['title']} [상태: {status}] [완료여부: {'완료' if is_done else '진행중'}]")
                if pr.get('body'):
                    context_parts.append(f"  본문: {pr['body'][:300]}...")

        if data["reviews"]:
            context_parts.append("\n## 수행한 코드 리뷰:")
            seen_prs = set()
            for review in data["reviews"]:
                pr_key = f"{review.get('repository')}#{review['pr_number']}"
                if pr_key not in seen_prs:
                    seen_prs.add(pr_key)
                    repo_name = review.get('repository', 'Unknown').split('/')[-1] if review.get('repository') else 'Unknown'
                    context_parts.append(f"- [리포지토리: {repo_name}] #{review['pr_number']} {review['pr_title']} ({review['state']}) [완료여부: 완료]")

        if not context_parts:
            return result

        context = "\n".join(context_parts)

        prompt = f"""다음은 {display_name} (@{username})님의 어제와 오늘 GitHub 작업 내용입니다.

{context}

위 내용을 바탕으로 두 가지 형식으로 요약해주세요:

## 1. 서술형 요약
이 팀원의 작업을 3-5문장으로 간결하게 한글로 요약해주세요.
스크럼 미팅에서 발표할 수 있는 형식으로 작성해주세요.
기술적인 세부사항보다는 무엇을 하고 있는지, 진행 상황이 어떤지에 초점을 맞춰주세요.

## 2. 작업 트리 (계층 구조)
작업 내용을 **GitHub 리포지토리별**로 그룹화하고, **어제 한 일**과 **오늘 할 일**로 나눠서 정리해주세요.

분류 기준:
- 어제 한 일: 상태가 Done, Closed, Merged, 완료, Archived 등 완료된 작업
- 오늘 할 일: 상태가 In Progress, Open, 진행중 등 아직 완료되지 않은 작업

형식 (반드시 이 구조를 따르세요):
📌 어제 한 일
- [리포지토리명]
    - 완료된 작업 1 (완료)
    - 완료된 작업 2 (완료)

📋 오늘 할 일  
- [리포지토리명]
    - 진행중인 작업 1 (진행중)
    - 진행중인 작업 2 (PR 리뷰중)

중요:
- 리포지토리별로 묶어서 정리
- 각 작업에 상태 표시 (완료/진행중/PR 리뷰중 등)
- 중복 항목 제거
- 간결하게 핵심만 작성

반드시 아래 형식으로 응답해주세요:
---NARRATIVE---
(서술형 요약 내용)
---TREE---
(작업 트리 내용)"""

        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response_text = message.content[0].text

            # Parse response
            if "---NARRATIVE---" in response_text and "---TREE---" in response_text:
                parts = response_text.split("---TREE---")
                narrative_part = parts[0].replace("---NARRATIVE---", "").strip()
                tree_part = parts[1].strip() if len(parts) > 1 else ""
                result["narrative"] = narrative_part
                result["tree"] = tree_part
            else:
                # Fallback: treat entire response as narrative
                result["narrative"] = response_text

            return result
        except Exception as e:
            logger.warning(f"Failed to generate summary for {username}: {e}")
            return result

    def _parse_tree_to_notion_blocks(self, tree_text: str) -> List[Dict[str, Any]]:
        """Parse tree-formatted text into Notion bulleted list blocks.

        Args:
            tree_text: Tree-formatted text with indentation

        Returns:
            List of Notion block objects
        """
        blocks = []
        lines = tree_text.strip().split('\n')

        for line in lines:
            if not line.strip():
                continue

            # Count leading spaces/tabs to determine indent level
            stripped = line.lstrip()
            if not stripped.startswith('-'):
                continue

            # Remove the leading dash and space
            content = stripped[1:].strip() if stripped.startswith('-') else stripped

            # Create bulleted list item
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": content[:100]}}]
                }
            })

        return blocks

    def build_notion_page_content(self, user_data: Dict[str, Dict[str, List]],
                                   user_summaries: Dict[str, Dict[str, str]]) -> List[Dict[str, Any]]:
        """Build Notion page content blocks from user data.

        Args:
            user_data: Dictionary of user data
            user_summaries: AI-generated summaries per user (dict with 'narrative' and 'tree' keys)

        Returns:
            List of Notion block objects
        """
        blocks = []

        # Add summary header
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        blocks.append({
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": f"📅 Daily Scrum - {today_str}"}}]
            }
        })

        # Add date range info
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {
                    "content": f"기간: {self.start_date.strftime('%Y-%m-%d')} ~ {self.end_date.strftime('%Y-%m-%d')}"
                }}],
                "icon": {"emoji": "📆"}
            }
        })

        # Add summary statistics
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": f"총 이슈: {self.stats['total_issues']} | 총 PR: {self.stats['total_prs']} | 총 리뷰: {self.stats['total_reviews']}"}
                }]
            }
        })

        blocks.append({
            "object": "block",
            "type": "divider",
            "divider": {}
        })

        # Add per-user sections
        for username in sorted(user_data.keys()):
            if username in BOT_USERS:
                continue

            data = user_data[username]
            display_name = self.get_notion_display_name(username)

            # Skip users with no activity
            if not data["issues"] and not data["prs"] and not data["reviews"]:
                continue

            # User header
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": f"👤 {display_name} (@{username})"}}]
                }
            })

            # AI Summary section
            summary_data = user_summaries.get(username, {})
            narrative = summary_data.get("narrative", "") if isinstance(summary_data, dict) else summary_data
            tree = summary_data.get("tree", "") if isinstance(summary_data, dict) else ""

            # Narrative summary (callout)
            if narrative:
                blocks.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{"type": "text", "text": {"content": narrative}}],
                        "icon": {"emoji": "🤖"},
                        "color": "blue_background"
                    }
                })

            # Tree summary (toggle block with bulleted list)
            if tree:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "🌳 작업 트리"}}]
                    }
                })

                # Add tree as code block for better formatting
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": tree[:2000]}}],
                        "language": "plain text"
                    }
                })

            # Issues section - grouped by repository
            if data["issues"]:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"📋 이슈 ({len(data['issues'])})"}}]
                    }
                })

                # Group issues by repository
                issues_by_repo = defaultdict(list)
                for issue in data["issues"]:
                    repo_name = self._extract_repo_name_from_url(issue.get('url', ''))
                    issues_by_repo[repo_name].append(issue)

                for repo_name in sorted(issues_by_repo.keys()):
                    # Repository name as bullet
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": repo_name}, "annotations": {"bold": True}}]
                        }
                    })
                    # Issues under this repo as paragraph (indented visually)
                    for issue in issues_by_repo[repo_name]:
                        issue_text = f"#{issue['number']} {issue['title']} [{issue['status']}]"
                        blocks.append({
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {
                                        "content": f"  {issue_text[:95]}",
                                        "link": {"url": issue['url']} if issue['url'] else None
                                    }
                                }]
                            }
                        })

            # PRs section - grouped by repository
            if data["prs"]:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"🔀 PR ({len(data['prs'])})"}}]
                    }
                })

                # Group PRs by repository
                prs_by_repo = defaultdict(list)
                for pr in data["prs"]:
                    repo_name = self._extract_repo_name_from_url(pr.get('url', ''))
                    prs_by_repo[repo_name].append(pr)

                for repo_name in sorted(prs_by_repo.keys()):
                    # Repository name as bullet
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": repo_name}, "annotations": {"bold": True}}]
                        }
                    })
                    # PRs under this repo
                    for pr in prs_by_repo[repo_name]:
                        pr_text = f"#{pr['number']} {pr['title']} [{pr['status']}]"
                        blocks.append({
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {
                                        "content": f"  {pr_text[:95]}",
                                        "link": {"url": pr['url']} if pr['url'] else None
                                    }
                                }]
                            }
                        })

            # Reviews section - grouped by repository
            if data["reviews"]:
                # Deduplicate reviews first
                seen_prs = set()
                unique_reviews = []
                for review in data["reviews"]:
                    pr_key = f"{review.get('repository')}#{review['pr_number']}"
                    if pr_key not in seen_prs:
                        seen_prs.add(pr_key)
                        unique_reviews.append(review)

                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"👀 리뷰 ({len(unique_reviews)})"}}]
                    }
                })

                # Group reviews by repository
                reviews_by_repo = defaultdict(list)
                for review in unique_reviews:
                    repo_name = review.get('repository', 'Unknown').split('/')[-1] if review.get('repository') else 'Unknown'
                    reviews_by_repo[repo_name].append(review)

                for repo_name in sorted(reviews_by_repo.keys()):
                    # Repository name as bullet
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": repo_name}, "annotations": {"bold": True}}]
                        }
                    })
                    # Reviews under this repo
                    for review in reviews_by_repo[repo_name]:
                        review_text = f"#{review['pr_number']} {review['pr_title']} ({review['state']})"
                        blocks.append({
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {
                                        "content": f"  {review_text[:95]}",
                                        "link": {"url": review['pr_url']} if review['pr_url'] else None
                                    }
                                }]
                            }
                        })

            # Add divider between users
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })

        return blocks

    def create_notion_page(self, user_data: Dict[str, Dict[str, List]],
                           user_summaries: Dict[str, str],
                           dry_run: bool = False) -> Optional[str]:
        """Create Notion page with daily scrum summary.

        Args:
            user_data: Dictionary of user data
            user_summaries: AI-generated summaries per user
            dry_run: If True, don't actually create the page

        Returns:
            Page ID or None if creation failed
        """
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        page_title = f"Daily Scrum - {today_str}"

        logger.info(f"Creating Notion page: {page_title}")

        if dry_run:
            logger.info("[DRY RUN] Would create Notion page with title: " + page_title)
            return "dry-run-page-id"

        try:
            # Build page content
            content_blocks = self.build_notion_page_content(user_data, user_summaries)

            # Create page properties
            properties = {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": page_title}
                        }
                    ]
                }
            }

            # Create page under parent
            def _create_page():
                return self.notion_service.client.pages.create(
                    parent={"page_id": self.notion_parent_id},
                    properties=properties,
                    children=content_blocks[:100]  # Notion API limits to 100 blocks per request
                )

            response = self.notion_service._handle_rate_limit(_create_page)
            page_id = response["id"]

            # If there are more blocks, append them
            if len(content_blocks) > 100:
                remaining_blocks = content_blocks[100:]
                for i in range(0, len(remaining_blocks), 100):
                    batch = remaining_blocks[i:i + 100]

                    def _append_blocks():
                        return self.notion_service.client.blocks.children.append(
                            block_id=page_id,
                            children=batch
                        )

                    self.notion_service._handle_rate_limit(_append_blocks)

            logger.info(f"Created Notion page: {page_id}")
            self.stats["notion_page_id"] = page_id

            return page_id

        except Exception as e:
            logger.error(f"Error creating Notion page: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def run(self, dry_run: bool = False, output_file: Optional[str] = None,
                  skip_details: bool = False, skip_summary: bool = False) -> bool:
        """Run daily scrum sync.

        Args:
            dry_run: If True, only collect and display data without creating page
            output_file: Optional JSON file to save statistics
            skip_details: Skip collecting body/comments (faster)
            skip_summary: Skip AI summary generation

        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.now(timezone.utc)

        logger.info(f"Starting Daily Scrum sync for {self.start_date.date()} to {self.end_date.date()}")
        if self.sprint_filter:
            logger.info(f"Sprint filter: {self.sprint_filter}")

        try:
            # Step 1: Collect sprint items
            items = await self.collect_sprint_items()

            # Step 2: Filter items by date
            filtered_items = self.filter_items_by_date(items)

            # Step 3: Collect PR reviews
            reviews = await self.collect_pr_reviews()

            # Step 4: Collect item details (body, comments)
            item_details = {}
            if not skip_details:
                item_details = await self.collect_item_details(filtered_items)

            # Step 5: Organize data by user
            user_data = self.collect_user_data(filtered_items, reviews, item_details)

            # Step 6: Generate AI summaries
            user_summaries = {}
            if not skip_summary and self.anthropic_client:
                logger.info("Generating AI summaries...")
                for username in user_data.keys():
                    if username in BOT_USERS:
                        continue
                    data = user_data[username]
                    if data["issues"] or data["prs"] or data["reviews"]:
                        summary = await self.summarize_user_work(username, data)
                        if summary.get("narrative") or summary.get("tree"):
                            user_summaries[username] = summary
                            logger.info(f"Generated summary for {username}")
                logger.info(f"Generated {len(user_summaries)} summaries")

            # Display summary
            logger.info("\n" + "=" * 60)
            logger.info(f"Daily Scrum Summary")
            logger.info(f"Period: {self.start_date.date()} to {self.end_date.date()}")
            logger.info(f"Total Issues: {self.stats['total_issues']}")
            logger.info(f"Total PRs: {self.stats['total_prs']}")
            logger.info(f"Total Reviews: {self.stats['total_reviews']}")
            logger.info(f"Active Users: {len([u for u in user_data.keys() if u not in BOT_USERS])}")
            logger.info("=" * 60)

            # Display per-user summary
            logger.info("\nPer-user summary:")
            for username in sorted(user_data.keys()):
                if username in BOT_USERS:
                    continue
                data = user_data[username]
                display_name = self.get_notion_display_name(username)
                logger.info(f"  {display_name:20} (@{username:25}) - Issues: {len(data['issues']):3}, PRs: {len(data['prs']):3}, Reviews: {len(data['reviews']):3}")

            # Save to file if requested
            if output_file:
                output_data = {
                    "date_range": {
                        "start": self.start_date.isoformat(),
                        "end": self.end_date.isoformat()
                    },
                    "summary": {
                        "total_issues": self.stats['total_issues'],
                        "total_prs": self.stats['total_prs'],
                        "total_reviews": self.stats['total_reviews'],
                        "active_users": len([u for u in user_data.keys() if u not in BOT_USERS])
                    },
                    "user_data": {
                        username: {
                            "display_name": self.get_notion_display_name(username),
                            "issues": data["issues"],
                            "prs": data["prs"],
                            "reviews": data["reviews"],
                            "ai_summary": user_summaries.get(username, {})
                        }
                        for username, data in user_data.items()
                        if username not in BOT_USERS
                    }
                }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

                logger.info(f"\nData saved to: {output_file}")

            if dry_run:
                logger.info("\n[DRY RUN] Would create Notion page with above data")
                if user_summaries:
                    logger.info("\nAI Summaries:")
                    for username, summary_data in user_summaries.items():
                        display_name = self.get_notion_display_name(username)
                        narrative = summary_data.get("narrative", "") if isinstance(summary_data, dict) else summary_data
                        tree = summary_data.get("tree", "") if isinstance(summary_data, dict) else ""
                        logger.info(f"\n{display_name} (@{username}):")
                        logger.info(f"[서술형 요약]\n{narrative}")
                        if tree:
                            logger.info(f"\n[작업 트리]\n{tree}")
                return True

            # Step 7: Create Notion page
            logger.info("\nCreating Notion page...")
            page_id = self.create_notion_page(user_data, user_summaries, dry_run=dry_run)

            if not page_id:
                logger.error("Failed to create Notion page")
                return False

            self.stats["end_time"] = datetime.now(timezone.utc)
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

            # Final summary
            logger.info("\n" + "=" * 60)
            logger.info("Daily Scrum sync completed!")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Notion Page ID: {page_id}")
            logger.info("=" * 60)

            return True

        except Exception as e:
            logger.error(f"Daily Scrum sync failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main function for daily scrum sync script."""
    parser = argparse.ArgumentParser(
        description="Sync daily work data from GitHub to Notion DailyScrum page with AI summaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync yesterday and today's data to Notion with AI summaries
  python scripts/daily_scrum_sync.py --notion-parent-id 2ba9eddc34e6800cbb43c744a495df3f

  # Dry run (preview only)
  python scripts/daily_scrum_sync.py --notion-parent-id abc123 --dry-run

  # Last 3 days with sprint filter
  python scripts/daily_scrum_sync.py --notion-parent-id abc123 --days 3 --sprint "25-11-Sprint4"

  # Fast mode (skip details and AI summary)
  python scripts/daily_scrum_sync.py --notion-parent-id abc123 --skip-details --skip-summary

  # Save to JSON file
  python scripts/daily_scrum_sync.py --notion-parent-id abc123 --output daily_scrum.json --dry-run
        """
    )

    parser.add_argument(
        "--notion-parent-id",
        required=True,
        help="Notion parent page ID for DailyScrum page"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=2,
        help="Number of days to look back (default: 2 for yesterday + today)"
    )
    parser.add_argument(
        "--sprint",
        help="Sprint name to filter items (e.g., '25-11-Sprint4')"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Collect and display data without creating Notion page"
    )
    parser.add_argument(
        "--output",
        help="Save data to JSON file"
    )
    parser.add_argument(
        "--skip-details",
        action="store_true",
        help="Skip collecting body/comments (faster)"
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="Skip AI summary generation"
    )
    parser.add_argument(
        "--anthropic-api-key",
        help="Claude API key (or set ANTHROPIC_API_KEY env var)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output"
    )

    args = parser.parse_args()

    # Configure logging
    if args.quiet:
        logger.setLevel("WARNING")

    # Get API key
    anthropic_api_key = args.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

    logger.info("Starting Daily Scrum sync script")

    try:
        # Initialize service
        sync_service = DailyScrumSyncService(
            notion_parent_id=args.notion_parent_id,
            days=args.days,
            sprint_filter=args.sprint,
            anthropic_api_key=anthropic_api_key
        )

        # Run sync
        success = await sync_service.run(
            dry_run=args.dry_run,
            output_file=args.output,
            skip_details=args.skip_details,
            skip_summary=args.skip_summary
        )

        if success:
            logger.info("Daily Scrum sync script completed successfully")
            sys.exit(0)
        else:
            logger.error("Daily Scrum sync script failed")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_with_config():
    """Run script with configuration validation."""
    try:
        config = get_config()
        logger.info("Configuration loaded successfully")

        # Run the async main function
        asyncio.run(main())

    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_with_config()
