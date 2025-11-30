#!/usr/bin/env python3
"""
Sprint PR review status check script.
Collects PRs for a sprint and checks their review status, syncing to Notion database.
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

# Bot reviewers to ignore when checking review status
# Format: repository_pattern -> list of bot reviewer usernames
# Supports exact match or glob patterns (use * for wildcard)
BOT_REVIEWERS_TO_IGNORE = {
    "ThakiCloud/ai-platform-webui": ["coderabbitai"],
    # Add more repositories as needed:
    # "ThakiCloud/*": ["dependabot[bot]", "github-actions[bot]"],
    # "*": ["renovate[bot]"],  # Global ignore
}


class SprintPRReviewService:
    """Service for collecting sprint PR review status and syncing to Notion."""

    def __init__(self, sprint_name: str, notion_parent_id: Optional[str] = None):
        """Initialize sprint PR review service.

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
            "total_prs": 0,
            "reviewed_prs": 0,
            "not_reviewed_prs": 0,
            "pr_details": []
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

    def is_bot_reviewer(self, reviewer: str, repository: str) -> bool:
        """Check if a reviewer should be ignored (is a bot) for the given repository.

        Args:
            reviewer: Reviewer username
            repository: Repository name (e.g., "ThakiCloud/ai-platform-webui")

        Returns:
            True if the reviewer should be ignored
        """
        # Check exact match first
        if repository in BOT_REVIEWERS_TO_IGNORE:
            if reviewer in BOT_REVIEWERS_TO_IGNORE[repository]:
                return True

        # Check wildcard patterns
        import fnmatch
        for pattern, bot_reviewers in BOT_REVIEWERS_TO_IGNORE.items():
            if fnmatch.fnmatch(repository, pattern):
                if reviewer in bot_reviewers:
                    return True

        return False

    def get_valid_reviews(self, reviews: List[Dict[str, Any]], repository: str) -> List[Dict[str, Any]]:
        """Filter out bot reviewers from the reviews list.

        Args:
            reviews: List of review dictionaries
            repository: Repository name

        Returns:
            List of valid (non-bot) reviews
        """
        valid_reviews = []
        for review in reviews:
            reviewer = review.get("reviewer")
            if reviewer and not self.is_bot_reviewer(reviewer, repository):
                valid_reviews.append(review)
        return valid_reviews

    def get_sprint_date_range(self) -> Optional[tuple[datetime, datetime]]:
        """Get date range for the sprint from GitHub project.

        Returns:
            Tuple of (start_date, end_date) or None if not found
        """
        logger.info(f"Finding date range for sprint: {self.sprint_name}")

        try:
            # Get project fields to find sprint/iteration field
            fields = self.github_service.get_project_fields()

            sprint_field = None
            # Try common field names for sprint/iteration
            sprint_field_names = ["스프린트", "Sprint", "Iteration"]

            for field in fields:
                if field.name in sprint_field_names:
                    if hasattr(field, 'configuration') and field.configuration:
                        sprint_field = field
                        logger.info(f"Using sprint field: {field.name}")
                        break
                    elif hasattr(field, 'dataType') and field.dataType.value == 'ITERATION':
                        sprint_field = field
                        logger.info(f"Using ITERATION field: {field.name}")
                        break

            if not sprint_field:
                logger.error(f"Could not find sprint field. Available fields: {[f.name for f in fields]}")
                return None

            if not hasattr(sprint_field, 'configuration') or not sprint_field.configuration:
                logger.error(f"Sprint field '{sprint_field.name}' has no configuration")
                return None

            # Get all iterations (active + completed)
            active_iterations = getattr(sprint_field.configuration, 'iterations', []) or []
            completed_iterations = getattr(sprint_field.configuration, 'completed_iterations', []) or []
            all_iterations = active_iterations + completed_iterations

            if not all_iterations:
                logger.error(f"Sprint field '{sprint_field.name}' has no iterations")
                return None

            # Find the matching sprint iteration
            for iteration in all_iterations:
                if iteration.title == self.sprint_name:
                    start_date = iteration.start_date
                    duration_days = iteration.duration
                    end_date = start_date + timedelta(days=duration_days)

                    logger.info(f"Sprint date range: {start_date.date()} to {end_date.date()}")
                    return (start_date, end_date)

            available_sprints = [it.title for it in all_iterations]
            logger.error(f"Sprint '{self.sprint_name}' not found in iterations")
            logger.error(f"Available sprints (active + completed): {available_sprints}")
            return None

        except Exception as e:
            logger.error(f"Error getting sprint date range: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def collect_sprint_prs(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Collect all PRs for the sprint period.

        Args:
            start_date: Sprint start date
            end_date: Sprint end date

        Returns:
            List of PR data with review information
        """
        logger.info(f"Collecting PRs from {start_date.date()} to {end_date.date()}")

        try:
            # Get all PRs from organization search
            reviews_data = self.github_service.get_all_organization_pr_reviews(start_date, end_date)

            # Process PRs and group by PR
            pr_map = {}  # pr_key -> pr_info

            for review_data in reviews_data:
                pr_info = review_data.get("pr", {})
                pr_number = pr_info.get("number")
                pr_repository = pr_info.get("repository")

                if not pr_number or not pr_repository:
                    continue

                pr_key = f"{pr_repository}#{pr_number}"

                # Initialize PR entry if not exists
                if pr_key not in pr_map:
                    pr_map[pr_key] = {
                        "number": pr_number,
                        "title": pr_info.get("title"),
                        "author": pr_info.get("author"),
                        "repository": pr_repository,
                        "created_at": pr_info.get("createdAt"),
                        "merged_at": pr_info.get("mergedAt"),
                        "reviews": [],
                        "has_reviews": False
                    }

                # Add review info
                reviewer = review_data.get("reviewer")
                review_state = review_data.get("state")
                submitted_at = review_data.get("submittedAt")

                if reviewer and review_state:
                    pr_map[pr_key]["reviews"].append({
                        "reviewer": reviewer,
                        "state": review_state,
                        "submitted_at": submitted_at
                    })

            # Filter bot reviewers and update has_reviews status
            for pr_key, pr_data in pr_map.items():
                repository = pr_data["repository"]
                all_reviews = pr_data["reviews"]

                # Filter out bot reviewers
                valid_reviews = self.get_valid_reviews(all_reviews, repository)

                # Update PR data
                pr_data["all_reviews"] = all_reviews  # Keep all reviews for reference
                pr_data["reviews"] = valid_reviews  # Only valid reviews
                pr_data["has_reviews"] = len(valid_reviews) > 0

                logger.debug(f"PR {pr_key}: {len(all_reviews)} total reviews, {len(valid_reviews)} valid reviews")

            # Convert to list and sort by Repository -> Not Reviewed -> Date
            prs_list = list(pr_map.values())
            prs_list.sort(key=lambda x: (
                x["repository"],  # First by repository
                x["has_reviews"],  # Then by review status (False = not reviewed comes first)
                x["created_at"] if x["created_at"] else ""  # Finally by date
            ))

            logger.info(f"Found {len(prs_list)} PRs in sprint period")

            return prs_list

        except Exception as e:
            logger.error(f"Error collecting sprint PRs: {e}")
            import traceback
            traceback.print_exc()
            return []

    def create_notion_database(self) -> Optional[str]:
        """Create Notion database for PR review status.

        Returns:
            Database ID or None if creation failed
        """
        logger.info("Creating Notion database for PR review status...")

        # Determine parent page ID
        parent_id = self.notion_parent_id
        if not parent_id:
            parent_id = os.getenv("NOTION_STATS_PARENT_ID")

        if not parent_id:
            logger.error("No parent page ID provided for database creation")
            logger.error("Please provide --notion-parent-id or set NOTION_STATS_PARENT_ID environment variable")
            return None

        # Define database schema
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        database_title = f"PR Review Status - {self.sprint_name} - {timestamp}"

        properties_schema = {
            "PR": {
                "title": {}
            },
            "Author": {
                "people": {}
            },
            "Repository": {
                "rich_text": {}
            },
            "Reviewed": {
                "checkbox": {}
            },
            "Review Count": {
                "number": {
                    "format": "number"
                }
            },
            "Reviewers": {
                "multi_select": {}
            },
            "Created At": {
                "date": {}
            },
            "PR URL": {
                "url": {}
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
            import traceback
            traceback.print_exc()
            return None

    async def sync_prs_to_notion(self, prs: List[Dict[str, Any]]) -> Dict[str, int]:
        """Sync PR review status to Notion database.

        Args:
            prs: List of PR data

        Returns:
            Dictionary with sync statistics
        """
        if not self.notion_db_id:
            logger.error("No Notion database ID set")
            return {"created": 0, "updated": 0, "failed": 0}

        logger.info(f"Syncing {len(prs)} PRs to Notion database: {self.notion_db_id}")

        sync_stats = {
            "created": 0,
            "updated": 0,
            "failed": 0
        }

        current_time = datetime.now(timezone.utc).isoformat()

        for pr in prs:
            try:
                # Get author info
                author_username = pr.get("author")
                author_user_id = self.get_notion_user_id(author_username) if author_username else None

                # Get reviewers
                reviewers = pr.get("reviews", [])
                reviewer_names = list(set([r["reviewer"] for r in reviewers if r.get("reviewer")]))

                # Build PR URL
                repo = pr.get("repository", "")
                pr_number = pr.get("number")
                pr_url = f"https://github.com/{repo}/pull/{pr_number}" if repo and pr_number else None

                # Build properties
                properties = {
                    "PR": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": f"#{pr_number} {pr.get('title', 'Untitled')}"[:100]}
                            }
                        ]
                    },
                    "Repository": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": repo}
                            }
                        ]
                    },
                    "Reviewed": {
                        "checkbox": pr.get("has_reviews", False)
                    },
                    "Review Count": {
                        "number": len(reviewers)
                    },
                    "Reviewers": {
                        "multi_select": [{"name": name} for name in reviewer_names[:10]]  # Limit to 10
                    },
                    "Last Updated": {
                        "date": {
                            "start": current_time
                        }
                    }
                }

                # Add author if available
                if author_user_id:
                    properties["Author"] = {
                        "people": [{"id": author_user_id}]
                    }
                else:
                    properties["Author"] = {
                        "people": []
                    }

                # Add created at
                if pr.get("created_at"):
                    properties["Created At"] = {
                        "date": {
                            "start": pr["created_at"]
                        }
                    }

                # Add PR URL
                if pr_url:
                    properties["PR URL"] = {
                        "url": pr_url
                    }

                # Check if page already exists (by PR number and repository)
                filters = [
                    {
                        "property": "PR",
                        "title": {
                            "contains": f"#{pr_number}"
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
                        logger.debug(f"Updated PR: {repo}#{pr_number}")
                    else:
                        sync_stats["failed"] += 1
                        logger.warning(f"Failed to update PR: {repo}#{pr_number}")
                else:
                    # Create new page
                    result = self.notion_service.create_page_in_database(self.notion_db_id, properties)
                    if result:
                        sync_stats["created"] += 1
                        logger.debug(f"Created PR: {repo}#{pr_number}")
                    else:
                        sync_stats["failed"] += 1
                        logger.warning(f"Failed to create PR: {repo}#{pr_number}")

                # Small delay to avoid rate limits
                await asyncio.sleep(0.3)

            except Exception as e:
                sync_stats["failed"] += 1
                logger.error(f"Error syncing PR {pr.get('number')}: {e}")

        logger.info(f"Sync completed: {sync_stats['created']} created, {sync_stats['updated']} updated, {sync_stats['failed']} failed")
        return sync_stats

    async def run(self, dry_run: bool = False, output_file: Optional[str] = None) -> bool:
        """Run sprint PR review check and sync.

        Args:
            dry_run: If True, only collect and display stats without syncing
            output_file: Optional JSON file to save statistics

        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.now(timezone.utc)

        logger.info(f"Starting sprint PR review check for: {self.sprint_name}")

        try:
            # Step 1: Get sprint date range
            date_range = self.get_sprint_date_range()
            if not date_range:
                logger.error("Could not determine sprint date range")
                return False

            start_date, end_date = date_range

            # Step 2: Collect sprint PRs with review status
            prs = await self.collect_sprint_prs(start_date, end_date)

            if not prs:
                logger.warning("No PRs found in sprint period")

            # Update statistics
            self.stats["total_prs"] = len(prs)
            self.stats["reviewed_prs"] = sum(1 for pr in prs if pr["has_reviews"])
            self.stats["not_reviewed_prs"] = sum(1 for pr in prs if not pr["has_reviews"])
            self.stats["pr_details"] = prs

            # Display statistics
            logger.info("\n" + "="*60)
            logger.info(f"Sprint: {self.sprint_name}")
            logger.info(f"Period: {start_date.date()} to {end_date.date()}")
            logger.info(f"Total PRs: {self.stats['total_prs']}")
            logger.info(f"Reviewed PRs: {self.stats['reviewed_prs']}")
            logger.info(f"Not Reviewed PRs: {self.stats['not_reviewed_prs']}")
            logger.info("="*60)

            # Display PR details
            logger.info("\nPR Review Status (Not Reviewed First):")
            for pr in prs:
                status = "✅ Reviewed" if pr["has_reviews"] else "❌ Not Reviewed"
                review_count = len(pr["reviews"])
                logger.info(f"  {status} - {pr['repository']}#{pr['number']} - {pr['title'][:50]} ({review_count} reviews)")

            # Save to file if requested
            if output_file:
                output_data = {
                    "sprint": self.sprint_name,
                    "date_range": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    },
                    "summary": {
                        "total_prs": self.stats['total_prs'],
                        "reviewed_prs": self.stats['reviewed_prs'],
                        "not_reviewed_prs": self.stats['not_reviewed_prs']
                    },
                    "prs": prs
                }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)

                logger.info(f"\nPR review status saved to: {output_file}")

            if dry_run:
                logger.info("\n[DRY RUN] Would sync PR status to Notion")
                return True

            # Step 3: Create Notion database
            logger.info("\nCreating Notion database...")
            database_id = self.create_notion_database()
            if not database_id:
                logger.error("Failed to create Notion database")
                return False

            # Step 4: Sync to Notion
            logger.info("\nSyncing PR status to Notion...")
            sync_result = await self.sync_prs_to_notion(prs)

            self.stats["end_time"] = datetime.now(timezone.utc)
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

            # Final summary
            logger.info("\n" + "="*60)
            logger.info("Sprint PR review check completed!")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Notion Database ID: {database_id}")
            logger.info(f"Pages Created: {sync_result['created']}")
            logger.info(f"Pages Updated: {sync_result['updated']}")
            if sync_result['failed'] > 0:
                logger.warning(f"Failed: {sync_result['failed']}")
            logger.info("="*60)

            return sync_result['failed'] == 0

        except Exception as e:
            logger.error(f"Sprint PR review check failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main function for sprint PR review check script."""
    parser = argparse.ArgumentParser(
        description="Check sprint PR review status and sync to Notion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check PR review status and sync to Notion
  python scripts/sprint_pr_review_check.py --sprint "25-07-Sprint4" --notion-parent-id abc123

  # Dry run (preview only)
  python scripts/sprint_pr_review_check.py --sprint "25-07-Sprint4" --dry-run

  # Save to JSON file
  python scripts/sprint_pr_review_check.py --sprint "25-07-Sprint4" --output pr_status.json --dry-run
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
        help="Collect and display PR status without syncing to Notion"
    )
    parser.add_argument(
        "--output",
        help="Save PR review status to JSON file"
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

    logger.info("Starting sprint PR review check script")

    try:
        # Initialize service
        review_service = SprintPRReviewService(
            sprint_name=args.sprint,
            notion_parent_id=args.notion_parent_id
        )

        # Run collection and sync
        success = await review_service.run(
            dry_run=args.dry_run,
            output_file=args.output
        )

        if success:
            logger.info("Sprint PR review check script completed successfully")
            sys.exit(0)
        else:
            logger.error("Sprint PR review check script failed")
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
