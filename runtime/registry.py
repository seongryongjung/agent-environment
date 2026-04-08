"""
함수 등록소

@register_function 데코레이터로 가상 함수를 등록한다.
등록된 함수는 tool schema와 실제 구현체를 함께 보관한다.
"""

from typing import Callable

_registry: dict[str, dict] = {}


def register_function(
    name: str,
    description: str,
    parameters: dict,
    required: list[str] = None,
):
    """
    함수를 등록하는 데코레이터.

    Args:
        name:        tool 이름 (LLM이 호출할 때 사용)
        description: tool 설명 (LLM에게 보여지는 텍스트)
        parameters:  파라미터 정의 {"param": {"type": ..., "description": ...}}
        required:    필수 파라미터 목록 (None이면 전체 필수)
    """
    def decorator(fn: Callable) -> Callable:
        _registry[name] = {
            "fn": fn,
            "schema": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required if required is not None else list(parameters.keys()),
                },
            },
        }
        return fn
    return decorator


def get_schemas() -> list[dict]:
    """등록된 모든 함수의 tool schema를 반환한다."""
    return [entry["schema"] for entry in _registry.values()]


def get_function(name: str) -> "Callable | None":
    """이름으로 함수를 반환한다. 없으면 None."""
    return _registry.get(name, {}).get("fn")


def list_names() -> list[str]:
    """등록된 함수 이름 목록을 반환한다."""
    return list(_registry.keys())
