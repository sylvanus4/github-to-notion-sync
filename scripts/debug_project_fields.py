#!/usr/bin/env python3
"""
Debug script to inspect GitHub project fields.
"""

import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.github_service import GitHubService
from src.utils.logger import init_logging, get_logger

# Initialize logging
init_logging()
logger = get_logger(__name__)


def main():
    """Debug GitHub project fields."""
    try:
        github_service = GitHubService()
        
        print("🔍 Fetching GitHub project info...")
        project_info = github_service.get_project_info()
        
        if project_info:
            print(f"📊 Project Info:")
            print(f"  ID: {project_info.get('id')}")
            print(f"  Title: {project_info.get('title')}")
            print(f"  URL: {project_info.get('url')}")
        else:
            print("❌ Could not fetch project info")
            
        # Let's also get raw data to see what fields are available
        print("\n🔍 Making raw GraphQL request to see available fields...")
        
        # Use the get_project_fields query
        query = github_service.config.load_graphql_query("get_project_fields")
        if query:
            variables = {
                "org": github_service.settings.github_org,
                "num": github_service.settings.github_project_number
            }
            
            response = github_service._make_request(query, variables)
            
            if response.data:
                project_data = response.data.get("organization", {}).get("projectV2", {})
                fields = project_data.get("fields", {}).get("nodes", [])
                
                print(f"\n📊 Project Fields ({len(fields)}):")
                for field in fields:
                    field_name = field.get("name")
                    field_type = field.get("dataType")
                    field_id = field.get("id")
                    
                    print(f"  {field_name} ({field_type}) - ID: {field_id}")
                    
                    # If it's a select field, show options
                    if field_type == "SINGLE_SELECT" and "options" in field:
                        options = field.get("options", [])
                        print(f"    Options:")
                        for option in options:
                            print(f"      - {option.get('name')} (ID: {option.get('id')})")
                            
                # Now let's get one item and see its raw structure
                items_data = project_data.get("items", {}).get("nodes", [])
                if items_data:
                    print(f"\n🔍 Raw structure of first item:")
                    first_item = items_data[0]
                    field_values = first_item.get("fieldValues", {}).get("nodes", [])
                    
                    print(f"Field Values Raw Data:")
                    for i, fv in enumerate(field_values):
                        print(f"  [{i}] {json.dumps(fv, indent=4)}")
                        
                    print(f"\nFirst item raw structure:")
                    print(json.dumps(first_item, indent=2))
                    
        else:
            print("❌ Could not load get_project_fields query")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 