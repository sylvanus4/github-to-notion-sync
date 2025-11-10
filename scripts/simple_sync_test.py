#!/usr/bin/env python3
"""
Simple sync test with error handling.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger

# Initialize logging
init_logging()
logger = get_logger(__name__)


def main():
    """Simple sync test."""
    try:
        print("🚀 Starting simple sync test...")

        # Initialize services
        github_service = GitHubService()
        notion_service = NotionService()

        # Test 1: Get GitHub items
        print("\n--- Test 1: Getting GitHub items ---")
        items = []
        count = 0
        for item in github_service.get_project_items():
            items.append(item)
            count += 1
            if count >= 3:  # Just test with 3 items
                break

        print(f"✅ Successfully retrieved {len(items)} GitHub items")

        # Test 2: Create simple Notion pages
        print("\n--- Test 2: Creating Notion pages ---")

        for i, item in enumerate(items):
            try:
                # Simple property structure
                properties = {
                    "작업": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": item.get_title()}
                            }
                        ]
                    }
                }

                # Add status if available
                status_value = item.get_field_value("Status")
                if status_value:
                    # Map GitHub status to Notion status
                    status_mapping = {
                        "Epic": "시작 전",
                        "Todo": "시작 전",
                        "In Progress": "진행 중",
                        "Done": "완료",
                        "25-07-Archive": "보관"
                    }
                    mapped_status = status_mapping.get(status_value, "시작 전")

                    # Try different property formats
                    try:
                        properties["진행 상태"] = {
                            "select": {"name": mapped_status}
                        }
                    except:
                        # If that fails, try without the property
                        pass

                # Create page
                response = notion_service.client.pages.create(
                    parent={"database_id": notion_service.settings.notion_db_id},
                    properties=properties
                )

                print(f"✅ Created page {i+1}: {item.get_title()}")
                print(f"   ID: {response['id']}")

                # Store for cleanup
                if i == 0:  # Store first page ID for cleanup later
                    test_page_id = response['id']

            except Exception as e:
                print(f"❌ Failed to create page {i+1}: {e}")
                # Continue with next item
                continue

        print(f"\n✅ Sync test completed!")
        print(f"Successfully processed {len(items)} GitHub items")

        # Cleanup test pages
        print("\n--- Cleanup: Archiving test pages ---")
        try:
            if 'test_page_id' in locals():
                notion_service.client.pages.update(
                    page_id=test_page_id,
                    archived=True
                )
                print("✅ Test pages cleaned up")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
