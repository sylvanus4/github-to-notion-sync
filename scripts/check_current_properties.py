#!/usr/bin/env python3
"""Check current Notion database properties."""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
load_dotenv()

from src.services.notion_service import NotionService

def main():
    notion_service = NotionService()

    try:
        database = notion_service.get_database()

        print("=== Current Notion Database Properties ===")
        print(f"Database: {database.title}")
        print(f"ID: {database.id}")
        print()

        print("Available Properties:")
        if hasattr(database, 'properties') and database.properties:
            for i, (prop_name, prop_data) in enumerate(database.properties.items(), 1):
                if isinstance(prop_data, dict):
                    prop_type = prop_data.get('type', 'unknown')
                    print(f"  {i}. {prop_name}: {prop_type}")
                else:
                    print(f"  {i}. {prop_name}: {type(prop_data)}")

        print("\n=== Checking for GitHub Node ID ===")
        if 'GitHub Node ID' in database.properties:
            print("✅ 'GitHub Node ID' property found!")
        else:
            print("❌ 'GitHub Node ID' property NOT found")
            print("\nPossible similar properties:")
            for prop_name in database.properties.keys():
                if 'github' in prop_name.lower() or 'node' in prop_name.lower() or 'id' in prop_name.lower():
                    print(f"  - {prop_name}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
