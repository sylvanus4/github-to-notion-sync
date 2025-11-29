#!/usr/bin/env python3
"""
Daily Scrum synchronization script.
Collects yesterday and today's work data from GitHub Projects and creates
a summary page in Notion's DailyScrum page with per-person breakdown.
"""

import sys
import os
import asyncio
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)

# GitHub username to Notion display name mapping
GITHUB_TO_NOTION_NAME = {
    "duyeol-yu": "유두열",
    "jaehoonkim": "김재훈",
    "sylvanus4": "한효정",
    "thaki-yakhyo": "yakhyo",
    "thakicloud-jotaeyang": "조태양",
    "yunjae-park1111": "박윤재",
    "hwyncho-thakicloud": "조휘연",
    "chohongcheol-thakicloud": "조홍철",
    "jongmin-kim-thakicloud": "김종민",
    "thakicloud-chanwoo": "신찬우",
    "ryangkyung-thaki": "강량경",
    "mjhan-tk": "한민정",
}

# GitHub username to Notion User ID mapping
GITHUB_TO_NOTION_USER_ID = {
    "duyeol-yu": "229d872b-594c-8104-b58b-000212f60087",
    "jaehoonkim": "229d872b-594c-8150-879d-00022f27519e",
    "sylvanus4": "229d872b-594c-816d-ae7c-0002f11615c0",
    "thaki-yakhyo": "23ed872b-594c-811f-8e2f-0002687c8ce2",
    "thakicloud-jotaeyang": "229d872b-594c-81b5-906f-00020b52c301",
    "yunjae-park1111": "225d872b-594c-81ba-9e42-0002b46f091a",
    "hwyncho-thakicloud": "245d872b-594c-814c-9657-000222886921",
    "chohongcheol-thakicloud": "259d872b-594c-812e-9ea8-00028d08dc7d",
    "jongmin-kim-thakicloud": "26bd872b-594c-81f8-98df-000226f169c0",
    "thakicloud-chanwoo": "26bd872b-594c-81fe-885e-00026a54788b",
    "ryangkyung-thaki": "28bd872b-594c-81f1-8ff5-000283ca84b5",
    "mjhan-tk": "279d872b-594c-81cf-b503-0002c9451f49",
}


class DailyScrumSyncService:
    """Service for collecting daily work data and syncing to Notion DailyScrum page."""

    def __init__(self, notion_parent_id: str, days: int = 2, sprint_filter: Optional[str] = None):
        """Initialize daily scrum sync service.

        Args:
            notion_parent_id: Notion parent page ID for DailyScrum
            days: Number of days to look back (default: 2 for yesterday + today)
            sprint_filter: Optional sprint name to filter items
        """
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        self.notion_parent_id = notion_parent_id
        self.days = days
        self.sprint_filter = sprint_filter

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
        """Collect project items for the current sprint.

        Returns:
            List of GitHub project items
        """
        logger.info(f"Collecting project items{f' for sprint: {self.sprint_filter}' if self.sprint_filter else ''}...")

        try:
            items = self.github_service.get_all_project_items(sprint_filter=self.sprint_filter)
            logger.info(f"Found {len(items)} project items")
            return items
        except Exception as e:
            logger.error(f"Error collecting sprint items: {e}")
            return []

    async def collect_pr_reviews(self) -> List[Dict[str, Any]]:
        """Collect PR reviews for the date range.

        Returns:
            List of review data
        """
        logger.info(f"Collecting PR reviews from {self.start_date.date()} to {self.end_date.date()}...")

        try:
            reviews = self.github_service.get_all_organization_pr_reviews(self.start_date, self.end_date)
            logger.info(f"Found {len(reviews)} PR reviews")
            return reviews
        except Exception as e:
            logger.error(f"Error collecting PR reviews: {e}")
            return []

    def filter_items_by_date(self, items: List[Any]) -> List[Any]:
        """Filter items by date range (updated within the date range).

        Args:
            items: List of GitHub project items

        Returns:
            Filtered list of items
        """
        filtered = []
        for item in items:
            try:
                # Check updated_at
                updated_at = item.updated_at if hasattr(item, 'updated_at') else None
                if updated_at and updated_at >= self.start_date:
                    filtered.append(item)
                    continue

                # Also check created_at
                created_at = item.created_at if hasattr(item, 'created_at') else None
                if created_at and created_at >= self.start_date:
                    filtered.append(item)

            except Exception as e:
                logger.warning(f"Error filtering item {item.id}: {e}")
                continue

        logger.info(f"Filtered {len(filtered)} items from {len(items)} total (updated since {self.start_date.date()})")
        return filtered

    def collect_user_data(self, items: List[Any], reviews: List[Dict[str, Any]]) -> Dict[str, Dict[str, List]]:
        """Collect and organize data by user.

        Args:
            items: List of GitHub project items
            reviews: List of PR reviews

        Returns:
            Dictionary mapping username to their issues, PRs, and reviews
        """
        logger.info("Organizing data by user...")

        user_data = defaultdict(lambda: {"issues": [], "prs": [], "reviews": []})

        # Process project items (issues and PRs)
        for item in items:
            try:
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

                item_info = {
                    "title": title,
                    "number": number,
                    "url": url,
                    "status": status,
                    "type": item_type
                }

                if item_type == "ISSUE":
                    for assignee in assignees:
                        username = assignee.login if hasattr(assignee, 'login') else str(assignee)
                        user_data[username]["issues"].append(item_info)
                        self.stats["total_issues"] += 1

                elif item_type == "PULL_REQUEST":
                    # Get PR author
                    if hasattr(item, 'content') and item.content:
                        author = None
                        if hasattr(item.content, 'author') and item.content.author:
                            author = item.content.author.login
                        if author:
                            user_data[author]["prs"].append(item_info)
                            self.stats["total_prs"] += 1

            except Exception as e:
                logger.warning(f"Error processing item: {e}")
                continue

        # Process PR reviews
        for review in reviews:
            try:
                reviewer = review.get("reviewer")
                if not reviewer:
                    continue

                pr_info = review.get("pr", {})
                review_info = {
                    "pr_title": pr_info.get("title"),
                    "pr_number": pr_info.get("number"),
                    "pr_url": f"https://github.com/{pr_info.get('repository')}/pull/{pr_info.get('number')}",
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

    def build_notion_page_content(self, user_data: Dict[str, Dict[str, List]]) -> List[Dict[str, Any]]:
        """Build Notion page content blocks from user data.

        Args:
            user_data: Dictionary of user data

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

            # Issues section
            if data["issues"]:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"📋 이슈 ({len(data['issues'])})"}}]
                    }
                })

                for issue in data["issues"]:
                    issue_text = f"#{issue['number']} {issue['title']} [{issue['status']}]"
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": issue_text[:100],
                                    "link": {"url": issue['url']} if issue['url'] else None
                                }
                            }]
                        }
                    })

            # PRs section
            if data["prs"]:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"🔀 PR ({len(data['prs'])})"}}]
                    }
                })

                for pr in data["prs"]:
                    pr_text = f"#{pr['number']} {pr['title']} [{pr['status']}]"
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": pr_text[:100],
                                    "link": {"url": pr['url']} if pr['url'] else None
                                }
                            }]
                        }
                    })

            # Reviews section
            if data["reviews"]:
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"👀 리뷰 ({len(data['reviews'])})"}}]
                    }
                })

                # Group reviews by PR to avoid duplicates
                seen_prs = set()
                for review in data["reviews"]:
                    pr_key = f"{review['pr_number']}"
                    if pr_key in seen_prs:
                        continue
                    seen_prs.add(pr_key)

                    review_text = f"#{review['pr_number']} {review['pr_title']} ({review['state']})"
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": review_text[:100],
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

    def create_notion_page(self, user_data: Dict[str, Dict[str, List]], dry_run: bool = False) -> Optional[str]:
        """Create Notion page with daily scrum summary.

        Args:
            user_data: Dictionary of user data
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
            content_blocks = self.build_notion_page_content(user_data)

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

    async def run(self, dry_run: bool = False, output_file: Optional[str] = None) -> bool:
        """Run daily scrum sync.

        Args:
            dry_run: If True, only collect and display data without creating page
            output_file: Optional JSON file to save statistics

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

            # Step 4: Organize data by user
            user_data = self.collect_user_data(filtered_items, reviews)

            # Display summary
            logger.info("\n" + "=" * 60)
            logger.info(f"Daily Scrum Summary")
            logger.info(f"Period: {self.start_date.date()} to {self.end_date.date()}")
            logger.info(f"Total Issues: {self.stats['total_issues']}")
            logger.info(f"Total PRs: {self.stats['total_prs']}")
            logger.info(f"Total Reviews: {self.stats['total_reviews']}")
            logger.info(f"Active Users: {len(user_data)}")
            logger.info("=" * 60)

            # Display per-user summary
            logger.info("\nPer-user summary:")
            for username in sorted(user_data.keys()):
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
                        "active_users": len(user_data)
                    },
                    "user_data": {
                        username: {
                            "display_name": self.get_notion_display_name(username),
                            "issues": data["issues"],
                            "prs": data["prs"],
                            "reviews": data["reviews"]
                        }
                        for username, data in user_data.items()
                    }
                }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

                logger.info(f"\nData saved to: {output_file}")

            if dry_run:
                logger.info("\n[DRY RUN] Would create Notion page with above data")
                return True

            # Step 5: Create Notion page
            logger.info("\nCreating Notion page...")
            page_id = self.create_notion_page(user_data, dry_run=dry_run)

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
        description="Sync daily work data from GitHub to Notion DailyScrum page",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync yesterday and today's data to Notion
  python scripts/daily_scrum_sync.py --notion-parent-id 2ba9eddc34e6800cbb43c744a495df3f

  # Dry run (preview only)
  python scripts/daily_scrum_sync.py --notion-parent-id abc123 --dry-run

  # Last 3 days with sprint filter
  python scripts/daily_scrum_sync.py --notion-parent-id abc123 --days 3 --sprint "25-11-Sprint4"

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
        "--quiet",
        action="store_true",
        help="Suppress non-error output"
    )

    args = parser.parse_args()

    # Configure logging
    if args.quiet:
        logger.setLevel("WARNING")

    logger.info("Starting Daily Scrum sync script")

    try:
        # Initialize service
        sync_service = DailyScrumSyncService(
            notion_parent_id=args.notion_parent_id,
            days=args.days,
            sprint_filter=args.sprint
        )

        # Run sync
        success = await sync_service.run(
            dry_run=args.dry_run,
            output_file=args.output
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
