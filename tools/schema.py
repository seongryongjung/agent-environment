"""
Tool Schema 정의

VFS tools (데이터 접근) + Runtime tools (액션)을 LLM에게 노출한다.

VFS tools:     read_file, list_dir, write_file
Runtime tools: generate_report
"""

VFS_TOOLS: list[dict] = [
    {
        "name": "read_file",
        "description": "파일 내용을 읽어 반환합니다. 센서 CSV, 매뉴얼, 보고서 등 모든 파일에 사용합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "읽을 파일의 절대 경로",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_dir",
        "description": "디렉토리의 파일/폴더 목록을 반환합니다. 어떤 데이터가 있는지 탐색할 때 사용합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "목록을 볼 디렉토리 경로",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "파일을 씁니다. 파일이 없으면 생성하고 있으면 덮어씁니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "path":    {"type": "string", "description": "쓸 파일의 절대 경로"},
                "content": {"type": "string", "description": "파일에 쓸 내용"},
            },
            "required": ["path", "content"],
        },
    },
]


def get_all_schemas() -> list[dict]:
    """VFS tool schema + Runtime tool schema를 합쳐서 반환한다."""
    from runtime.registry import get_schemas
    return VFS_TOOLS + get_schemas()
