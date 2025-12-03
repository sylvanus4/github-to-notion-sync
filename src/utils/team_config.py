"""
Team Configuration Loader
팀별 설정 파일을 로드하고 관리하는 유틸리티 모듈

지원하는 설정 파일:
- config/teams/{team-id}/sprint_config.yml - 팀 스프린트 설정 (필수)
- config/teams/{team-id}/field_mappings.yml - 팀 필드 매핑 (선택, 없으면 공통 사용)
"""

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# 기본 경로
DEFAULT_CONFIG_DIR = Path("config")
TEAMS_DIR = DEFAULT_CONFIG_DIR / "teams"


@dataclass
class TeamConfig:
    """팀 설정 데이터 클래스"""

    # 팀 기본 정보
    team_id: str
    team_name: str
    description: str = ""
    enabled: bool = True

    # GitHub 설정
    github_org: str = ""
    github_project_number: int = 0

    # Notion 설정
    notion_database_id: str = ""

    # 스프린트 설정
    current_sprint: str = ""
    notion_parent_id: str = ""
    sprint_checker_parent_id: str = ""
    daily_scrum_parent_id: str = ""
    qa_database_id: str = ""

    # 원본 설정 데이터 (추가 필드 접근용)
    raw_config: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict, team_id: str) -> "TeamConfig":
        """딕셔너리에서 TeamConfig 생성"""
        team_info = data.get("team") or {}
        github_info = data.get("github") or {}
        notion_info = data.get("notion") or {}
        sprint_info = data.get("sprint") or {}

        return cls(
            team_id=team_info.get("id", team_id),
            team_name=team_info.get("name", team_id),
            description=team_info.get("description", ""),
            enabled=team_info.get("enabled", True),
            github_org=github_info.get("org", ""),
            github_project_number=github_info.get("project_number", 0),
            notion_database_id=notion_info.get("database_id", ""),
            current_sprint=sprint_info.get("current", ""),
            notion_parent_id=sprint_info.get("notion_parent_id", ""),
            sprint_checker_parent_id=sprint_info.get("sprint_checker_parent_id", ""),
            daily_scrum_parent_id=sprint_info.get("daily_scrum_parent_id", ""),
            qa_database_id=sprint_info.get("qa_database_id", ""),
            raw_config=data,
        )


def get_config_dir() -> Path:
    """설정 디렉토리 경로 반환 (환경변수로 오버라이드 가능)"""
    config_dir = os.environ.get("CONFIG_DIR", str(DEFAULT_CONFIG_DIR))
    return Path(config_dir)


def get_teams_dir() -> Path:
    """팀 설정 디렉토리 경로 반환"""
    return get_config_dir() / "teams"


def is_multi_team_mode() -> bool:
    """멀티팀 모드인지 확인 (config/teams/ 디렉토리 존재 여부)"""
    teams_dir = get_teams_dir()
    if not teams_dir.exists():
        return False

    # teams 디렉토리에 실제 팀 설정이 있는지 확인
    for item in teams_dir.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            config_file = item / "sprint_config.yml"
            if config_file.exists():
                return True

    return False


def list_available_teams() -> list[str]:
    """사용 가능한 팀 ID 목록 반환"""
    teams_dir = get_teams_dir()
    if not teams_dir.exists():
        return []

    teams = []
    for item in teams_dir.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            config_file = item / "sprint_config.yml"
            if config_file.exists():
                teams.append(item.name)

    return sorted(teams)


def load_yaml_file(file_path: Path) -> dict[str, Any]:
    """YAML 파일 로드"""
    if not file_path.exists():
        logger.warning(f"Config file not found: {file_path}")
        return {}

    try:
        with open(file_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            result: dict[str, Any] = data if data else {}
            return result
    except yaml.YAMLError as e:
        logger.exception(f"Failed to parse YAML file {file_path}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Failed to load config file {file_path}: {e}")
        raise


def load_team_config(team_id: str) -> TeamConfig:
    """팀 설정 로드

    Args:
        team_id: 팀 식별자 (예: 'synos', 'ragos')

    Returns:
        TeamConfig 객체

    Raises:
        FileNotFoundError: 팀 설정 파일이 없는 경우
        ValueError: 팀 ID가 유효하지 않은 경우
    """
    if not team_id:
        raise ValueError("Team ID cannot be empty")

    teams_dir = get_teams_dir()
    team_dir = teams_dir / team_id

    if not team_dir.exists():
        msg = f"Team directory not found: {team_dir}"
        raise FileNotFoundError(msg)

    config_file = team_dir / "sprint_config.yml"
    if not config_file.exists():
        msg = f"Team config file not found: {config_file}"
        raise FileNotFoundError(msg)

    data = load_yaml_file(config_file)
    return TeamConfig.from_dict(data, team_id)


def get_team_sprint_config(team_id: str) -> dict:
    """팀 스프린트 설정 반환 (레거시 형식 호환)

    Args:
        team_id: 팀 식별자

    Returns:
        스프린트 설정 딕셔너리 (기존 sprint_config.yml 형식과 호환)
    """
    config = load_team_config(team_id)

    # 레거시 형식으로 변환
    return {
        "current_sprint": config.current_sprint,
        "notion_parent_id": config.notion_parent_id,
        "sprint_checker_parent_id": config.sprint_checker_parent_id,
        "daily_scrum_parent_id": config.daily_scrum_parent_id,
        "qa_database_id": config.qa_database_id,
        # 추가 정보
        "team_id": config.team_id,
        "team_name": config.team_name,
        "github_org": config.github_org,
        "github_project_number": config.github_project_number,
    }


def get_team_field_mappings(team_id: str) -> dict:
    """팀 필드 매핑 설정 반환

    팀별 field_mappings.yml이 있으면 로드하고,
    없으면 공통 config/field_mappings.yml 로드

    Args:
        team_id: 팀 식별자

    Returns:
        필드 매핑 딕셔너리
    """
    teams_dir = get_teams_dir()
    team_field_mappings = teams_dir / team_id / "field_mappings.yml"

    if team_field_mappings.exists():
        logger.debug(f"Loading team-specific field mappings: {team_field_mappings}")
        return load_yaml_file(team_field_mappings)

    # 팀별 설정이 없으면 공통 설정 사용
    common_field_mappings = get_config_dir() / "field_mappings.yml"
    if common_field_mappings.exists():
        logger.debug(f"Loading common field mappings: {common_field_mappings}")
        return load_yaml_file(common_field_mappings)

    logger.warning("No field mappings found")
    return {}


def get_team_user_mappings(team_id: str) -> dict[str, str]:
    """팀 사용자 매핑 반환 (GitHub username → Notion user ID)

    Args:
        team_id: 팀 식별자

    Returns:
        사용자 매핑 딕셔너리
    """
    field_mappings = get_team_field_mappings(team_id)

    # 팀별 field_mappings.yml에서 user_mappings 확인
    user_mappings: dict[str, str] = field_mappings.get("user_mappings", {})

    # 또는 github_to_notion.assignees.value_mappings에서 확인 (레거시 형식)
    if not user_mappings:
        github_to_notion = field_mappings.get("github_to_notion", {})
        assignees = github_to_notion.get("assignees", {})
        user_mappings = assignees.get("value_mappings", {})

    return user_mappings


def load_legacy_config() -> dict:
    """레거시 설정 로드 (config/sprint_config.yml)

    멀티팀 모드가 아닌 경우 기존 설정 파일 사용

    Returns:
        레거시 스프린트 설정 딕셔너리
    """
    config_dir = get_config_dir()
    legacy_config = config_dir / "sprint_config.yml"

    if not legacy_config.exists():
        logger.warning(f"Legacy config file not found: {legacy_config}")
        return {}

    return load_yaml_file(legacy_config)


def get_effective_config(team_id: str | None = None) -> dict:
    """효과적인 설정 반환 (팀 ID가 있으면 팀 설정, 없으면 레거시)

    Args:
        team_id: 팀 식별자 (None이면 레거시 또는 기본 팀)

    Returns:
        설정 딕셔너리
    """
    # 팀 ID가 지정된 경우
    if team_id:
        return get_team_sprint_config(team_id)

    # 멀티팀 모드인지 확인
    if is_multi_team_mode():
        # DEFAULT_TEAM 환경변수 확인
        default_team = os.environ.get("DEFAULT_TEAM")
        if default_team:
            try:
                return get_team_sprint_config(default_team)
            except FileNotFoundError:
                logger.warning(f"Default team '{default_team}' not found, falling back to legacy")

        # 사용 가능한 첫 번째 팀 사용
        available_teams = list_available_teams()
        if available_teams:
            logger.info(f"No team specified, using first available: {available_teams[0]}")
            return get_team_sprint_config(available_teams[0])

    # 레거시 설정 사용
    logger.info("Using legacy config")
    return load_legacy_config()


def set_environment_from_team_config(team_id: str) -> dict[str, str]:
    """팀 설정에서 환경변수 설정

    워크플로우나 스크립트에서 팀 설정을 환경변수로 설정할 때 사용

    Args:
        team_id: 팀 식별자

    Returns:
        설정된 환경변수 딕셔너리
    """
    config = load_team_config(team_id)
    env_vars: dict[str, Any] = {}

    # GitHub 설정
    if config.github_org:
        env_vars["GH_ORG"] = config.github_org
    if config.github_project_number:
        env_vars["GH_PROJECT_NUMBER"] = str(config.github_project_number)

    # Notion 설정
    if config.notion_database_id:
        env_vars["NOTION_DB_ID"] = config.notion_database_id

    # 스프린트 설정
    if config.current_sprint:
        env_vars["SPRINT_FILTER"] = config.current_sprint
    if config.notion_parent_id:
        env_vars["NOTION_PARENT_ID"] = config.notion_parent_id
    if config.sprint_checker_parent_id:
        env_vars["SPRINT_CHECKER_PARENT_ID"] = config.sprint_checker_parent_id
    if config.daily_scrum_parent_id:
        env_vars["DAILY_SCRUM_PARENT_ID"] = config.daily_scrum_parent_id

    # 환경변수 설정
    for key, value in env_vars.items():
        os.environ[key] = value

    return env_vars
