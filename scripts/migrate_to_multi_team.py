#!/usr/bin/env python3
"""
Migrate to Multi-Team Configuration
기존 단일 팀 설정을 멀티 팀 구조로 마이그레이션하는 스크립트

사용법:
    python scripts/migrate_to_multi_team.py --team synos [--dry-run]

이 스크립트는:
1. config/teams/{team}/ 디렉토리를 생성합니다
2. 기존 config/sprint_config.yml을 새 형식으로 변환합니다
3. 기존 config/field_mappings.yml에서 팀별 사용자 매핑을 분리합니다
"""

import argparse
import shutil
import sys
from pathlib import Path

import yaml

# 프로젝트 루트
project_root = Path(__file__).parent.parent
config_dir = project_root / "config"


def load_yaml(file_path: Path) -> dict:
    """YAML 파일 로드"""
    if not file_path.exists():
        return {}
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_yaml(file_path: Path, data: dict, dry_run: bool = False) -> None:
    """YAML 파일 저장"""
    if dry_run:
        print(f"\n[DRY RUN] Would create: {file_path}")
        print("=" * 60)
        print(yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False))
        print("=" * 60)
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"✅ Created: {file_path}")


def convert_sprint_config(legacy_config: dict, team_id: str) -> dict:
    """기존 sprint_config.yml을 새 형식으로 변환"""
    return {
        "team": {
            "id": team_id,
            "name": team_id.title(),  # 첫 글자 대문자
            "description": f"{team_id.title()} 팀 GitHub-Notion 동기화",
            "enabled": True,
        },
        "github": {
            "org": "ThakiCloud",  # 기본값, 환경변수로 오버라이드 가능
            "project_number": 0,  # 수동 입력 필요
        },
        "sprint": {
            "current": legacy_config.get("current_sprint", ""),
            "notion_parent_id": legacy_config.get("notion_parent_id", ""),
            "sprint_checker_parent_id": legacy_config.get("sprint_checker_parent_id", ""),
            "daily_scrum_parent_id": legacy_config.get("daily_scrum_parent_id", ""),
            "qa_database_id": legacy_config.get("qa_database_id", ""),
        },
    }


def extract_user_mappings(field_mappings: dict) -> dict:
    """field_mappings.yml에서 사용자 매핑 추출"""
    user_mappings = {}
    display_names = {}

    # github_to_notion.assignees.value_mappings에서 추출
    github_to_notion = field_mappings.get("github_to_notion", {})
    assignees = github_to_notion.get("assignees", {})
    user_mappings = assignees.get("value_mappings", {})

    # github_to_display_name에서 추출
    display_names = field_mappings.get("github_to_display_name", {})

    return {
        "user_mappings": user_mappings,
        "display_names": display_names,
    }


def migrate_to_multi_team(team_id: str, dry_run: bool = False) -> bool:
    """단일 팀 설정을 멀티 팀 구조로 마이그레이션"""
    print(f"🚀 Migrating to multi-team structure for team: {team_id}")
    print(f"   Dry run: {dry_run}")

    # 1. 기존 설정 로드
    legacy_sprint = load_yaml(config_dir / "sprint_config.yml")
    legacy_field_mappings = load_yaml(config_dir / "field_mappings.yml")

    if not legacy_sprint:
        print("❌ No legacy sprint_config.yml found")
        return False

    # 2. 팀 디렉토리 생성
    team_dir = config_dir / "teams" / team_id
    if not dry_run:
        team_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {team_dir}")

    # 3. sprint_config.yml 변환
    new_sprint_config = convert_sprint_config(legacy_sprint, team_id)
    save_yaml(team_dir / "sprint_config.yml", new_sprint_config, dry_run)

    # 4. field_mappings.yml에서 사용자 매핑 추출
    user_data = extract_user_mappings(legacy_field_mappings)
    if user_data["user_mappings"] or user_data["display_names"]:
        team_field_mappings = {
            "# Team Field Mappings": None,  # 주석용
            "user_mappings": user_data["user_mappings"],
            "display_names": user_data["display_names"],
        }
        # 주석 제거
        del team_field_mappings["# Team Field Mappings"]
        team_field_mappings_clean = {
            "user_mappings": user_data["user_mappings"],
            "display_names": user_data["display_names"],
        }
        save_yaml(team_dir / "field_mappings.yml", team_field_mappings_clean, dry_run)

    # 5. 요약
    print("\n" + "=" * 60)
    print("📋 Migration Summary")
    print("=" * 60)
    print(f"Team: {team_id}")
    print(f"Sprint Config: {team_dir / 'sprint_config.yml'}")
    print(f"Field Mappings: {team_dir / 'field_mappings.yml'}")
    print(f"Current Sprint: {new_sprint_config['sprint']['current']}")
    print(f"User Mappings: {len(user_data['user_mappings'])} users")

    print("\n⚠️  Next Steps:")
    print("1. GitHub Project Number를 팀 설정에 입력하세요")
    print("2. 필요한 경우 Notion ID들을 확인하세요")
    print("3. 워크플로우에서 --team 옵션으로 테스트하세요")

    if dry_run:
        print("\n[DRY RUN] 실제 파일은 생성되지 않았습니다")
        print("실제 마이그레이션을 수행하려면 --dry-run 옵션을 제거하세요")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Migrate to multi-team configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview migration (dry run)
  python scripts/migrate_to_multi_team.py --team synos --dry-run

  # Perform actual migration
  python scripts/migrate_to_multi_team.py --team synos
        """,
    )

    parser.add_argument(
        "--team",
        required=True,
        help="Team ID (e.g., synos, ragos, cloud-infra)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without creating files",
    )

    args = parser.parse_args()

    success = migrate_to_multi_team(args.team, args.dry_run)

    if success:
        print("\n✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Migration failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

