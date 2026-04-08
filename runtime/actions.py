"""
Action Tools — 공장 상태를 변경하는 툴

에이전트가 호출하면 실행 결과를 반환한다.
어떤 액션이 호출됐는지는 agent.run()의 tool_calls 로그로 추적한다.
"""

from runtime.registry import register_function


@register_function(
    name="shutdown_line",
    description="지정한 생산 라인을 즉시 차단합니다. 온도 긴급차단 임계값(115°C) 도달 시 사용합니다.",
    parameters={
        "line_id": {"type": "string", "description": "차단할 라인 ID (예: line3)"},
        "reason":  {"type": "string", "description": "차단 사유"},
    },
)
def shutdown_line(line_id: str, reason: str) -> dict:
    return {"ok": True, "line_id": line_id, "status": "shutdown", "reason": reason}


@register_function(
    name="open_valve",
    description="지정한 밸브를 수동으로 완전 개방합니다. 냉각수 유량 회복 시 사용합니다.",
    parameters={
        "valve_id": {"type": "string", "description": "밸브 ID (예: V-07)"},
    },
)
def open_valve(valve_id: str) -> dict:
    return {"ok": True, "valve_id": valve_id, "position": "open"}


@register_function(
    name="create_work_order",
    description="장비 정비 작업 지시를 생성합니다. 점검/교체/세척 등 정비가 필요한 장비에 사용합니다.",
    parameters={
        "equipment_id": {"type": "string", "description": "정비 대상 장비 ID (예: V-07)"},
        "description":  {"type": "string", "description": "정비 내용 설명"},
        "priority":     {"type": "string", "description": "우선순위: critical | high | medium | low"},
    },
)
def create_work_order(equipment_id: str, description: str, priority: str = "high") -> dict:
    return {"ok": True, "equipment_id": equipment_id, "description": description, "priority": priority}


@register_function(
    name="notify_engineer",
    description="담당 엔지니어에게 알림을 발송합니다. 경고/위험 상황 발생 시 반드시 호출해야 합니다.",
    parameters={
        "level":   {"type": "string", "description": "알림 수준: info | warning | critical"},
        "message": {"type": "string", "description": "알림 메시지"},
    },
)
def notify_engineer(level: str, message: str) -> dict:
    return {"ok": True, "sent": True, "level": level, "message": message}


@register_function(
    name="request_restart_approval",
    description="라인 재가동 승인을 요청합니다. 긴급차단 후 재가동 시 설비팀장 승인이 필요합니다.",
    parameters={
        "line_id": {"type": "string", "description": "재가동할 라인 ID"},
        "reason":  {"type": "string", "description": "재가동 사유 및 조치 완료 내용"},
    },
)
def request_restart_approval(line_id: str, reason: str) -> dict:
    return {
        "ok": True,
        "line_id": line_id,
        "approval_status": "pending",
        "message": "설비팀장(내선 201)에게 승인 요청이 전달됐습니다. 승인 전까지 재가동 금지.",
    }
