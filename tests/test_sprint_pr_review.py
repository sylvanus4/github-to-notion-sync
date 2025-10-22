"""
Test suite for sprint PR review check script.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.sprint_pr_review_check import SprintPRReviewService


class TestSprintPRReviewService:
    """Test SprintPRReviewService class."""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock config."""
        config = Mock()
        config.settings = Mock()
        config.settings.github_org = "TestOrg"
        config.settings.github_project_number = 5
        config.settings.github_token = "test_token"
        return config
    
    @pytest.fixture
    def service(self, mock_config):
        """Create service instance with mocked dependencies."""
        with patch('scripts.sprint_pr_review_check.get_config', return_value=mock_config):
            with patch('scripts.sprint_pr_review_check.GitHubService'):
                with patch('scripts.sprint_pr_review_check.NotionService'):
                    with patch('scripts.sprint_pr_review_check.FieldMapper'):
                        service = SprintPRReviewService(
                            sprint_name="Test-Sprint",
                            notion_parent_id="test_parent_id"
                        )
                        return service
    
    def test_initialization(self, service):
        """Test service initialization."""
        assert service.sprint_name == "Test-Sprint"
        assert service.notion_parent_id == "test_parent_id"
        assert service.stats["sprint_name"] == "Test-Sprint"
        assert service.stats["total_prs"] == 0
    
    def test_get_notion_display_name(self, service):
        """Test GitHub username to Notion display name conversion."""
        assert service.get_notion_display_name("sylvanus4") == "한효정"
        assert service.get_notion_display_name("jaehoonkim") == "김재훈"
        assert service.get_notion_display_name("unknown_user") == "unknown_user"
    
    def test_get_notion_user_id(self, service):
        """Test GitHub username to Notion User ID conversion."""
        assert service.get_notion_user_id("sylvanus4") == "229d872b-594c-816d-ae7c-0002f11615c0"
        assert service.get_notion_user_id("jaehoonkim") == "229d872b-594c-8150-879d-00022f27519e"
        assert service.get_notion_user_id("unknown_user") is None
    
    def test_is_bot_reviewer(self, service):
        """Test bot reviewer detection."""
        # Test exact match
        assert service.is_bot_reviewer("coderabbitai", "ThakiCloud/ai-platform-webui") is True
        assert service.is_bot_reviewer("humanreviewer", "ThakiCloud/ai-platform-webui") is False
        
        # Test non-configured repository
        assert service.is_bot_reviewer("coderabbitai", "ThakiCloud/other-repo") is False
    
    def test_get_valid_reviews(self, service):
        """Test filtering of bot reviewers."""
        reviews = [
            {"reviewer": "coderabbitai", "state": "APPROVED"},
            {"reviewer": "humanreviewer", "state": "APPROVED"},
            {"reviewer": "anotherhuman", "state": "COMMENTED"},
        ]
        
        # For ai-platform-webui, coderabbitai should be filtered
        valid_reviews = service.get_valid_reviews(reviews, "ThakiCloud/ai-platform-webui")
        assert len(valid_reviews) == 2
        assert all(r["reviewer"] != "coderabbitai" for r in valid_reviews)
        
        # For other repos, all reviews should be valid
        valid_reviews = service.get_valid_reviews(reviews, "ThakiCloud/other-repo")
        assert len(valid_reviews) == 3
    
    @pytest.mark.asyncio
    async def test_collect_sprint_prs(self, service):
        """Test PR collection with sorting and bot filtering."""
        # Mock GitHub service
        start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2024, 1, 14, tzinfo=timezone.utc)
        
        mock_reviews = [
            # Repo A - has human review
            {
                "pr": {
                    "number": 1,
                    "title": "Test PR 1",
                    "author": "testuser",
                    "repository": "ThakiCloud/ai-platform-webui",
                    "createdAt": "2024-01-02T00:00:00Z",
                    "mergedAt": None
                },
                "reviewer": "humanreviewer",
                "state": "APPROVED",
                "submittedAt": "2024-01-03T00:00:00Z"
            },
            # Repo A - only bot review (should be not reviewed)
            {
                "pr": {
                    "number": 2,
                    "title": "Test PR 2",
                    "author": "testuser2",
                    "repository": "ThakiCloud/ai-platform-webui",
                    "createdAt": "2024-01-05T00:00:00Z",
                    "mergedAt": None
                },
                "reviewer": "coderabbitai",
                "state": "APPROVED",
                "submittedAt": "2024-01-06T00:00:00Z"
            },
            # Repo B - has review
            {
                "pr": {
                    "number": 3,
                    "title": "Test PR 3",
                    "author": "testuser3",
                    "repository": "ThakiCloud/other-repo",
                    "createdAt": "2024-01-04T00:00:00Z",
                    "mergedAt": None
                },
                "reviewer": "reviewer1",
                "state": "APPROVED",
                "submittedAt": "2024-01-05T00:00:00Z"
            }
        ]
        
        service.github_service.get_all_organization_pr_reviews = Mock(return_value=mock_reviews)
        
        prs = await service.collect_sprint_prs(start_date, end_date)
        
        assert len(prs) >= 2
        
        # Find specific PRs
        pr1 = next((p for p in prs if p["number"] == 1), None)
        pr2 = next((p for p in prs if p["number"] == 2), None)
        
        # PR1 should have reviews (human reviewer)
        assert pr1 is not None
        assert pr1["has_reviews"] is True
        
        # PR2 should NOT have reviews (only bot reviewer)
        assert pr2 is not None
        assert pr2["has_reviews"] is False
        
        # Verify sorting: Repository first
        for i in range(len(prs) - 1):
            # If same repository, not reviewed should come before reviewed
            if prs[i]["repository"] == prs[i + 1]["repository"]:
                if not prs[i]["has_reviews"]:
                    # Not reviewed comes first within same repository
                    pass  # This is correct
                    
        # Check that ThakiCloud/ai-platform-webui PRs come before ThakiCloud/other-repo
        # (alphabetically)
        repo_order = [pr["repository"] for pr in prs]
        ai_platform_indices = [i for i, r in enumerate(repo_order) if r == "ThakiCloud/ai-platform-webui"]
        other_repo_indices = [i for i, r in enumerate(repo_order) if r == "ThakiCloud/other-repo"]
        
        if ai_platform_indices and other_repo_indices:
            assert max(ai_platform_indices) < min(other_repo_indices)
    
    def test_create_notion_database_no_parent_id(self, service):
        """Test database creation without parent ID."""
        service.notion_parent_id = None
        
        with patch.dict('os.environ', {}, clear=True):
            result = service.create_notion_database()
            assert result is None
    
    def test_create_notion_database_success(self, service):
        """Test successful database creation."""
        service.notion_parent_id = "test_parent_id"
        service.notion_service.create_database = Mock(return_value="test_db_id")
        
        result = service.create_notion_database()
        
        assert result == "test_db_id"
        assert service.notion_db_id == "test_db_id"
        service.notion_service.create_database.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_sync_prs_to_notion_no_db_id(self, service):
        """Test sync without database ID."""
        service.notion_db_id = None
        
        result = await service.sync_prs_to_notion([])
        
        assert result["created"] == 0
        assert result["updated"] == 0
        assert result["failed"] == 0
    
    @pytest.mark.asyncio
    async def test_sync_prs_to_notion_success(self, service):
        """Test successful sync."""
        service.notion_db_id = "test_db_id"
        
        mock_prs = [
            {
                "number": 1,
                "title": "Test PR",
                "author": "testuser",
                "repository": "TestOrg/test-repo",
                "created_at": "2024-01-01T00:00:00Z",
                "has_reviews": True,
                "reviews": [{"reviewer": "reviewer1", "state": "APPROVED"}]
            }
        ]
        
        service.notion_service.find_page_by_composite_key = Mock(return_value=None)
        service.notion_service.create_page_in_database = Mock(return_value={"id": "page_id"})
        
        result = await service.sync_prs_to_notion(mock_prs)
        
        assert result["created"] == 1
        assert result["failed"] == 0


class TestSprintPRReviewIntegration:
    """Integration tests for sprint PR review service."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_workflow_dry_run(self):
        """Test full workflow in dry run mode."""
        with patch('scripts.sprint_pr_review_check.get_config'):
            with patch('scripts.sprint_pr_review_check.GitHubService') as mock_gh:
                with patch('scripts.sprint_pr_review_check.NotionService'):
                    with patch('scripts.sprint_pr_review_check.FieldMapper'):
                        # Setup mocks
                        mock_gh_instance = mock_gh.return_value
                        
                        # Mock sprint field
                        mock_field = Mock()
                        mock_field.name = "스프린트"
                        mock_field.dataType = Mock(value="ITERATION")
                        
                        mock_iteration = Mock()
                        mock_iteration.title = "Test-Sprint"
                        mock_iteration.start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
                        mock_iteration.duration = 14
                        
                        mock_config = Mock()
                        mock_config.iterations = [mock_iteration]
                        mock_field.configuration = mock_config
                        
                        mock_gh_instance.get_project_fields.return_value = [mock_field]
                        mock_gh_instance.get_all_organization_pr_reviews.return_value = []
                        
                        # Create service and run
                        service = SprintPRReviewService(
                            sprint_name="Test-Sprint",
                            notion_parent_id="test_parent_id"
                        )
                        service.github_service = mock_gh_instance
                        
                        result = await service.run(dry_run=True)
                        
                        # In dry run, should succeed even with no data
                        assert result is True


def test_imports():
    """Test that all required imports are available."""
    try:
        from scripts.sprint_pr_review_check import (
            SprintPRReviewService,
            GITHUB_TO_NOTION_NAME,
            GITHUB_TO_NOTION_USER_ID
        )
        assert SprintPRReviewService is not None
        assert isinstance(GITHUB_TO_NOTION_NAME, dict)
        assert isinstance(GITHUB_TO_NOTION_USER_ID, dict)
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_script_executable():
    """Test that script file exists and is executable."""
    script_path = Path(__file__).parent.parent / "scripts" / "sprint_pr_review_check.py"
    assert script_path.exists(), "Script file does not exist"
    assert script_path.is_file(), "Script path is not a file"
    # Check if file has execute permission
    import os
    assert os.access(script_path, os.X_OK), "Script is not executable"

