#!/usr/bin/env python3
"""
Check actual status options in Notion database by examining existing pages.
"""

import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)


def check_status_options():
    """Check actual status options used in existing Notion pages."""
    logger.info("Checking actual status options in Notion database...")

    # Initialize services
    notion_service = NotionService()

    try:
        # Get all existing pages
        print("Fetching existing pages from Notion database...")
        pages = notion_service.get_all_pages()

        print(f"Found {len(pages)} existing pages")

        # Collect all unique status values
        status_values = set()
        sample_pages = []

        for i, page in enumerate(pages[:10]):  # Look at first 10 pages
            page_data = {
                "id": page.id,
                "title": "Unknown",
                "status": None
            }

            # Get title
            if page.properties and "작업" in page.properties:
                title_prop = page.properties["작업"]
                if hasattr(title_prop, 'title') and title_prop.title:
                    page_data["title"] = title_prop.title[0].plain_text if title_prop.title else "No title"

            # Get status
            if page.properties and "진행 상태" in page.properties:
                status_prop = page.properties["진행 상태"]
                print(f"Page {i+1} status property type: {type(status_prop)}")
                print(f"Page {i+1} status property: {status_prop}")

                # Try different ways to get status value
                if hasattr(status_prop, 'status') and status_prop.status:
                    if hasattr(status_prop.status, 'name'):
                        status_value = status_prop.status.name
                        status_values.add(status_value)
                        page_data["status"] = status_value
                    else:
                        page_data["status"] = str(status_prop.status)
                        print(f"  Status object: {status_prop.status}")
                elif hasattr(status_prop, 'name'):
                    status_value = status_prop.name
                    status_values.add(status_value)
                    page_data["status"] = status_value
                else:
                    print(f"  Could not parse status for page {i+1}")

            sample_pages.append(page_data)

        print("\n" + "="*60)
        print("NOTION STATUS OPTIONS ANALYSIS")
        print("="*60)

        print(f"\nUnique status values found: {len(status_values)}")
        if status_values:
            for status in sorted(status_values):
                print(f"  - '{status}'")
        else:
            print("  No status values found")

        print(f"\nSample pages:")
        for page in sample_pages:
            print(f"  {page['title'][:50]:50} | Status: {page['status']}")

        # Try to get database schema to see status field definition
        print(f"\nTrying to get database schema...")
        database = notion_service.get_database()
        if database and database.properties:
            status_property = database.properties.get("진행 상태")
            if status_property:
                print(f"Status property type: {status_property.type}")
                print(f"Status property details: {status_property}")

                # Check if it has options
                if hasattr(status_property, 'status') and status_property.status:
                    status_config = status_property.status
                    print(f"Status config: {status_config}")

                    if hasattr(status_config, 'options'):
                        print(f"Status options from schema: {status_config.options}")
                    if hasattr(status_config, 'groups'):
                        print(f"Status groups from schema: {status_config.groups}")

        return status_values

    except Exception as e:
        logger.error(f"Error checking status options: {e}")
        import traceback
        traceback.print_exc()
        return set()


if __name__ == "__main__":
    status_options = check_status_options()
    print(f"\nFound {len(status_options)} unique status values")
