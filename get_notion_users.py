#!/usr/bin/env python3
"""
Get Notion workspace users
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.notion_service import NotionService
from src.utils.logger import get_logger, init_logging

# Initialize logging
init_logging()
logger = get_logger(__name__)


def get_notion_users():
    """Get all users in Notion workspace"""
    try:
        print("🔍 Getting Notion workspace users...")
        print("=" * 60)

        # Initialize Notion service
        notion_service = NotionService()

        # Get users
        try:
            users_response = notion_service.client.users.list()
            users = users_response.get("results", [])

            print(f"Found {len(users)} users in workspace:")
            print("-" * 40)

            for user in users:
                user_id = user.get("id")
                user_type = user.get("type")
                name = user.get("name", "No name")

                if user_type == "person":
                    person = user.get("person", {})
                    email = person.get("email", "No email")
                    print(f"  👤 {name}")
                    print(f"      ID: {user_id}")
                    print(f"      Email: {email}")
                    print(f"      Type: {user_type}")
                    print()
                elif user_type == "bot":
                    print(f"  🤖 {name} (bot)")
                    print(f"      ID: {user_id}")
                    print()

        except Exception as e:
            print(f"❌ Failed to get users: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    get_notion_users()
