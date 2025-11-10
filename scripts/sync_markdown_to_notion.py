#!/usr/bin/env python3
"""
GitHub Markdown to Notion Page Sync Script.
Syncs a specific GitHub markdown file to a Notion page.
"""

import sys
import os
import asyncio
import argparse
import base64
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Initialize logging first (before importing other modules)
try:
    from src.utils.logger import init_logging, get_logger
    init_logging()
    logger = get_logger(__name__)
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Import other modules
try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
    NOTION_AVAILABLE = True
except Exception as e:
    logger.warning(f"Notion client not available: {e}")
    NOTION_AVAILABLE = False


class MarkdownSyncService:
    """Service for syncing GitHub markdown files to Notion pages."""

    def __init__(self):
        """Initialize markdown sync service."""
        if not NOTION_AVAILABLE:
            raise RuntimeError("Notion client not available. Please install notion-client package.")

        # Initialize Notion client directly
        notion_token = os.getenv("NOTION_TOKEN")
        if not notion_token:
            raise RuntimeError("NOTION_TOKEN environment variable is required.")

        self.notion_client = Client(auth=notion_token)

        # Track sync statistics
        self.stats = {
            "markdown_fetched": False,
            "notion_page_updated": False,
            "start_time": None,
            "end_time": None,
            "error": None
        }

    def _markdown_to_notion_blocks(self, markdown_text: str, title: str = None) -> List[Dict]:
        """Convert markdown text to Notion blocks with improved parsing.

        Args:
            markdown_text: Markdown content
            title: Optional title for the section

        Returns:
            List of Notion block objects
        """
        blocks = []

        # Add title if provided
        if title:
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                }
            })

        if not markdown_text or not markdown_text.strip():
            return blocks

        # Split by lines for better parsing
        lines = markdown_text.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                i += 1
                continue

            # Handle code blocks (multiline)
            if line.startswith('```'):
                code_blocks = self._parse_code_block(lines, i)
                blocks.extend(code_blocks['blocks'])
                i = code_blocks['next_index']
                continue

            # Handle headings
            if line.startswith('#'):
                heading_block = self._parse_heading(line)
                if heading_block:
                    blocks.append(heading_block)
                i += 1
                continue

            # Handle lists (bullet and numbered)
            if self._is_list_item(line):
                list_blocks, next_i = self._parse_list(lines, i)
                blocks.extend(list_blocks)
                i = next_i
                continue

            # Handle blockquotes
            if line.startswith('>'):
                quote_blocks, next_i = self._parse_blockquote(lines, i)
                blocks.extend(quote_blocks)
                i = next_i
                continue

            # Handle horizontal rules
            if line.strip() in ['---', '***', '___']:
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
                i += 1
                continue

            # Handle tables
            if '|' in line and line.count('|') >= 2:
                table_blocks, next_i = self._parse_table(lines, i)
                blocks.extend(table_blocks)
                i = next_i
                continue

            # Handle regular paragraphs
            paragraph_blocks, next_i = self._parse_paragraph(lines, i)
            blocks.extend(paragraph_blocks)
            i = next_i

        return blocks

    def _parse_code_block(self, lines: List[str], start_index: int) -> Dict:
        """Parse code block from lines."""
        blocks = []
        i = start_index
        language = ""
        code_content = []

        # Extract language from first line
        first_line = lines[i].strip()
        if len(first_line) > 3:
            language = first_line[3:].strip()

        i += 1

        # Collect code content until closing ```
        while i < len(lines):
            line = lines[i]
            if line.strip() == '```':
                break
            code_content.append(line)
            i += 1

        # Create code block
        if code_content:
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "language": language or "plain text",
                    "rich_text": [{"type": "text", "text": {"content": '\n'.join(code_content)}}]
                }
            })

        return {"blocks": blocks, "next_index": i + 1}

    def _parse_heading(self, line: str) -> Optional[Dict]:
        """Parse heading from line."""
        heading_level = len(line) - len(line.lstrip('#'))
        heading_text = line.lstrip('# ').strip()

        if not heading_text:
            return None

        # Map heading levels to Notion block types
        if heading_level == 1:
            block_type = "heading_1"
        elif heading_level == 2:
            block_type = "heading_2"
        else:
            block_type = "heading_3"

        # Parse rich text for headings (may contain links)
        rich_text = self._parse_rich_text(heading_text)

        return {
            "object": "block",
            "type": block_type,
            block_type: {
                "rich_text": rich_text
            }
        }

    def _is_list_item(self, line: str) -> bool:
        """Check if line is a list item."""
        return (line.startswith('- ') or line.startswith('* ') or
                line.startswith('+ ') or
                (line and line[0].isdigit() and '. ' in line))

    def _is_list_item_with_indent(self, line: str) -> bool:
        """Check if line is a list item, considering indentation."""
        stripped = line.strip()
        return (stripped.startswith('- ') or stripped.startswith('* ') or
                stripped.startswith('+ ') or
                (stripped and stripped[0].isdigit() and '. ' in stripped))

    def _get_indent_level(self, line: str) -> int:
        """Get the indentation level of a line (number of leading spaces)."""
        return len(line) - len(line.lstrip())

    def _parse_list(self, lines: List[str], start_index: int) -> tuple:
        """Parse list items from lines with proper nesting support."""
        blocks = []
        i = start_index

        while i < len(lines):
            original_line = lines[i]
            line = original_line.strip()

            if not line or not self._is_list_item_with_indent(original_line):
                break

            # Get indentation level
            indent_level = self._get_indent_level(original_line)

            # Determine list type and extract text
            if line.startswith(('- ', '* ', '+ ')):
                list_type = "bulleted_list_item"
                list_text = line[2:].strip()
            else:
                list_type = "numbered_list_item"
                # Extract text after number - handle various formats
                dot_index = line.find('. ')
                if dot_index != -1:
                    list_text = line[dot_index + 2:].strip()
                else:
                    # Handle cases like "1)" or other formats
                    match = re.match(r'^\d+[\)\.]\s*(.*)', line)
                    if match:
                        list_text = match.group(1).strip()
                    else:
                        list_text = line

            # Parse rich text with links and formatting
            rich_text = self._parse_rich_text(list_text)

            # Create list item block
            list_item = {
                "object": "block",
                "type": list_type,
                list_type: {
                    "rich_text": rich_text
                }
            }

            # Check for nested items
            nested_items = []
            next_i = i + 1

            # Look ahead for nested items
            while next_i < len(lines):
                next_original_line = lines[next_i]
                next_line = next_original_line.strip()

                if not next_line:
                    next_i += 1
                    continue

                if not self._is_list_item_with_indent(next_original_line):
                    break

                next_indent = self._get_indent_level(next_original_line)

                # If next item has deeper indentation, it's nested
                if next_indent > indent_level:
                    nested_blocks, next_i = self._parse_list(lines, next_i)
                    nested_items.extend(nested_blocks)
                else:
                    # Same or less indentation, stop looking for nested items
                    break

            # Add nested items if any
            if nested_items:
                list_item[list_type]["children"] = nested_items

            blocks.append(list_item)
            i = next_i if nested_items else i + 1

        return blocks, i

    def _parse_blockquote(self, lines: List[str], start_index: int) -> tuple:
        """Parse blockquote from lines."""
        blocks = []
        i = start_index
        quote_content = []

        while i < len(lines):
            line = lines[i].strip()

            if not line.startswith('>'):
                break

            # Remove '>' prefix and add to content
            quote_text = line[1:].strip()
            if quote_text:
                quote_content.append(quote_text)

            i += 1

        # Create quote block
        if quote_content:
            quote_text = ' '.join(quote_content)
            rich_text = self._parse_rich_text(quote_text)

            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": rich_text
                }
            })

        return blocks, i

    def _parse_table(self, lines: List[str], start_index: int) -> tuple:
        """Parse table from lines."""
        blocks = []
        i = start_index
        table_rows = []
        has_separator = False

        # Collect table rows
        while i < len(lines):
            line = lines[i].strip()

            if not line or '|' not in line:
                break

            # Check if this is a separator row
            if re.match(r'^[\|\-\s:]+$', line):
                has_separator = True
                i += 1
                continue

            # Parse table row - handle empty cells properly
            cells = [cell.strip() for cell in line.split('|')]
            # Remove empty first and last cells if they exist
            if cells and not cells[0]:
                cells = cells[1:]
            if cells and not cells[-1]:
                cells = cells[:-1]
            table_rows.append(cells)

            i += 1

        # Create table block if we have rows
        if table_rows:
            # Create a formatted table representation
            table_content = []

            for row_idx, row in enumerate(table_rows):
                # Clean up each cell and handle bold formatting
                cleaned_cells = []
                for cell in row:
                    # Remove markdown bold formatting and clean up
                    clean_cell = cell.replace('**', '').strip()
                    # Handle empty cells
                    if not clean_cell:
                        clean_cell = " "
                    cleaned_cells.append(clean_cell)

                # Create formatted row with proper spacing
                if row_idx == 0:  # Header row
                    formatted_row = " | ".join([f"**{cell}**" for cell in cleaned_cells])
                else:
                    formatted_row = " | ".join(cleaned_cells)

                table_content.append(formatted_row)

            # Create table as a single paragraph with proper formatting
            table_text = "\n".join(table_content)

            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"📊 Table:\n{table_text}"}}]
                }
            })

        return blocks, i

    def _parse_paragraph(self, lines: List[str], start_index: int) -> tuple:
        """Parse paragraph from lines."""
        blocks = []
        i = start_index
        paragraph_lines = []

        # Collect consecutive non-empty lines
        while i < len(lines):
            line = lines[i].strip()

            # Stop at empty line or special markdown syntax
            if (not line or
                line.startswith('#') or
                line.startswith('```') or
                line.startswith('>') or
                line.startswith('---') or
                line.startswith('***') or
                line.startswith('___') or
                self._is_list_item(line) or
                ('|' in line and line.count('|') >= 2)):
                break

            paragraph_lines.append(line)
            i += 1

        # Create paragraph block
        if paragraph_lines:
            # Join lines with proper spacing, preserving line breaks where needed
            paragraph_text = ' '.join(paragraph_lines)

            # Parse rich text with links and formatting
            rich_text = self._parse_rich_text(paragraph_text)

            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": rich_text
                }
            })

        return blocks, i

    def _parse_rich_text(self, text: str) -> List[Dict]:
        """Parse text with markdown formatting into Notion rich text format.

        Args:
            text: Text with markdown formatting

        Returns:
            List of rich text objects for Notion
        """
        rich_text = []

        # Handle markdown links: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        parts = []
        last_end = 0

        for match in re.finditer(link_pattern, text):
            # Add text before the link
            if match.start() > last_end:
                before_text = text[last_end:match.start()]
                if before_text:
                    parts.append({"type": "text", "content": before_text})

            # Add the link
            link_text = match.group(1)
            link_url = match.group(2)
            parts.append({
                "type": "link",
                "content": link_text,
                "url": link_url
            })

            last_end = match.end()

        # Add remaining text after last link
        if last_end < len(text):
            remaining_text = text[last_end:]
            if remaining_text:
                parts.append({"type": "text", "content": remaining_text})

        # If no links found, treat as plain text
        if not parts:
            parts = [{"type": "text", "content": text}]

        # Convert to Notion rich text format
        for part in parts:
            if part["type"] == "link":
                rich_text.append({
                    "type": "text",
                    "text": {
                        "content": part["content"],
                        "link": {"url": part["url"]}
                    }
                })
            else:
                # Handle bold formatting **text**
                content = part["content"]
                bold_pattern = r'\*\*([^*]+)\*\*'

                if re.search(bold_pattern, content):
                    # Split by bold formatting
                    bold_parts = []
                    last_pos = 0

                    for bold_match in re.finditer(bold_pattern, content):
                        # Add text before bold
                        if bold_match.start() > last_pos:
                            before_bold = content[last_pos:bold_match.start()]
                            if before_bold:
                                bold_parts.append({
                                    "type": "text",
                                    "text": {"content": before_bold}
                                })

                        # Add bold text
                        bold_text = bold_match.group(1)
                        bold_parts.append({
                            "type": "text",
                            "text": {
                                "content": bold_text
                            },
                            "annotations": {"bold": True}
                        })

                        last_pos = bold_match.end()

                    # Add remaining text
                    if last_pos < len(content):
                        remaining = content[last_pos:]
                        if remaining:
                            bold_parts.append({
                                "type": "text",
                                "text": {"content": remaining}
                            })

                    rich_text.extend(bold_parts)
                else:
                    # Plain text
                    rich_text.append({
                        "type": "text",
                        "text": {"content": content}
                    })

        return rich_text if rich_text else [{"type": "text", "text": {"content": text}}]

    def fetch_github_markdown(self, owner: str, repo: str, file_path: str, branch: str = "main") -> Optional[str]:
        """Fetch markdown content from GitHub repository.

        Args:
            owner: GitHub repository owner
            repo: Repository name
            file_path: Path to the markdown file
            branch: Branch name (default: main)

        Returns:
            Markdown content as string, or None if failed
        """
        try:
            # GitHub API endpoint for file content
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

            # Get GitHub token from environment
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                logger.error("GITHUB_TOKEN environment variable not set")
                return None

            headers = {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            }

            params = {"ref": branch}

            logger.info(f"Fetching markdown from {owner}/{repo}/{file_path} (branch: {branch})")

            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            file_data = response.json()

            # Decode base64 content
            if file_data.get("encoding") == "base64":
                content = base64.b64decode(file_data["content"]).decode("utf-8")
                logger.info(f"Successfully fetched markdown content ({len(content)} characters)")
                self.stats["markdown_fetched"] = True
                return content
            else:
                logger.error(f"Unexpected encoding: {file_data.get('encoding')}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch markdown from GitHub: {e}")
            self.stats["error"] = str(e)
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching markdown: {e}")
            self.stats["error"] = str(e)
            return None

    def sync_to_notion_page(self, notion_page_id: str, markdown_content: str,
                           title: str = None, replace_content: bool = True) -> bool:
        """Sync markdown content to a Notion page.

        Args:
            notion_page_id: Notion page ID
            markdown_content: Markdown content to sync
            title: Optional title for the content
            replace_content: Whether to replace existing content or append

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Syncing markdown to Notion page: {notion_page_id}")

            if replace_content:
                # Clear existing content first
                self._clear_page_content(notion_page_id)

            # Convert markdown to Notion blocks
            content_blocks = self._markdown_to_notion_blocks(
                markdown_content, title
            )

            if not content_blocks:
                logger.warning("No content blocks generated from markdown")
                return False

            # Add content to Notion page in chunks (max 100 blocks per request)
            chunk_size = 100
            for i in range(0, len(content_blocks), chunk_size):
                chunk = content_blocks[i:i + chunk_size]
                logger.info(f"Adding chunk {i//chunk_size + 1} with {len(chunk)} blocks")

                response = self.notion_client.blocks.children.append(
                    block_id=notion_page_id,
                    children=chunk
                )

                # Small delay between chunks to avoid rate limiting
                if i + chunk_size < len(content_blocks):
                    import time
                    time.sleep(0.1)

            logger.info(f"Successfully synced markdown to Notion page")
            self.stats["notion_page_updated"] = True
            return True

        except Exception as e:
            logger.error(f"Failed to sync markdown to Notion page: {e}")
            self.stats["error"] = str(e)
            return False

    def _clear_page_content(self, page_id: str) -> bool:
        """Clear all content from a Notion page.

        Args:
            page_id: Notion page ID

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all blocks from the page
            blocks_response = self.notion_client.blocks.children.list(
                block_id=page_id
            )

            # Delete all blocks except the title
            for block in blocks_response.get("results", []):
                if block.get("type") != "child_page":  # Don't delete child pages
                    try:
                        self.notion_client.blocks.delete(block_id=block["id"])
                    except Exception as e:
                        logger.warning(f"Failed to delete block {block['id']}: {e}")

            logger.info("Cleared existing page content")
            return True

        except Exception as e:
            logger.error(f"Failed to clear page content: {e}")
            return False

    def run_sync(self, owner: str, repo: str, file_path: str, notion_page_id: str,
                 branch: str = "main", title: str = None, replace_content: bool = True) -> bool:
        """Run the complete markdown sync process.

        Args:
            owner: GitHub repository owner
            repo: Repository name
            file_path: Path to the markdown file
            notion_page_id: Notion page ID
            branch: Branch name
            title: Optional title for the content
            replace_content: Whether to replace existing content

        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.now()

        try:
            logger.info("Starting GitHub markdown to Notion sync")
            logger.info(f"Source: {owner}/{repo}/{file_path} (branch: {branch})")
            logger.info(f"Target: Notion page {notion_page_id}")

            # Fetch markdown content
            markdown_content = self.fetch_github_markdown(owner, repo, file_path, branch)
            if not markdown_content:
                logger.error("Failed to fetch markdown content")
                return False

            # Sync to Notion page
            success = self.sync_to_notion_page(
                notion_page_id, markdown_content, title, replace_content
            )

            if success:
                logger.info("Markdown sync completed successfully")
            else:
                logger.error("Failed to sync markdown to Notion page")

            return success

        except Exception as e:
            logger.error(f"Unexpected error during sync: {e}")
            self.stats["error"] = str(e)
            return False
        finally:
            self.stats["end_time"] = datetime.now()
            self._print_stats()

    def _print_stats(self):
        """Print sync statistics."""
        duration = None
        if self.stats["start_time"] and self.stats["end_time"]:
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

        print("\n" + "="*50)
        print("MARKDOWN SYNC STATISTICS")
        print("="*50)
        print(f"Markdown fetched: {'✅' if self.stats['markdown_fetched'] else '❌'}")
        print(f"Notion page updated: {'✅' if self.stats['notion_page_updated'] else '❌'}")
        if duration:
            print(f"Duration: {duration:.2f} seconds")
        if self.stats["error"]:
            print(f"Error: {self.stats['error']}")
        print("="*50)


def print_usage_examples():
    """Print usage examples."""
    print("""
🚀 GitHub Markdown to Notion Sync - 사용 예시
==============================================

📋 1. 환경 변수 설정
export NOTION_TOKEN="your-notion-integration-token"
export GITHUB_TOKEN="your-github-personal-access-token"

📝 2. 기본 사용법
python3 scripts/sync_markdown_to_notion.py \\
  --owner ThakiCloud \\
  --repo github-to-notion-sync \\
  --file README.md \\
  --page-id your-notion-page-id

🔍 3. Dry-run으로 미리보기
python3 scripts/sync_markdown_to_notion.py \\
  --owner ThakiCloud \\
  --repo github-to-notion-sync \\
  --file README.md \\
  --page-id your-notion-page-id \\
  --dry-run

🌿 4. 특정 브랜치에서 싱크
python3 scripts/sync_markdown_to_notion.py \\
  --owner ThakiCloud \\
  --repo github-to-notion-sync \\
  --file docs/API.md \\
  --page-id your-notion-page-id \\
  --branch develop \\
  --title "API Documentation"

➕ 5. 기존 내용에 추가
python3 scripts/sync_markdown_to_notion.py \\
  --owner ThakiCloud \\
  --repo github-to-notion-sync \\
  --file CHANGELOG.md \\
  --page-id your-notion-page-id \\
  --no-replace

💡 팁:
- Notion 페이지 ID는 URL에서 32자리 문자열입니다
- GitHub 토큰에는 'repo' 권한이 필요합니다
- Notion 토큰은 해당 페이지에 대한 쓰기 권한이 필요합니다
""")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Sync GitHub markdown file to Notion page",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync README.md from main branch
  python sync_markdown_to_notion.py --owner ThakiCloud --repo my-repo --file README.md --page-id abc123

  # Sync from specific branch with custom title
  python sync_markdown_to_notion.py --owner ThakiCloud --repo my-repo --file docs/guide.md --page-id abc123 --branch develop --title "Development Guide"

  # Append content instead of replacing
  python sync_markdown_to_notion.py --owner ThakiCloud --repo my-repo --file CHANGELOG.md --page-id abc123 --no-replace

  # Show usage examples
  python sync_markdown_to_notion.py --examples
        """
    )

    parser.add_argument(
        "--owner", "-o",
        help="GitHub repository owner (e.g., ThakiCloud)"
    )

    parser.add_argument(
        "--repo", "-r",
        help="Repository name"
    )

    parser.add_argument(
        "--file", "-f",
        help="Path to markdown file (e.g., README.md, docs/guide.md)"
    )

    parser.add_argument(
        "--page-id", "-p",
        help="Notion page ID"
    )

    parser.add_argument(
        "--branch", "-b",
        default="main",
        help="GitHub branch name (default: main)"
    )

    parser.add_argument(
        "--title", "-t",
        help="Optional title for the content section"
    )

    parser.add_argument(
        "--no-replace",
        action="store_true",
        help="Append content instead of replacing existing content"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )

    parser.add_argument(
        "--examples",
        action="store_true",
        help="Show usage examples and exit"
    )

    args = parser.parse_args()

    # Show examples if requested
    if args.examples:
        print_usage_examples()
        return

    # Validate arguments
    if not args.owner or not args.repo or not args.file or not args.page_id:
        print("❌ Error: Missing required arguments.")
        print("Required: --owner, --repo, --file, --page-id")
        print("Use --examples to see usage examples")
        print("Use --help to see all options")
        sys.exit(1)

    # Check if modules are available
    if not NOTION_AVAILABLE:
        print("❌ Error: Notion client not available.")
        print("Please install the required package:")
        print("  pip install notion-client")
        print("")
        print("And ensure the following environment variables are set:")
        print("  - NOTION_TOKEN (required for Notion API access)")
        print("  - GITHUB_TOKEN (required for GitHub API access)")
        sys.exit(1)

    # Initialize service
    sync_service = MarkdownSyncService()

    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print(f"Would sync: {args.owner}/{args.repo}/{args.file} -> Notion page {args.page_id}")
        print(f"Branch: {args.branch}")
        print(f"Title: {args.title or 'None'}")
        print(f"Replace content: {not args.no_replace}")
        return

    # Run sync
    success = sync_service.run_sync(
        owner=args.owner,
        repo=args.repo,
        file_path=args.file,
        notion_page_id=args.page_id,
        branch=args.branch,
        title=args.title,
        replace_content=not args.no_replace
    )

    if success:
        print("\n✅ Markdown sync completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Markdown sync failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
