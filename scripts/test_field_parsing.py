#!/usr/bin/env python3
"""
Test field value parsing directly.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.models.github_models import GitHubProjectField, GitHubProjectFieldType

def test_field_parsing():
    """Test field value parsing logic."""
    
    # Test data from actual API response
    test_field_values = [
        {
            "name": "25-07-Archive",
            "optionId": "c0a1d8f8",
            "field": {
                "id": "PVTSSF_lADODHOnas4A9FHMzgw46Tk",
                "name": "Status",
                "dataType": "SINGLE_SELECT"
            }
        },
        {
            "text": "전사 주간보고",
            "field": {
                "id": "PVTF_lADODHOnas4A9FHMzgw46Tc",
                "name": "Title",
                "dataType": "TITLE"
            }
        },
        {
            "name": "P1",
            "optionId": "87367794",
            "field": {
                "id": "PVTSSF_lADODHOnas4A9FHMzgw46qc",
                "name": "Priority",
                "dataType": "SINGLE_SELECT"
            }
        },
        {
            "date": "2025-07-28",
            "field": {
                "id": "PVTF_lADODHOnas4A9FHMzgw46qw",
                "name": "End date",
                "dataType": "DATE"
            }
        }
    ]
    
    for i, field_value_data in enumerate(test_field_values):
        print(f"\n--- Testing field value {i+1} ---")
        print(f"Raw data: {field_value_data}")
        
        try:
            field_data = field_value_data.get("field", {})
            print(f"Field name: {field_data.get('name')}")
            print(f"Field dataType: {field_data.get('dataType')}")
            
            # Try to create GitHubProjectField
            field = GitHubProjectField(**field_data)
            print(f"Created field: {field.name} ({field.dataType})")
            
            # Check field type enum value
            print(f"Field type enum: {GitHubProjectFieldType.SINGLE_SELECT}")
            print(f"Matches SINGLE_SELECT: {field.dataType == GitHubProjectFieldType.SINGLE_SELECT}")
            print(f"Matches DATE: {field.dataType == GitHubProjectFieldType.DATE}")
            print(f"Matches TITLE: {field.dataType == GitHubProjectFieldType.TITLE}")
            
            # Check what keys are available
            print(f"Available keys in data: {list(field_value_data.keys())}")
            
            # Check specific conditions
            if field.dataType == GitHubProjectFieldType.SINGLE_SELECT and "name" in field_value_data:
                print(f"✅ SINGLE_SELECT condition met!")
            elif field.dataType == GitHubProjectFieldType.DATE and "date" in field_value_data:
                print(f"✅ DATE condition met!")
                # Test date parsing
                date_str = field_value_data["date"]
                try:
                    parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    print(f"✅ Date parsed successfully: {parsed_date}")
                except Exception as date_e:
                    print(f"❌ Date parsing failed: {date_e}")
            elif field.dataType == GitHubProjectFieldType.TITLE and "text" in field_value_data:
                print(f"✅ TITLE condition met!")
            else:
                print(f"❌ No condition met")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_field_parsing() 