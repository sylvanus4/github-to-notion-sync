#!/usr/bin/env python3
"""
노션 회의록 페이지에서 미팅 노트 스크립트를 추출하여 로컬에 저장하는 스크립트.

Usage:
    python scripts/extract_meeting_scripts.py

환경 변수:
    NOTION_TOKEN: 노션 API 토큰
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client

# .env 파일에서 환경 변수 로드
load_dotenv()

# 회의록 데이터베이스 ID
MEETINGS_DATABASE_ID = "22c9eddc34e680d5beb9d2cf6c8403b4"

# 출력 디렉토리
OUTPUT_DIR = Path("meeting_scripts")


def get_notion_client():
    """노션 클라이언트 초기화."""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN 환경 변수가 설정되지 않았습니다.")
    return Client(auth=token)


def get_all_meeting_pages(client: Client, database_id: str) -> list[dict]:
    """데이터베이스에서 모든 회의록 페이지를 가져옵니다."""
    pages = []
    cursor = None
    
    while True:
        query_params = {
            "database_id": database_id,
            "page_size": 100,
        }
        if cursor:
            query_params["start_cursor"] = cursor
            
        response = client.databases.query(**query_params)
        pages.extend(response.get("results", []))
        
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
    
    print(f"총 {len(pages)}개의 회의록 페이지를 찾았습니다.")
    return pages


def get_page_blocks(client: Client, page_id: str) -> list[dict]:
    """페이지의 모든 블록을 가져옵니다 (중첩된 블록 포함)."""
    blocks = []
    cursor = None
    
    while True:
        query_params = {
            "block_id": page_id,
            "page_size": 100,
        }
        if cursor:
            query_params["start_cursor"] = cursor
            
        response = client.blocks.children.list(**query_params)
        blocks.extend(response.get("results", []))
        
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
    
    return blocks


def get_nested_blocks(client: Client, block_id: str) -> list[dict]:
    """중첩된 블록을 재귀적으로 가져옵니다."""
    try:
        return get_page_blocks(client, block_id)
    except Exception as e:
        # 일부 블록 타입(예: transcription)은 API에서 지원되지 않음
        print(f"  [경고] 블록 {block_id[:8]}... 의 자식 블록을 가져올 수 없음: {e}")
        return []


def extract_text_from_rich_text(rich_text_list: list) -> str:
    """rich_text 배열에서 텍스트를 추출합니다."""
    return "".join(item.get("plain_text", "") for item in rich_text_list)


def block_to_text(block: dict, indent: int = 0) -> str:
    """블록을 텍스트로 변환합니다."""
    block_type = block.get("type", "")
    indent_str = "  " * indent
    text = ""
    
    if block_type == "paragraph":
        content = block.get("paragraph", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        return f"{indent_str}{text}\n" if text else "\n"
    
    elif block_type in ("heading_1", "heading_2", "heading_3"):
        content = block.get(block_type, {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        prefix = "#" * int(block_type[-1])
        return f"{indent_str}{prefix} {text}\n"
    
    elif block_type == "bulleted_list_item":
        content = block.get("bulleted_list_item", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        return f"{indent_str}• {text}\n"
    
    elif block_type == "numbered_list_item":
        content = block.get("numbered_list_item", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        return f"{indent_str}1. {text}\n"
    
    elif block_type == "to_do":
        content = block.get("to_do", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        checked = "☑" if content.get("checked") else "☐"
        return f"{indent_str}{checked} {text}\n"
    
    elif block_type == "toggle":
        content = block.get("toggle", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        return f"{indent_str}▶ {text}\n"
    
    elif block_type == "code":
        content = block.get("code", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        language = content.get("language", "")
        return f"{indent_str}```{language}\n{text}\n{indent_str}```\n"
    
    elif block_type == "quote":
        content = block.get("quote", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        return f"{indent_str}> {text}\n"
    
    elif block_type == "callout":
        content = block.get("callout", {})
        text = extract_text_from_rich_text(content.get("rich_text", []))
        emoji = content.get("icon", {}).get("emoji", "💡")
        return f"{indent_str}{emoji} {text}\n"
    
    elif block_type == "divider":
        return f"{indent_str}---\n"
    
    elif block_type == "table":
        return f"{indent_str}[표]\n"
    
    elif block_type == "column_list":
        return ""  # 컬럼 리스트는 자식 블록으로 처리
    
    elif block_type == "column":
        return ""  # 컬럼은 자식 블록으로 처리
    
    elif block_type == "synced_block":
        return ""  # 동기화 블록은 자식 블록으로 처리
    
    else:
        # 알 수 없는 블록 타입
        return f"{indent_str}[{block_type}]\n"


def extract_script_section(client: Client, blocks: list[dict], section_keywords: list[str] = None) -> str:
    """
    블록 목록에서 미팅 노트 스크립트 섹션을 찾아 추출합니다.
    
    section_keywords: 스크립트 섹션을 식별하는 키워드 목록
    """
    if section_keywords is None:
        section_keywords = [
            "미팅 노트 스크립트",
            "Meeting Notes Script",
            "회의록 스크립트",
            "스크립트",
            "Script",
            "Transcript",
            "녹취록",
            "전체 녹취",
        ]
    
    result_text = []
    in_script_section = False
    script_section_level = 0
    
    def process_blocks(blocks_list: list[dict], indent: int = 0):
        nonlocal in_script_section, script_section_level
        
        for block in blocks_list:
            block_type = block.get("type", "")
            block_id = block.get("id", "")
            
            # 헤딩에서 스크립트 섹션 시작 감지
            if block_type in ("heading_1", "heading_2", "heading_3", "toggle"):
                content = block.get(block_type, {})
                text = extract_text_from_rich_text(content.get("rich_text", []))
                
                # 스크립트 섹션 키워드 확인
                if any(keyword.lower() in text.lower() for keyword in section_keywords):
                    in_script_section = True
                    if block_type == "heading_1":
                        script_section_level = 1
                    elif block_type == "heading_2":
                        script_section_level = 2
                    elif block_type == "heading_3":
                        script_section_level = 3
                    else:
                        script_section_level = 4  # toggle
                    
                    result_text.append(block_to_text(block, indent))
                    
                    # 토글이나 중첩 블록이 있으면 자식 블록도 가져옴
                    if block.get("has_children"):
                        child_blocks = get_nested_blocks(client, block_id)
                        process_blocks(child_blocks, indent + 1)
                    continue
                
                # 다른 동일 레벨 또는 상위 레벨 헤딩이 나오면 스크립트 섹션 종료
                elif in_script_section:
                    current_level = {"heading_1": 1, "heading_2": 2, "heading_3": 3}.get(block_type, 4)
                    if current_level <= script_section_level:
                        in_script_section = False
            
            # 스크립트 섹션 내부의 블록 처리
            if in_script_section:
                result_text.append(block_to_text(block, indent))
                
                # 자식 블록이 있으면 재귀적으로 처리
                if block.get("has_children"):
                    child_blocks = get_nested_blocks(client, block_id)
                    process_blocks(child_blocks, indent + 1)
    
    process_blocks(blocks)
    
    return "".join(result_text).strip()


def extract_all_content(client: Client, blocks: list[dict]) -> str:
    """페이지의 모든 블록을 텍스트로 변환합니다."""
    result_text = []
    
    def process_blocks(blocks_list: list[dict], indent: int = 0):
        for block in blocks_list:
            block_id = block.get("id", "")
            result_text.append(block_to_text(block, indent))
            
            # 자식 블록이 있으면 재귀적으로 처리
            if block.get("has_children"):
                child_blocks = get_nested_blocks(client, block_id)
                process_blocks(child_blocks, indent + 1)
    
    process_blocks(blocks)
    
    return "".join(result_text).strip()


def get_page_title(page: dict) -> str:
    """페이지 제목을 추출합니다."""
    properties = page.get("properties", {})
    
    # 제목 속성 찾기 (일반적으로 "Name" 또는 "제목" 또는 첫 번째 title 타입 속성)
    for prop_name, prop_value in properties.items():
        if prop_value.get("type") == "title":
            title_content = prop_value.get("title", [])
            if title_content:
                return extract_text_from_rich_text(title_content)
    
    return "Untitled"


def sanitize_filename(filename: str) -> str:
    """파일명에 사용할 수 없는 문자를 제거합니다."""
    # 파일명에 사용할 수 없는 문자 제거
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # 공백을 언더스코어로 변경
    sanitized = sanitized.replace(" ", "_")
    # 연속된 언더스코어 제거
    sanitized = re.sub(r'_+', '_', sanitized)
    # 최대 길이 제한
    return sanitized[:100]


def save_script(title: str, content: str, page_id: str, output_dir: Path) -> Path:
    """스크립트를 파일로 저장합니다."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일명 생성
    safe_title = sanitize_filename(title)
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{timestamp}_{safe_title}_{page_id[:8]}.md"
    
    filepath = output_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"페이지 ID: {page_id}\n\n")
        f.write("---\n\n")
        f.write(content)
    
    return filepath


def analyze_page_structure(client: Client, page_id: str):
    """페이지 구조를 분석하여 출력합니다 (디버깅용)."""
    print(f"\n페이지 구조 분석: {page_id}")
    print("=" * 60)
    
    blocks = get_page_blocks(client, page_id)
    
    def print_blocks(blocks_list: list[dict], indent: int = 0):
        for block in blocks_list:
            block_type = block.get("type", "unknown")
            block_id = block.get("id", "")
            has_children = block.get("has_children", False)
            
            # 블록 내용 추출
            content = block.get(block_type, {})
            if isinstance(content, dict) and "rich_text" in content:
                text = extract_text_from_rich_text(content.get("rich_text", []))[:50]
            else:
                text = ""
            
            prefix = "  " * indent
            children_indicator = " [+]" if has_children else ""
            print(f"{prefix}{block_type}{children_indicator}: {text}")
            
            if has_children:
                child_blocks = get_nested_blocks(client, block_id)
                print_blocks(child_blocks, indent + 1)
    
    print_blocks(blocks)


def main():
    """메인 함수."""
    import argparse
    
    parser = argparse.ArgumentParser(description="노션 회의록에서 스크립트를 추출합니다.")
    parser.add_argument("--database-id", default=MEETINGS_DATABASE_ID, 
                       help="회의록 데이터베이스 ID")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR),
                       help="출력 디렉토리")
    parser.add_argument("--page-id", help="특정 페이지만 처리 (테스트용)")
    parser.add_argument("--analyze", action="store_true",
                       help="페이지 구조 분석 모드 (스크립트 추출 없이 구조만 출력)")
    parser.add_argument("--extract-all", action="store_true",
                       help="스크립트 섹션만이 아닌 전체 내용 추출")
    parser.add_argument("--keywords", nargs="+",
                       help="스크립트 섹션을 식별하는 키워드 목록")
    
    args = parser.parse_args()
    
    client = get_notion_client()
    output_dir = Path(args.output_dir)
    
    # 특정 페이지만 처리
    if args.page_id:
        page_id = args.page_id.replace("-", "")
        
        if args.analyze:
            analyze_page_structure(client, page_id)
            return
        
        # 페이지 정보 가져오기
        page = client.pages.retrieve(page_id=page_id)
        title = get_page_title(page)
        print(f"페이지 처리 중: {title}")
        
        blocks = get_page_blocks(client, page_id)
        
        if args.extract_all:
            content = extract_all_content(client, blocks)
        else:
            content = extract_script_section(client, blocks, args.keywords)
        
        if content:
            filepath = save_script(title, content, page_id, output_dir)
            print(f"저장됨: {filepath}")
        else:
            print("스크립트 섹션을 찾을 수 없습니다.")
            print("\n전체 내용을 추출하려면 --extract-all 옵션을 사용하세요.")
            print("또는 --analyze 옵션으로 페이지 구조를 확인하세요.")
        return
    
    # 모든 회의록 페이지 처리
    pages = get_all_meeting_pages(client, args.database_id)
    
    saved_count = 0
    skipped_count = 0
    
    for page in pages:
        page_id = page.get("id", "").replace("-", "")
        title = get_page_title(page)
        
        print(f"\n처리 중: {title}")
        
        if args.analyze:
            analyze_page_structure(client, page_id)
            continue
        
        try:
            blocks = get_page_blocks(client, page_id)
            
            if args.extract_all:
                content = extract_all_content(client, blocks)
            else:
                content = extract_script_section(client, blocks, args.keywords)
            
            if content:
                filepath = save_script(title, content, page_id, output_dir)
                print(f"  저장됨: {filepath}")
                saved_count += 1
            else:
                print(f"  스크립트 섹션 없음 (건너뜀)")
                skipped_count += 1
                
        except Exception as e:
            print(f"  오류: {e}")
            skipped_count += 1
    
    print(f"\n완료: {saved_count}개 저장, {skipped_count}개 건너뜀")
    print(f"출력 디렉토리: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
