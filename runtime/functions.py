"""
가상 산업 도구 함수 구현

LLM이 직접 할 수 없는 액션만 구현한다.
데이터 조회/분석은 VFS tools(read_file, list_dir)로 LLM이 직접 수행한다.
"""

from datetime import datetime

import vfs
from runtime.registry import register_function


# ── 보고서 함수 ───────────────────────────────────────────────

@register_function(
    name="generate_report",
    description="분석 내용을 바탕으로 보고서 파일을 /factory/workspace/에 생성합니다.",
    parameters={
        "title":   {"type": "string", "description": "보고서 제목"},
        "content": {"type": "string", "description": "보고서 본문 내용"},
    },
)
def generate_report(title: str, content: str) -> dict:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = title.replace(" ", "_").replace("/", "-")
    path = f"/factory/workspace/report_{safe_title}_{timestamp}.txt"

    body = f"{'=' * 60}\n{title}\n생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 60}\n\n{content}"
    vfs.write_file(path, body)

    return {
        "ok": True,
        "path": path,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

