#!/usr/bin/env python3
"""
Sprint statistics collection and Notion sync script.
Collects user statistics (issues, PRs, reviews) for a sprint and syncs to Notion database.
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

import yaml

from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.utils.mapping import FieldMapper
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)


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


class SprintStatsService:
    """Service for collecting sprint statistics and syncing to Notion."""

    def __init__(self, sprint_name: str, notion_parent_id: Optional[str] = None):
        """Initialize sprint stats service.

        Args:
            sprint_name: Name of the sprint (e.g., "25-07-Sprint4")
            notion_parent_id: Optional parent page ID for database creation
        """
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        self.field_mapper = FieldMapper(self.config)
        self.sprint_name = sprint_name
        self.notion_parent_id = notion_parent_id
        self.notion_db_id = None

        # Track statistics
        self.stats = {
            "sprint_name": sprint_name,
            "start_time": None,
            "end_time": None,
            "total_users": 0,
            "total_issues": 0,
            "total_prs": 0,
            "total_reviews": 0,
            "user_stats": {}
        }

    def get_notion_display_name(self, github_username: str) -> str:
        """Convert GitHub username to Notion display name.

        Args:
            github_username: GitHub username

        Returns:
            Notion display name (Korean name if mapped, otherwise GitHub username)
        """
        return GITHUB_TO_NOTION_NAME.get(github_username, github_username)

    def get_notion_user_id(self, github_username: str) -> Optional[str]:
        """Convert GitHub username to Notion User ID.

        Args:
            github_username: GitHub username

        Returns:
            Notion User ID if mapped, otherwise None
        """
        return GITHUB_TO_NOTION_USER_ID.get(github_username)

    def get_sprint_date_range(self) -> Optional[tuple[datetime, datetime]]:
        """Get date range for the sprint from GitHub project.

        Returns:
            Tuple of (start_date, end_date) or None if not found
        """
        logger.info(f"Finding date range for sprint: {self.sprint_name}")

        try:
            # Get project fields to find sprint/iteration field
            fields = self.github_service.get_project_fields()

            # Debug: Log all field names to help identify the sprint field
            logger.debug(f"Available fields: {[field.name for field in fields]}")

            sprint_field = None
            # Try common field names for sprint/iteration
            sprint_field_names = ["스프린트", "Sprint", "Iteration"]

            for field in fields:
                if field.name in sprint_field_names:
                    logger.debug(f"Found potential sprint field: {field.name}")
                    logger.debug(f"Field type: {field.dataType if hasattr(field, 'dataType') else 'unknown'}")
                    logger.debug(f"Has configuration: {hasattr(field, 'configuration')}")
                    if hasattr(field, 'configuration') and field.configuration:
                        logger.debug(f"Configuration: {field.configuration}")
                        sprint_field = field
                        logger.info(f"Using sprint field: {field.name}")
                        break
                    else:
                        logger.warning(f"Field '{field.name}' found but has no configuration")
                        # Try to use it anyway for ITERATION type
                        if hasattr(field, 'dataType') and field.dataType.value == 'ITERATION':
                            sprint_field = field
                            logger.info(f"Using ITERATION field: {field.name} (without configuration check)")
                            break

            if not sprint_field:
                logger.error(f"Could not find sprint field. Available fields: {[f.name for f in fields]}")
                logger.error("Please check if the sprint field exists in your GitHub project")
                return None

            if not hasattr(sprint_field, 'configuration') or not sprint_field.configuration:
                logger.error(f"Sprint field '{sprint_field.name}' has no configuration")
                return None

            if not hasattr(sprint_field.configuration, 'iterations') or not sprint_field.configuration.iterations:
                logger.error(f"Sprint field '{sprint_field.name}' has no iterations")
                return None

            # Debug: Log available iterations
            available_sprints = [it.title for it in sprint_field.configuration.iterations]
            logger.debug(f"Available sprint iterations: {available_sprints}")

            # Find the matching sprint iteration
            for iteration in sprint_field.configuration.iterations:
                if iteration.title == self.sprint_name:
                    start_date = iteration.start_date
                    duration_days = iteration.duration
                    end_date = start_date + timedelta(days=duration_days)

                    logger.info(f"Sprint date range: {start_date.date()} to {end_date.date()}")
                    return (start_date, end_date)

            logger.error(f"Sprint '{self.sprint_name}' not found in iterations")
            logger.error(f"Available sprints: {available_sprints}")
            return None

        except Exception as e:
            logger.error(f"Error getting sprint date range: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def collect_sprint_items(self) -> List[Any]:
        """Collect all project items for the sprint.

        Returns:
            List of GitHub project items
        """
        logger.info(f"Collecting project items for sprint: {self.sprint_name}")

        try:
            # Use existing method with sprint filter
            items = self.github_service.get_all_project_items(sprint_filter=self.sprint_name)

            logger.info(f"Found {len(items)} items in sprint")
            return items

        except Exception as e:
            logger.error(f"Error collecting sprint items: {e}")
            return []

    async def collect_pr_reviews(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Collect PR reviews for the sprint period.

        Args:
            start_date: Sprint start date
            end_date: Sprint end date

        Returns:
            List of review data
        """
        logger.info(f"Collecting PR reviews from {start_date.date()} to {end_date.date()}")

        try:
            reviews = self.github_service.get_all_organization_pr_reviews(start_date, end_date)

            logger.info(f"Found {len(reviews)} reviews in sprint period")
            return reviews

        except Exception as e:
            logger.error(f"Error collecting PR reviews: {e}")
            return []

    def calculate_user_stats(self, sprint_items: List[Any], reviews: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """Calculate statistics per user.

        Args:
            sprint_items: List of sprint project items
            reviews: List of PR reviews

        Returns:
            Dictionary mapping username to stats (issues, prs, reviews)
        """
        logger.info("Calculating user statistics...")

        user_stats = defaultdict(lambda: {"issues": 0, "prs": 0, "reviews": 0})
        pr_keys = set()  # Track PRs to avoid duplicates (using repository + number as key)

        # Count issues and PRs from project items
        for item in sprint_items:
            try:
                # Get assignees for the item
                assignees = item.get_assignees() if hasattr(item, 'get_assignees') else []

                # Determine if it's an issue or PR
                item_type = item.type.value if hasattr(item.type, 'value') else str(item.type)

                if item_type == "ISSUE":
                    # Count as issue for each assignee
                    for assignee in assignees:
                        username = assignee.login if hasattr(assignee, 'login') else str(assignee)
                        user_stats[username]["issues"] += 1

                elif item_type == "PULL_REQUEST":
                    # Count as PR for the author
                    if hasattr(item, 'content') and item.content:
                        author = None
                        pr_number = None
                        repo_name = None

                        if hasattr(item.content, 'author') and item.content.author:
                            author = item.content.author.login

                        if hasattr(item.content, 'number'):
                            pr_number = item.content.number

                        if hasattr(item.content, 'repository') and item.content.repository:
                            repo_name = item.content.repository.full_name

                        if author:
                            user_stats[author]["prs"] += 1

                            # Track this PR to avoid counting it again
                            if repo_name and pr_number:
                                pr_key = f"{repo_name}#{pr_number}"
                                pr_keys.add(pr_key)
                                logger.debug(f"Added PR from project: {pr_key} by {author}")

            except Exception as e:
                logger.warning(f"Error processing item {item.id}: {e}")
                continue

        # Count PRs from Organization search results (from review data)
        # This catches PRs that aren't added to the project
        pr_authors_from_reviews = {}  # pr_key -> author
        for review in reviews:
            try:
                pr_info = review.get("pr", {})
                author = pr_info.get("author")
                pr_number = pr_info.get("number")
                repository = pr_info.get("repository")

                if author and pr_number and repository:
                    pr_key = f"{repository}#{pr_number}"

                    # Only count if we haven't seen this PR yet
                    if pr_key not in pr_keys:
                        # Track the author for this PR
                        if pr_key not in pr_authors_from_reviews:
                            pr_authors_from_reviews[pr_key] = author
                            pr_keys.add(pr_key)
                            logger.debug(f"Added PR from reviews: {pr_key} by {author}")

            except Exception as e:
                logger.warning(f"Error extracting PR info from review: {e}")
                continue

        # Add PR counts from review data
        for pr_key, author in pr_authors_from_reviews.items():
            user_stats[author]["prs"] += 1
            logger.debug(f"Counted PR for {author}: {pr_key}")

        # Count reviews
        for review in reviews:
            try:
                reviewer = review.get("reviewer")
                if reviewer:
                    user_stats[reviewer]["reviews"] += 1
            except Exception as e:
                logger.warning(f"Error processing review: {e}")
                continue

        # Update overall stats
        self.stats["total_users"] = len(user_stats)
        self.stats["total_issues"] = sum(stats["issues"] for stats in user_stats.values())
        self.stats["total_prs"] = sum(stats["prs"] for stats in user_stats.values())
        self.stats["total_reviews"] = sum(stats["reviews"] for stats in user_stats.values())
        self.stats["user_stats"] = dict(user_stats)

        logger.info(f"Statistics calculated for {len(user_stats)} users")
        logger.info(f"  Total Issues: {self.stats['total_issues']}")
        logger.info(f"  Total PRs: {self.stats['total_prs']}")
        logger.info(f"  Total Reviews: {self.stats['total_reviews']}")

        return dict(user_stats)

    def create_notion_database(self) -> Optional[str]:
        """Create Notion database for sprint statistics.

        Returns:
            Database ID or None if creation failed
        """
        logger.info("Creating Notion database for sprint statistics...")

        # Determine parent page ID
        parent_id = self.notion_parent_id
        if not parent_id:
            # Try to get from environment or use a default
            parent_id = os.getenv("NOTION_STATS_PARENT_ID")

        if not parent_id:
            logger.error("No parent page ID provided for database creation")
            logger.error("Please provide --notion-parent-id or set NOTION_STATS_PARENT_ID environment variable")
            return None

        # Define database schema with timestamp to ensure uniqueness
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        database_title = f"Sprint Statistics - {self.sprint_name} - {timestamp}"

        properties_schema = {
            "Sprint": {
                "title": {}
            },
            "User": {
                "people": {}
            },
            "Issues": {
                "number": {
                    "format": "number"
                }
            },
            "PRs": {
                "number": {
                    "format": "number"
                }
            },
            "Reviews": {
                "number": {
                    "format": "number"
                }
            },
            "Last Updated": {
                "date": {}
            }
        }

        try:
            database_id = self.notion_service.create_database(
                parent_page_id=parent_id,
                title=database_title,
                properties_schema=properties_schema
            )

            if database_id:
                self.notion_db_id = database_id
                logger.info(f"Created database: {database_id}")
                return database_id
            else:
                logger.error("Failed to create database")
                return None

        except Exception as e:
            logger.error(f"Error creating database: {e}")
            return None

    async def sync_stats_to_notion(self, user_stats: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        """Sync user statistics to Notion database.

        Args:
            user_stats: User statistics dictionary

        Returns:
            Dictionary with sync statistics
        """
        if not self.notion_db_id:
            logger.error("No Notion database ID set")
            return {"created": 0, "updated": 0, "failed": 0}

        logger.info(f"Syncing statistics to Notion database: {self.notion_db_id}")

        sync_stats = {
            "created": 0,
            "updated": 0,
            "failed": 0
        }

        current_time = datetime.now(timezone.utc).isoformat()

        for username, stats in user_stats.items():
            try:
                # Convert GitHub username to Notion display name and User ID
                notion_display_name = self.get_notion_display_name(username)
                notion_user_id = self.get_notion_user_id(username)

                # Build properties for this user's stats
                properties = {
                    "Sprint": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": f"{self.sprint_name} - {notion_display_name}"}
                            }
                        ]
                    },
                    "Issues": {
                        "number": stats["issues"]
                    },
                    "PRs": {
                        "number": stats["prs"]
                    },
                    "Reviews": {
                        "number": stats["reviews"]
                    },
                    "Last Updated": {
                        "date": {
                            "start": current_time
                        }
                    }
                }

                # Add User field - use people type if User ID is available
                if notion_user_id:
                    properties["User"] = {
                        "people": [
                            {
                                "id": notion_user_id
                            }
                        ]
                    }
                else:
                    # Fallback to rich_text if no User ID mapping exists
                    logger.warning(f"No Notion User ID found for {username}, using display name only")
                    properties["User"] = {
                        "people": []
                    }

                # Check if page already exists (using composite key: Sprint + User)
                # Use people filter if User ID is available
                if notion_user_id:
                    filters = [
                        {
                            "property": "User",
                            "people": {
                                "contains": notion_user_id
                            }
                        }
                    ]
                else:
                    # If no User ID, search by Sprint title (fallback)
                    filters = [
                        {
                            "property": "Sprint",
                            "title": {
                                "equals": f"{self.sprint_name} - {notion_display_name}"
                            }
                        }
                    ]

                existing_page = self.notion_service.find_page_by_composite_key(
                    self.notion_db_id,
                    filters
                )

                if existing_page:
                    # Update existing page
                    result = self.notion_service.update_page_properties(existing_page.id, properties)
                    if result:
                        sync_stats["updated"] += 1
                        logger.debug(f"Updated stats for user: {notion_display_name} ({username})")
                    else:
                        sync_stats["failed"] += 1
                        logger.warning(f"Failed to update stats for user: {notion_display_name} ({username})")
                else:
                    # Create new page
                    result = self.notion_service.create_page_in_database(self.notion_db_id, properties)
                    if result:
                        sync_stats["created"] += 1
                        logger.debug(f"Created stats for user: {notion_display_name} ({username})")
                    else:
                        sync_stats["failed"] += 1
                        logger.warning(f"Failed to create stats for user: {notion_display_name} ({username})")

                # Small delay to avoid rate limits
                await asyncio.sleep(0.3)

            except Exception as e:
                sync_stats["failed"] += 1
                logger.error(f"Error syncing stats for user {username}: {e}")

        logger.info(f"Sync completed: {sync_stats['created']} created, {sync_stats['updated']} updated, {sync_stats['failed']} failed")
        return sync_stats

    async def run(self, dry_run: bool = False, output_file: Optional[str] = None) -> bool:
        """Run sprint statistics collection and sync.

        Args:
            dry_run: If True, only collect and display stats without syncing
            output_file: Optional JSON file to save statistics

        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.now(timezone.utc)

        logger.info(f"Starting sprint statistics collection for: {self.sprint_name}")

        try:
            # Step 1: Get sprint date range
            date_range = self.get_sprint_date_range()
            if not date_range:
                logger.error("Could not determine sprint date range")
                return False

            start_date, end_date = date_range

            # Step 2: Collect sprint items
            sprint_items = await self.collect_sprint_items()
            if not sprint_items:
                logger.warning("No sprint items found")

            # Step 3: Collect PR reviews
            reviews = await self.collect_pr_reviews(start_date, end_date)

            # Step 4: Calculate user statistics
            user_stats = self.calculate_user_stats(sprint_items, reviews)

            if not user_stats:
                logger.warning("No user statistics calculated")

            # Display statistics
            logger.info("\n" + "="*60)
            logger.info(f"Sprint: {self.sprint_name}")
            logger.info(f"Period: {start_date.date()} to {end_date.date()}")
            logger.info(f"Total Users: {self.stats['total_users']}")
            logger.info(f"Total Issues: {self.stats['total_issues']}")
            logger.info(f"Total PRs: {self.stats['total_prs']}")
            logger.info(f"Total Reviews: {self.stats['total_reviews']}")
            logger.info("="*60)

            # Display per-user stats
            logger.info("\nUser Statistics:")
            for username, stats in sorted(user_stats.items()):
                notion_display_name = self.get_notion_display_name(username)
                logger.info(f"  {notion_display_name:20} ({username:25}) - Issues: {stats['issues']:3}, PRs: {stats['prs']:3}, Reviews: {stats['reviews']:3}")

            # Save to file if requested
            if output_file:
                output_data = {
                    "sprint": self.sprint_name,
                    "date_range": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "summary": {
                        "total_users": self.stats['total_users'],
                        "total_issues": self.stats['total_issues'],
                        "total_prs": self.stats['total_prs'],
                        "total_reviews": self.stats['total_reviews']
                    },
                    "user_stats": user_stats
                }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)

                logger.info(f"\nStatistics saved to: {output_file}")

            if dry_run:
                logger.info("\n[DRY RUN] Would sync statistics to Notion")
                return True

            # Step 5: Create Notion database
            logger.info("\nCreating Notion database...")
            database_id = self.create_notion_database()
            if not database_id:
                logger.error("Failed to create Notion database")
                return False

            # Step 6: Sync to Notion
            logger.info("\nSyncing statistics to Notion...")
            sync_result = await self.sync_stats_to_notion(user_stats)

            self.stats["end_time"] = datetime.now(timezone.utc)
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

            # Final summary
            logger.info("\n" + "="*60)
            logger.info("Sprint statistics collection completed!")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Notion Database ID: {database_id}")
            logger.info(f"Pages Created: {sync_result['created']}")
            logger.info(f"Pages Updated: {sync_result['updated']}")
            if sync_result['failed'] > 0:
                logger.warning(f"Failed: {sync_result['failed']}")
            logger.info("="*60)

            return sync_result['failed'] == 0

        except Exception as e:
            logger.error(f"Sprint stats collection failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main function for sprint stats script."""
    parser = argparse.ArgumentParser(
        description="Collect sprint statistics and sync to Notion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect stats and sync to Notion
  python scripts/sprint_stats.py --sprint "25-07-Sprint4" --notion-parent-id abc123

  # Dry run (preview only)
  python scripts/sprint_stats.py --sprint "25-07-Sprint4" --dry-run

  # Save to JSON file
  python scripts/sprint_stats.py --sprint "25-07-Sprint4" --output stats.json --dry-run
        """
    )

    parser.add_argument(
        "--sprint",
        required=True,
        help="Sprint name (e.g., '25-07-Sprint4')"
    )
    parser.add_argument(
        "--notion-parent-id",
        help="Notion parent page ID for database creation (or set NOTION_STATS_PARENT_ID env var)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Collect and display stats without syncing to Notion"
    )
    parser.add_argument(
        "--output",
        help="Save statistics to JSON file"
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

    logger.info("Starting sprint stats script")

    try:
        # Initialize service
        stats_service = SprintStatsService(
            sprint_name=args.sprint,
            notion_parent_id=args.notion_parent_id
        )

        # Run collection and sync
        success = await stats_service.run(
            dry_run=args.dry_run,
            output_file=args.output
        )

        if success:
            logger.info("Sprint stats script completed successfully")
            sys.exit(0)
        else:
            logger.error("Sprint stats script failed")
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
