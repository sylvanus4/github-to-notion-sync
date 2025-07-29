#!/usr/bin/env python3
"""
Final sync test with corrected property names.
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
    """Final sync test with proper property names."""
    try:
        print("🚀 Starting final sync test...")
        
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
            if count >= 5:  # Test with 5 items
                break
        
        print(f"✅ Successfully retrieved {len(items)} GitHub items")
        
        # Test 2: Create Notion pages with corrected property names
        print("\n--- Test 2: Creating Notion pages ---")
        created_pages = []
        
        for i, item in enumerate(items):
            try:
                # Basic properties that should always work
                properties = {
                    "작업": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": f"[TEST] {item.get_title()}"}
                            }
                        ]
                    }
                }
                
                # Try to add mapped fields gradually
                status_value = item.get_field_value("Status")
                priority_value = item.get_field_value("Priority")
                end_date_value = item.get_field_value("End date")
                
                print(f"   Item {i+1}: {item.get_title()}")
                print(f"   - Status: {status_value}")
                print(f"   - Priority: {priority_value}")
                print(f"   - End date: {end_date_value}")
                
                # Map GitHub values to Notion values
                if status_value:
                    status_mapping = {
                        "Epic": "시작 전",
                        "Todo": "시작 전", 
                        "In Progress": "진행 중",
                        "Done": "완료",
                        "25-07-Archive": "보관"
                    }
                    mapped_status = status_mapping.get(status_value, "시작 전")
                    
                    # Use "status" instead of "진행 상태"
                    properties["status"] = {
                        "select": {"name": mapped_status}
                    }
                
                if priority_value:
                    priority_mapping = {
                        "P0": "높음",
                        "P1": "중간", 
                        "P2": "낮음"
                    }
                    mapped_priority = priority_mapping.get(priority_value, "중간")
                    
                    properties["우선순위"] = {
                        "select": {"name": mapped_priority}
                    }
                
                if end_date_value:
                    # Format date properly
                    if hasattr(end_date_value, 'strftime'):
                        date_str = end_date_value.strftime('%Y-%m-%d')
                    else:
                        date_str = str(end_date_value)
                    
                    properties["마감일"] = {
                        "date": {"start": date_str}
                    }
                
                # Create page
                response = notion_service.client.pages.create(
                    parent={"database_id": notion_service.settings.notion_db_id},
                    properties=properties
                )
                
                print(f"   ✅ Created page: {response['id']}")
                created_pages.append(response['id'])
                
            except Exception as e:
                print(f"   ❌ Failed to create page {i+1}: {e}")
                # Try with minimal properties
                try:
                    minimal_properties = {
                        "작업": {
                            "title": [
                                {
                                    "type": "text",
                                    "text": {"content": f"[MINIMAL TEST] {item.get_title()}"}
                                }
                            ]
                        }
                    }
                    
                    response = notion_service.client.pages.create(
                        parent={"database_id": notion_service.settings.notion_db_id},
                        properties=minimal_properties
                    )
                    
                    print(f"   ✅ Created minimal page: {response['id']}")
                    created_pages.append(response['id'])
                    
                except Exception as e2:
                    print(f"   ❌ Even minimal creation failed: {e2}")
                    continue
        
        print(f"\n✅ Sync test completed!")
        print(f"Successfully created {len(created_pages)} Notion pages")
        print(f"Processed {len(items)} GitHub items")
        
        # Provide cleanup information
        if created_pages:
            print(f"\n📋 Created pages for cleanup:")
            for page_id in created_pages:
                print(f"   - {page_id}")
            
            # Ask if user wants to cleanup
            print(f"\n🧹 To cleanup test pages later, you can archive them manually in Notion")
            print(f"   or run: notion_service.client.pages.update(page_id='PAGE_ID', archived=True)")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 