"""
State DB — 변경 가능한 공장 장비/라인 상태

VFS는 파일(문서) 저장소고, State DB는 장비/라인의 실시간 상태를 담는다.
에이전트의 action tool 호출로 상태가 변경되며, task_evaluator가 최종 상태를 검증한다.
"""

import copy
from datetime import datetime

_state: dict = {}
_action_log: list[dict] = []


def reset(initial_state: dict) -> None:
    """태스크 시작 시 상태를 초기화한다."""
    global _state, _action_log
    _state = copy.deepcopy(initial_state)
    _action_log = []


def get_all() -> dict:
    return copy.deepcopy(_state)


def get(key: str, default=None):
    """점(.) 구분 경로로 값 조회. 예: get('lines.line3.status')"""
    keys = key.split(".")
    node = _state
    for k in keys:
        if not isinstance(node, dict) or k not in node:
            return default
        node = node[k]
    return node


def set(key: str, value) -> None:
    """점(.) 구분 경로로 값 설정. 예: set('lines.line3.status', 'shutdown')"""
    keys = key.split(".")
    node = _state
    for k in keys[:-1]:
        node = node.setdefault(k, {})
    node[keys[-1]] = value


def append_to_list(key: str, item) -> None:
    """리스트 항목에 아이템 추가. 키가 없으면 빈 리스트로 초기화."""
    existing = get(key) or []
    existing.append(item)
    set(key, existing)


def append_log(action: str, args: dict, result: dict) -> None:
    """액션 실행 이력을 기록한다. action tool에서 호출한다."""
    _action_log.append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "args": args,
        "result": result,
    })


def get_action_log() -> list[dict]:
    """전체 액션 실행 이력 반환."""
    return list(_action_log)


def get_called_actions() -> list[str]:
    """실행된 액션 이름 목록 (중복 포함, 순서 유지)."""
    return [entry["action"] for entry in _action_log]
