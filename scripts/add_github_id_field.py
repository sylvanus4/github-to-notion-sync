#!/usr/bin/env python3
"""
Add GitHub ID field to Notion database for duplicate checking.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
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


def add_github_id_field():
    """Add GitHub ID field to Notion database."""
    try:
        config = get_config()
        notion_service = NotionService()
        
        database_id = config.settings.notion_db_id
        
        logger.info(f"Adding GitHub ID field to database {database_id}...")
        
        # Update database to add GitHub ID property
        response = notion_service.client.databases.update(
            database_id=database_id,
            properties={
                "GitHub ID": {
                    "rich_text": {}
                }
            }
        )
        
        logger.info("Successfully added GitHub ID field to database")
        logger.info(f"Database: {response.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        
        # Verify the field was added
        database = notion_service.get_database()
        if database and "GitHub ID" in database.properties:
            logger.info("✅ GitHub ID field verified in database")
            return True
        else:
            logger.error("❌ GitHub ID field not found after adding")
            return False
        
    except Exception as e:
        logger.error(f"Failed to add GitHub ID field: {e}")
        return False


if __name__ == "__main__":
    success = add_github_id_field()
    sys.exit(0 if success else 1)

