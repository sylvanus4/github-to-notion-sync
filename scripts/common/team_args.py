"""
Common Team Argument Parser
스크립트에서 공통으로 사용하는 --team 인자 처리 모듈
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any

# 프로젝트 루트를 path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.team_config import (  # noqa: E402
    TeamConfig,
    get_effective_config,
    get_team_field_mappings,
    is_multi_team_mode,
    list_available_teams,
    load_team_config,
    set_environment_from_team_config,
)

logger = logging.getLogger(__name__)


def add_team_argument(parser: argparse.ArgumentParser) -> None:
    """argparse 파서에 --team 인자 추가

    Args:
        parser: ArgumentParser 인스턴스
    """
    parser.add_argument(
        "--team",
        "-t",
        type=str,
        default=None,
        help="팀 ID (예: synos, ragos). 미지정 시 DEFAULT_TEAM 환경변수 또는 레거시 설정 사용",
    )


def get_team_from_args(args: argparse.Namespace) -> str | None:
    """인자에서 팀 ID 추출

    우선순위:
    1. --team 인자
    2. DEFAULT_TEAM 환경변수

    Args:
        args: 파싱된 인자

    Returns:
        팀 ID 또는 None
    """
    if hasattr(args, "team") and args.team:
        return args.team

    return os.environ.get("DEFAULT_TEAM")


def get_team_config_from_args(args: argparse.Namespace) -> TeamConfig | None:
    """인자에서 팀 설정 로드

    Args:
        args: 파싱된 인자

    Returns:
        TeamConfig 또는 None (레거시 모드)
    """
    team_id = get_team_from_args(args)

    if team_id:
        try:
            config = load_team_config(team_id)
            logger.info(f"Loaded team config: {team_id} ({config.team_name})")
            return config
        except FileNotFoundError:
            logger.exception(f"Team '{team_id}' not found")
            available = list_available_teams()
            if available:
                logger.info(f"Available teams: {', '.join(available)}")
            raise

    # 멀티팀 모드에서 팀 미지정
    if is_multi_team_mode():
        available = list_available_teams()
        if available:
            # 첫 번째 팀 사용
            team_id = available[0]
            logger.warning(f"No team specified, using first available: {team_id}")
            return load_team_config(team_id)

    # 레거시 모드
    logger.info("Using legacy mode (no team config)")
    return None


def setup_team_environment(args: argparse.Namespace) -> dict[str, str]:
    """팀 설정에서 환경변수 설정

    Args:
        args: 파싱된 인자

    Returns:
        설정된 환경변수 딕셔너리
    """
    team_id = get_team_from_args(args)

    if team_id:
        env_vars = set_environment_from_team_config(team_id)
        logger.info(f"Set environment variables for team '{team_id}': {list(env_vars.keys())}")
        return env_vars

    return {}


def get_sprint_config_from_args(args: argparse.Namespace) -> dict[str, Any]:
    """인자에서 스프린트 설정 로드 (레거시 형식 호환)

    Args:
        args: 파싱된 인자

    Returns:
        스프린트 설정 딕셔너리
    """
    team_id = get_team_from_args(args)
    return get_effective_config(team_id)


def get_field_mappings_from_args(args: argparse.Namespace) -> dict[str, Any]:
    """인자에서 필드 매핑 로드

    Args:
        args: 파싱된 인자

    Returns:
        필드 매핑 딕셔너리
    """
    team_id = get_team_from_args(args)

    if team_id:
        return get_team_field_mappings(team_id)

    # 레거시: 공통 설정 사용
    from src.utils.team_config import get_config_dir, load_yaml_file

    common_mappings = get_config_dir() / "field_mappings.yml"
    if common_mappings.exists():
        return load_yaml_file(common_mappings)

    return {}


def print_team_info(args: argparse.Namespace) -> None:
    """팀 정보 출력 (디버그용)

    Args:
        args: 파싱된 인자
    """
    team_id = get_team_from_args(args)

    print("=" * 50)
    print("Team Configuration")
    print("=" * 50)

    if team_id:
        try:
            config = load_team_config(team_id)
            print(f"Team ID: {config.team_id}")
            print(f"Team Name: {config.team_name}")
            print(f"GitHub Org: {config.github_org}")
            print(f"GitHub Project: {config.github_project_number}")
            print(f"Current Sprint: {config.current_sprint}")
            print(f"Notion Parent ID: {config.notion_parent_id}")
        except FileNotFoundError:
            print(f"Team '{team_id}' not found")
    elif is_multi_team_mode():
        available = list_available_teams()
        print("Multi-team mode enabled")
        print(f"Available teams: {', '.join(available)}")
    else:
        print("Legacy mode (single team)")

    print("=" * 50)

