#!/usr/bin/env python3
"""
Debug script to inspect GitHub project data.
"""

import sys
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.github_service import GitHubService
from src.utils.logger import init_logging, get_logger

# Initialize logging with DEBUG level
init_logging()
logging.getLogger().setLevel(logging.DEBUG)
logger = get_logger(__name__)


def main():
    """Debug GitHub data fetching."""
    try:
        github_service = GitHubService()

        print("🔍 Fetching GitHub project items...")
        items = []
        for i, item in enumerate(github_service.get_project_items()):
            items.append(item)
            if i >= 4:  # Just get first 5 items for debugging
                break

        print(f"📊 Found {len(items)} items")

        for i, item in enumerate(items):
            print(f"\n--- Item {i+1}: {item.get_title()} ---")
            print(f"ID: {item.id}")
            print(f"Type: {item.type}")
            print(f"Content Type: {type(item.content).__name__ if item.content else 'None'}")
            print(f"Raw field_values count: {len(item.field_values)}")

            print(f"\nField Values ({len(item.field_values)}):")
            for field_value in item.field_values:
                field_name = field_value.field.name
                field_type = field_value.field.dataType

                # Get the actual value
                if hasattr(field_value, 'text'):
                    value = field_value.text
                elif hasattr(field_value, 'number'):
                    value = field_value.number
                elif hasattr(field_value, 'date'):
                    value = field_value.date
                elif hasattr(field_value, 'name'):
                    value = field_value.name
                elif hasattr(field_value, 'title'):
                    value = field_value.title
                else:
                    value = "Unknown"

                print(f"  {field_name} ({field_type}): {value}")

            # Test the get_field_value method
            print(f"\nTesting get_field_value method:")
            status_value = item.get_field_value("Status")
            priority_value = item.get_field_value("Priority")
            end_date_value = item.get_field_value("End date")

            print(f"  Status: {status_value}")
            print(f"  Priority: {priority_value}")
            print(f"  End date: {end_date_value}")

            # Test assignees
            print(f"\nTesting assignees:")
            assignees = item.get_assignees()
            print(f"  Assignees count: {len(assignees)}")
            if assignees:
                for j, assignee in enumerate(assignees):
                    print(f"    {j+1}. {assignee.login} ({assignee.name})")
            else:
                print("    No assignees")

            # Test other content properties
            if item.content:
                print(f"\nContent details:")
                print(f"  URL: {item.get_url()}")
                print(f"  Number: {item.get_number()}")
                print(f"  State: {item.get_state()}")

            print("-" * 50)

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
