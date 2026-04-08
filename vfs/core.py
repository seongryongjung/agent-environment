"""
VFS Core — dict 트리 기반 가상 파일 시스템

내부 구조:
    dict  → 디렉토리
    str   → 파일 (내용)

예시:
    _tree = {
        "factory": {
            "sensors": {
                "line3_temp.csv": "timestamp,value\\n..."
            },
            "workspace": {}
        }
    }
"""

from __future__ import annotations
from typing import Union

from .errors import (
    VFSError,
    VFSFileNotFoundError,
    VFSNotADirectoryError,
    VFSIsADirectoryError,
    VFSFileExistsError,
)

# 전역 트리 상태
_tree: dict = {}


# ── 내부 유틸 ────────────────────────────────────────────────

def _parse_path(path: str) -> list[str]:
    """'/factory/sensors/line3.csv' → ['factory', 'sensors', 'line3.csv']"""
    path = path.strip()
    if not path.startswith("/"):
        raise VFSError(f"경로는 /로 시작해야 합니다: {path}")
    return [p for p in path.split("/") if p]


def _get_node(parts: list[str]) -> Union[dict, str]:
    """트리를 탐색해 노드 반환. 없으면 VFSFileNotFoundError."""
    node = _tree
    for i, part in enumerate(parts):
        if not isinstance(node, dict):
            raise VFSNotADirectoryError("/" + "/".join(parts[:i]))
        if part not in node:
            raise VFSFileNotFoundError("/" + "/".join(parts[: i + 1]))
        node = node[part]
    return node


def _get_parent(parts: list[str]) -> tuple[dict, str]:
    """(부모 dict, 마지막 이름) 반환."""
    if not parts:
        raise VFSError("루트 경로에는 부모가 없습니다")
    parent = _get_node(parts[:-1]) if parts[:-1] else _tree
    if not isinstance(parent, dict):
        raise VFSNotADirectoryError("/" + "/".join(parts[:-1]))
    return parent, parts[-1]


def _deep_copy(obj: Union[dict, str]) -> Union[dict, str]:
    if isinstance(obj, dict):
        return {k: _deep_copy(v) for k, v in obj.items()}
    return obj


# ── 공개 API ─────────────────────────────────────────────────

def reset(initial_tree: dict = None) -> None:
    """VFS를 초기화한다. 시나리오 로드 시 호출."""
    global _tree
    _tree = _deep_copy(initial_tree) if initial_tree else {}


def read_file(path: str) -> str:
    """파일 내용을 반환한다."""
    parts = _parse_path(path)
    node = _get_node(parts)
    if isinstance(node, dict):
        raise VFSIsADirectoryError(path)
    return node


def write_file(path: str, content: str) -> None:
    """파일을 쓴다. 없으면 생성, 있으면 덮어쓴다."""
    parts = _parse_path(path)
    parent, name = _get_parent(parts)
    if name in parent and isinstance(parent[name], dict):
        raise VFSIsADirectoryError(path)
    parent[name] = content


def list_dir(path: str) -> list[str]:
    """디렉토리 내 항목 이름을 정렬해서 반환한다."""
    parts = _parse_path(path) if path != "/" else []
    node = _get_node(parts) if parts else _tree
    if not isinstance(node, dict):
        raise VFSNotADirectoryError(path)
    return sorted(node.keys())


def mkdir(path: str, parents: bool = False) -> None:
    """디렉토리를 생성한다. parents=True면 중간 경로도 함께 생성."""
    parts = _parse_path(path)
    if parents:
        node = _tree
        for i, part in enumerate(parts):
            if part not in node:
                node[part] = {}
            elif not isinstance(node[part], dict):
                raise VFSNotADirectoryError("/" + "/".join(parts[: i + 1]))
            node = node[part]
    else:
        parent, name = _get_parent(parts)
        if name in parent:
            raise VFSFileExistsError(path)
        parent[name] = {}


def delete(path: str) -> None:
    """파일 또는 디렉토리를 삭제한다."""
    parts = _parse_path(path)
    parent, name = _get_parent(parts)
    if name not in parent:
        raise VFSFileNotFoundError(path)
    del parent[name]


def move(src: str, dst: str) -> None:
    """파일 또는 디렉토리를 이동/이름변경한다."""
    src_parts = _parse_path(src)
    dst_parts = _parse_path(dst)

    src_parent, src_name = _get_parent(src_parts)
    if src_name not in src_parent:
        raise VFSFileNotFoundError(src)

    dst_parent, dst_name = _get_parent(dst_parts)
    dst_parent[dst_name] = src_parent.pop(src_name)


def exists(path: str) -> bool:
    """경로가 존재하면 True."""
    try:
        parts = _parse_path(path)
        if not parts:
            return True
        _get_node(parts)
        return True
    except (VFSFileNotFoundError, VFSNotADirectoryError):
        return False


def is_file(path: str) -> bool:
    """파일이면 True."""
    try:
        return isinstance(_get_node(_parse_path(path)), str)
    except (VFSFileNotFoundError, VFSNotADirectoryError):
        return False


def is_dir(path: str) -> bool:
    """디렉토리면 True."""
    try:
        parts = _parse_path(path)
        return isinstance(_get_node(parts) if parts else _tree, dict)
    except (VFSFileNotFoundError, VFSNotADirectoryError):
        return False


def tree(path: str = "/", _prefix: str = "") -> str:
    """디렉토리 구조를 트리 문자열로 반환한다. 디버깅용."""
    parts = _parse_path(path) if path != "/" else []
    node = _get_node(parts) if parts else _tree
    if not isinstance(node, dict):
        return path

    lines = []
    items = sorted(node.keys())
    for i, name in enumerate(items):
        connector = "└── " if i == len(items) - 1 else "├── "
        child = node[name]
        lines.append(_prefix + connector + name)
        if isinstance(child, dict):
            extension = "    " if i == len(items) - 1 else "│   "
            sub_path = path.rstrip("/") + "/" + name
            sub = tree(sub_path, _prefix + extension)
            if sub:
                lines.append(sub)
    return "\n".join(lines)
