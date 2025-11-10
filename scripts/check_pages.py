#!/usr/bin/env python3
"""Check pages in Notion database."""

import os
import sys
from notion_client import Client

def main():
    """Check pages in Notion database."""
    # Get environment variables
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_DB_ID")

    if not notion_token or not notion_db_id:
        print("Error: NOTION_TOKEN and NOTION_DB_ID environment variables are required")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    try:
        # Query database for all pages
        response = notion.databases.query(
            database_id=notion_db_id,
            page_size=100
        )

        pages = response.get("results", [])
        total_pages = len(pages)

        print(f"Total pages in database: {total_pages}")

        if total_pages > 0:
            print("\nFirst 10 pages:")
            for i, page in enumerate(pages[:10]):
                title = ""
                properties = page.get("properties", {})
                if "작업" in properties:
                    title_prop = properties["작업"]
                    if title_prop.get("title"):
                        title = title_prop["title"][0]["plain_text"]

                created_time = page.get("created_time", "")
                print(f"  {i+1}. {title} (created: {created_time})")

        # Check if there are more pages
        if response.get("has_more", False):
            print(f"\nNote: There are more pages. Showing first {total_pages}.")

    except Exception as e:
        print(f"Error querying database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
