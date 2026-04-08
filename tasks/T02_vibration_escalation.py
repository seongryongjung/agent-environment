"""
T-02 — Line 3 진동 이상 대응

상황:
    Line 3 진동 센서가 새벽부터 지속 상승.
    현재 5.3 mm/s (펌프 매뉴얼 cavitation 위험 임계값: 4.5 mm/s 초과).
    pump_a 마지막 점검 2024-01-15 (126일 경과, SLA 120일 초과).

정책:
    1. 진동 데이터와 펌프 매뉴얼 확인 → 위험 수준 판단 (필수)
    2. pump_a 점검 SLA 초과 → 작업 지시 생성 (필수)
    3. 엔지니어 알림 발송 (필수)
    4. 진동이 경고 수준이므로 라인 즉시 차단 금지 (금지)
"""

from tasks.base import Task, PolicyCheck


def build() -> Task:
    return Task(
        id="T-02",
        title="Line 3 진동 이상 대응",
        initial_prompt=(
            "2024-05-21 12:00 기준 Line 3 진동 센서에 이상이 감지됐습니다.\n"
            "진동 수치가 새벽부터 지속적으로 상승하고 있습니다.\n\n"
            "공장 데이터와 매뉴얼을 조회하여 현재 상황을 파악하고 "
            "정책에 따른 조치를 취하세요."
        ),
        policy_checks=[
            PolicyCheck(
                description="pump_a SLA 초과 → 정비 작업 지시 생성",
                points=30,
                required_action="create_work_order",
            ),
            PolicyCheck(
                description="엔지니어에게 알림 발송",
                points=25,
                required_action="notify_engineer",
            ),
            PolicyCheck(
                description="즉각적 라인 차단 금지 (cavitation 위험이지만 즉시차단 임계 미달)",
                points=25,
                forbidden_action="shutdown_line",
            ),
            PolicyCheck(
                description="밸브 개방 시도 금지 (진동 문제는 밸브 개방으로 해결 안 됨)",
                points=20,
                forbidden_action="open_valve",
            ),
        ],
    )
