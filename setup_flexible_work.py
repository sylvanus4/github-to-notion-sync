#!/usr/bin/env python3
"""
유연근무제 관리 데이터베이스에 모든 사용자 등록
"""

import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

# Configuration
DATABASE_ID = "45343f1a47144cf7983eadba11e4d909"
APPLICATION_MONTH = "2026-01-01"  # 적용 월: 2026년 1월
CHANGE_REQUEST_DATE = "2026-01-12"  # 변경 신청일
START_TIME = "09:00"  # 출근 시간
END_TIME = "18:00"  # 퇴근 시간
DEFAULT_TEAM = "기타"  # 기본 팀


def main():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    # 1. Get all users
    print("🔍 Notion 워크스페이스 사용자 가져오는 중...")
    users_response = notion.users.list()
    users = users_response.get("results", [])

    # Filter only person (not bot)
    person_users = [u for u in users if u.get("type") == "person"]
    print(f"✅ {len(person_users)}명의 사용자를 찾았습니다 (봇 제외)")

    # 2. Get existing entries in database
    print("\n📂 기존 데이터베이스 항목 확인 중...")
    existing_entries = {}
    has_more = True
    start_cursor = None

    while has_more:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            start_cursor=start_cursor,
        )
        for page in response.get("results", []):
            title_prop = page.get("properties", {}).get("담당자", {})
            title_list = title_prop.get("title", [])
            if title_list:
                name = title_list[0].get("plain_text", "")
                existing_entries[name] = page.get("id")

        has_more = response.get("has_more", False)
        start_cursor = response.get("next_cursor")

    print(f"📋 기존 항목: {len(existing_entries)}개")

    # 3. Create entries for each user
    print("\n📝 사용자 등록 시작...")
    created_count = 0
    skipped_count = 0
    error_count = 0

    for user in person_users:
        name = user.get("name", "Unknown")
        email = user.get("person", {}).get("email", "")

        # Skip if already exists
        if name in existing_entries:
            print(f"⏭️  건너뜀 (이미 존재): {name}")
            skipped_count += 1
            continue

        # Create new entry
        try:
            properties = {
                "담당자": {"title": [{"text": {"content": name}}]},
                "팀": {"select": {"name": DEFAULT_TEAM}},
                "적용 월": {"date": {"start": APPLICATION_MONTH}},
                "출근 시간": {"select": {"name": START_TIME}},
                "퇴근 시간": {"select": {"name": END_TIME}},
                "변경 신청일": {"date": {"start": CHANGE_REQUEST_DATE}},
                "비고": {
                    "rich_text": [{"text": {"content": f"이메일: {email}" if email else ""}}]
                },
            }

            notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties=properties,
            )
            print(f"✅ 등록 완료: {name}")
            created_count += 1

        except Exception as e:
            print(f"❌ 등록 실패: {name} - {e}")
            error_count += 1

    # 4. Summary
    print("\n" + "=" * 60)
    print("📊 등록 결과 요약")
    print("=" * 60)
    print(f"  ✅ 새로 등록: {created_count}명")
    print(f"  ⏭️  건너뜀 (이미 존재): {skipped_count}명")
    print(f"  ❌ 등록 실패: {error_count}명")
    print(f"  📋 전체 사용자: {len(person_users)}명")
    print()
    print("📌 설정 정보:")
    print(f"  - 적용 월: 2026년 1월")
    print(f"  - 출근 시간: {START_TIME}")
    print(f"  - 퇴근 시간: {END_TIME}")
    print(f"  - 변경 신청일: {CHANGE_REQUEST_DATE}")
    print(f"  - 기본 팀: {DEFAULT_TEAM}")


if __name__ == "__main__":
    main()
