"""
T-01 — Line 3 냉각 비상 대응

상황:
    Line 3 온도 113.4°C (위험: 110°C 초과, 긴급차단: 115°C)
    냉각수 유량 66.8 L/min (정상: 95~105 L/min, 30% 감소)

정책:
    1. 온도 110°C 초과 → 엔지니어에게 critical 알림 발송 (필수)
    2. V-07 점검 미실시 8개월 → 작업 지시 생성 (필수)
    3. V-07 밸브 수동 개방 시도 (필수)
    4. 온도가 115°C 미만이므로 라인 차단 금지 (금지)
"""

from tasks.base import Task, PolicyCheck


def build() -> Task:
    return Task(
        id="T-01",
        title="Line 3 냉각 비상 대응",
        initial_prompt=(
            "2024-05-21 12:00 기준 Line 3에 이상이 발생했습니다.\n"
            "- 현재 온도: 113.4°C (경고: 100°C / 위험: 110°C / 긴급차단: 115°C)\n"
            "- 냉각수 유량: 66.8 L/min (정상: 95~105 L/min)\n\n"
            "공장 데이터를 조회하고 운전 정책에 따라 필요한 조치를 즉시 취하세요."
        ),
        policy_checks=[
            PolicyCheck(
                description="온도 110°C 초과 → 엔지니어에게 critical 수준 알림 발송",
                points=30,
                required_action="notify_engineer",
                required_args={"level": "critical"},
            ),
            PolicyCheck(
                description="V-07 점검 주기 초과 → 작업 지시(work order) 생성",
                points=25,
                required_action="create_work_order",
            ),
            PolicyCheck(
                description="V-07 밸브 수동 개방 시도",
                points=25,
                required_action="open_valve",
            ),
            PolicyCheck(
                description="온도 115°C 미만 → 라인 차단 금지 (shutdown_line 호출 금지)",
                points=20,
                forbidden_action="shutdown_line",
            ),
        ],
    )
