"""
Factory Data Loader

factory_data/ 디렉토리의 파일들을 읽어 VFS를 초기화한다.
시나리오와 무관하게 항상 동일한 공장 데이터가 VFS에 올라간다.

사용법:
    from factory_data.loader import load_factory

    load_factory()          # VFS 초기화
    scenario = load_scenario("A-01")  # 질문 + 채점 기준만 로드
"""

from pathlib import Path
import vfs

_FACTORY_ROOT = Path(__file__).parent


def load_factory() -> None:
    """
    factory_data/ 디렉토리를 재귀 탐색하여 VFS를 초기화한다.
    기존 VFS 상태는 완전히 교체된다.
    """
    tree = _build_tree(_FACTORY_ROOT)
    vfs.reset({"factory": tree})

    # 에이전트 작업공간 보장
    if not vfs.exists("/factory/workspace"):
        vfs.mkdir("/factory/workspace", parents=True)


def _build_tree(directory: Path) -> dict:
    """디렉토리를 재귀 탐색해 dict 트리로 변환한다."""
    tree = {}
    for item in sorted(directory.iterdir()):
        if item.name.startswith("_") or item.suffix == ".py":
            continue  # __init__.py, loader.py 등 스킵
        if item.is_dir():
            tree[item.name] = _build_tree(item)
        elif item.is_file():
            tree[item.name] = item.read_text(encoding="utf-8")
    return tree
