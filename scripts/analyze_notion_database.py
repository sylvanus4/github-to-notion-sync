#!/usr/bin/env python3
"""
Analyze Notion database properties and suggest GitHub field mappings.
This script helps understand the current database structure before sync.
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
from src.services.github_service import GitHubService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)


def analyze_notion_database():
    """Analyze the Notion database structure."""
    logger.info("Analyzing Notion database structure...")

    try:
        notion_service = NotionService()

        # Get database information
        database = notion_service.get_database()

        if not database:
            logger.error("Failed to retrieve database information")
            return None

        logger.info(f"Database ID: {database.id}")
        logger.info(f"Database Title: {database.title}")

        print("\n" + "="*60)
        print("NOTION DATABASE ANALYSIS")
        print("="*60)

        # Analyze properties
        properties = database.properties
        print(f"\nFound {len(properties)} properties:")
        print("-" * 40)

        property_info = {}
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get('type', 'unknown')
            property_info[prop_name] = prop_type

            print(f"Property: {prop_name}")
            print(f"  Type: {prop_type}")

            # Show additional info for select properties
            if prop_type == 'select' and 'select' in prop_data:
                options = prop_data['select'].get('options', [])
                if options:
                    print(f"  Options: {[opt.get('name', '') for opt in options]}")
            elif prop_type == 'multi_select' and 'multi_select' in prop_data:
                options = prop_data['multi_select'].get('options', [])
                if options:
                    print(f"  Options: {[opt.get('name', '') for opt in options]}")

            print()

        return property_info

    except Exception as e:
        logger.error(f"Failed to analyze database: {e}")
        return None


def analyze_github_data():
    """Analyze GitHub project data structure."""
    logger.info("Analyzing GitHub project data...")

    try:
        github_service = GitHubService()

        # Get project fields
        project_fields = github_service.get_project_fields()

        print("\n" + "="*60)
        print("GITHUB PROJECT ANALYSIS")
        print("="*60)

        print(f"\nFound {len(project_fields)} custom fields:")
        print("-" * 40)

        field_info = {}
        for field in project_fields:
            field_info[field.name] = {
                'id': field.id,
                'dataType': field.dataType.value if field.dataType else 'unknown'
            }

            print(f"Field: {field.name}")
            print(f"  ID: {field.id}")
            print(f"  Type: {field.dataType.value if field.dataType else 'unknown'}")

            # Show options for select fields
            if hasattr(field, 'options') and field.options:
                try:
                    if isinstance(field.options, list):
                        print(f"  Options: {[opt.get('name', str(opt)) if isinstance(opt, dict) else getattr(opt, 'name', str(opt)) for opt in field.options]}")
                    else:
                        print(f"  Options: {field.options}")
                except Exception as e:
                    print(f"  Options: (could not parse - {e})")

            print()

        # Get sample items to understand data structure
        print("\nSample GitHub items (first 3):")
        print("-" * 40)

        try:
            items = list(github_service.get_project_items())[:3]
            for i, item in enumerate(items, 1):
                print(f"\nItem {i}:")
                print(f"  ID: {item.id}")
                print(f"  Type: {item.type.value if hasattr(item.type, 'value') else item.type}")
                print(f"  Title: {item.get_title() if hasattr(item, 'get_title') else 'N/A'}")

                # Show field values
                print("  Custom Fields:")
                if hasattr(item, 'field_values') and item.field_values:
                    for field_value in item.field_values:
                        try:
                            field_name = getattr(field_value.field, 'name', 'Unknown')
                            value = None

                            if hasattr(field_value, 'text'):
                                value = field_value.text
                            elif hasattr(field_value, 'name'):
                                value = field_value.name
                            elif hasattr(field_value, 'date'):
                                value = field_value.date
                            elif hasattr(field_value, 'number'):
                                value = field_value.number

                            print(f"    {field_name}: {value}")
                        except Exception as e:
                            print(f"    (field parsing error: {e})")
                else:
                    print("    No field values found")

            return field_info, items[:3]
        except Exception as e:
            print(f"Error getting sample items: {e}")
            return field_info, []

    except Exception as e:
        logger.error(f"Failed to analyze GitHub data: {e}")
        return None, []


def suggest_mappings(notion_properties, github_fields):
    """Suggest field mappings based on analysis."""
    print("\n" + "="*60)
    print("SUGGESTED FIELD MAPPINGS")
    print("="*60)

    # Common mappings based on naming patterns
    common_mappings = {
        'title': ['작업', 'Task Name', 'Title', '제목'],
        'status': ['진행 상태', 'Status', '상태'],
        'priority': ['우선순위', 'Priority', '우선 순위'],
        'assignees': ['담당자', 'Assignees', 'Assignee', '담당', '할당'],
        'due_date': ['마감일', 'Due Date', 'End Date', '마감', '종료일'],
        'labels': ['태그', 'Tags', 'Labels', '라벨'],
    }

    print("\nRecommended mappings:")
    print("-" * 30)

    mappings = {}

    for github_field, notion_candidates in common_mappings.items():
        for candidate in notion_candidates:
            if candidate in notion_properties:
                mappings[github_field] = candidate
                print(f"{github_field:15} -> {candidate} ({notion_properties[candidate]})")
                break

    # Check for unmapped Notion properties
    unmapped_notion = []
    for prop_name in notion_properties:
        if prop_name not in mappings.values():
            unmapped_notion.append(prop_name)

    if unmapped_notion:
        print(f"\nUnmapped Notion properties: {unmapped_notion}")

    # Check for unmapped GitHub fields
    unmapped_github = []
    for field_name in github_fields:
        if field_name not in mappings:
            unmapped_github.append(field_name)

    if unmapped_github:
        print(f"Unmapped GitHub fields: {unmapped_github}")

    return mappings


def main():
    """Main function."""
    logger.info("Starting database analysis...")

    try:
        # Analyze Notion database
        notion_properties = analyze_notion_database()
        if not notion_properties:
            logger.error("Failed to analyze Notion database")
            sys.exit(1)

        # Analyze GitHub data
        github_fields, sample_items = analyze_github_data()
        if not github_fields:
            logger.error("Failed to analyze GitHub data")
            sys.exit(1)

        # Suggest mappings
        mappings = suggest_mappings(notion_properties, github_fields)

        # Save analysis results
        analysis_results = {
            'notion_properties': notion_properties,
            'github_fields': github_fields,
            'suggested_mappings': mappings,
            'sample_items_count': len(sample_items)
        }

        with open('database_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)

        logger.info("Analysis complete! Results saved to database_analysis.json")

        print(f"\n{'='*60}")
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"Results saved to: database_analysis.json")
        print(f"Notion properties: {len(notion_properties)}")
        print(f"GitHub fields: {len(github_fields)}")
        print(f"Suggested mappings: {len(mappings)}")

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
