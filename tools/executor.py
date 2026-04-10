"""
Tool Executor — VFS / Runtime 라우터

tool call 이름을 보고 VFS 함수 또는 Runtime 함수로 라우팅한다.

    read_file / list_dir / write_file  → vfs
    generate_report                    → runtime
"""

import json

import vfs
from vfs.errors import VFSError
import runtime


_VFS_DISPATCH: dict[str, callable] = {
    "read_file":  lambda args: vfs.read_file(**args),
    "list_dir":   lambda args: vfs.list_dir(**args),
    "write_file": lambda args: (vfs.write_file(**args), "ok")[1],
}





def execute(name: str, args: dict) -> dict:
    """
    tool 이름과 args를 받아 적절한 레이어로 라우팅하고 결과를 반환한다.

    Returns:
        {"ok": True, "result": ...} 또는 {"ok": False, "error": ...}
    """
    if name in _VFS_DISPATCH:
        return _execute_vfs(name, args)
    else:
        return runtime.call(name, args)


def _execute_vfs(name: str, args: dict) -> dict:
    try:
        result = _VFS_DISPATCH[name](args)
        return {"ok": True, "result": result}
    except VFSError as e:
        return {"ok": False, "error": str(e)}
    except TypeError as e:
        return {"ok": False, "error": f"파라미터 오류: {e}"}


def execute_from_llm_response(tool_name: str, tool_args: dict) -> str:
    """
    LLM의 tool call을 실행하고 결과를 문자열로 반환한다.
    agent/loop.py에서 tool_result 메시지 생성 시 사용.
    """
    result = execute(tool_name, tool_args)
    return json.dumps(result, ensure_ascii=False, indent=2)
