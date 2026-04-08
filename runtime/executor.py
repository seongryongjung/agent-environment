"""
함수 실행기

tool call 이름 + args를 받아 등록된 함수를 실행하고 결과를 반환한다.
"""

import json
from runtime.registry import get_function, list_names


def call(name: str, args: dict) -> dict:
    """
    등록된 가상 함수를 호출한다.

    Args:
        name: 함수 이름
        args: 파라미터 dict

    Returns:
        {"ok": True, "result": ...} 또는 {"ok": False, "error": ...}
    """
    fn = get_function(name)

    if fn is None:
        available = ", ".join(list_names())
        return {
            "ok": False,
            "error": f"함수를 찾을 수 없습니다: '{name}'. 사용 가능: {available}",
        }

    try:
        result = fn(**args)
        return {"ok": True, "result": result}
    except TypeError as e:
        return {"ok": False, "error": f"파라미터 오류: {e}"}
    except Exception as e:
        return {"ok": False, "error": f"실행 오류: {e}"}


def call_json(name: str, args_json: str) -> dict:
    """JSON 문자열 args를 받아 call()을 호출한다. LLM 연동 시 편의용."""
    try:
        args = json.loads(args_json)
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"args JSON 파싱 실패: {e}"}
    return call(name, args)
