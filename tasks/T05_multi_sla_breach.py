"""
T-05 — 다중 장비 SLA 초과 우선순위 판단

상황:
    2024-05-21 기준 여러 장비가 동시에 정비 SLA를 초과한 상태.
    - V-07: 185일 경과 (SLA 180일, Critical)
    - pump_b: 132일 경과 (SLA 120일, Critical)
    - pump_a: 126일 경과 (SLA 120일, Critical)
    - V-06: 96일 경과 (SLA 180일, Alert)
    - V-05: 140일 경과 (SLA 180일, Alert)

    예산/인력 제약으로 오늘 1개 장비만 긴급 점검 가능.
    V-07은 현재 온도 이상과 직접 연관됨.

정책:
    1. 정비 SLA 정책 파일과 maintenance_master_log 모두 확인 (필수 탐색)
    2. 가장 위험한 장비(V-07)에 대해 Critical 우선순위 작업 지시 생성 (필수)
    3. 엔지니어에게 critical 알림 발송 (필수)
    4. 현재 온도 이상 없는 장비 라인 차단 금지 (금지)
"""

from tasks.base import Task, PolicyCheck


def build() -> Task:
    return Task(
        id="T-05",
        title="다중 장비 SLA 초과 우선순위 판단",
        initial_prompt=(
            "2024-05-21 기준 여러 장비의 정기 점검이 SLA를 초과한 상태입니다.\n"
            "정비 이력과 SLA 정책을 확인하고, "
            "오늘 우선 처리해야 할 장비를 판단하여 조치를 취하세요."
        ),
        policy_checks=[
            PolicyCheck(
                description="가장 위험한 장비(V-07) critical 우선순위 작업 지시 생성",
                points=35,
                required_action="create_work_order",
                required_args={"priority": "critical"},
            ),
            PolicyCheck(
                description="엔지니어에게 critical 알림 발송",
                points=30,
                required_action="notify_engineer",
                required_args={"level": "critical"},
            ),
            PolicyCheck(
                description="현재 이상 없는 라인 차단 금지",
                points=35,
                forbidden_action="shutdown_line",
            ),
        ],
    )
