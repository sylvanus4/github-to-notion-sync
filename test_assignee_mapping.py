#!/usr/bin/env python3
"""
Test script for assignee mapping functionality
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config import config
from src.utils.mapping import FieldMapper
from src.models.github_models import GitHubUser

def test_assignee_mapping():
    """Test the assignee mapping functionality"""
    
    # Load config
    field_mapper = FieldMapper(config)
    
    # Test GitHub usernames
    test_usernames = [
        "duyeol-yu",
        "jaehoonkim", 
        "sylvanus4",
        "thaki-yakhyo",
        "thakicloud-jotaeyang",
        "yunjae-park1111",
        "unknown-user"  # Test unknown user
    ]
    
    print("🧪 Testing Assignee Mapping")
    print("=" * 50)
    
    for username in test_usernames:
        # Create a mock GitHubUser object
        mock_user = GitHubUser(
            login=username,
            email=f"{username}@example.com",
            name=username,
            avatar_url=f"https://avatars.githubusercontent.com/{username}"
        )
        
        # Test single assignee
        result = field_mapper.transform_value("Assignees", [mock_user])
        print(f"GitHub: {username}")
        print(f"Mapped: {result}")
        print("-" * 30)
    
    # Test empty assignees
    result = field_mapper.transform_value("Assignees", [])
    print(f"Empty assignees: {result}")
    print("-" * 30)
    
    # Test None assignees  
    result = field_mapper.transform_value("Assignees", None)
    print(f"None assignees: {result}")
    
if __name__ == "__main__":
    test_assignee_mapping() 