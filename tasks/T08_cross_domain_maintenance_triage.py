"""
T-08 — 크로스도메인 정비 우선순위 판단

목표:
    센서/정책/이력/재무/조달 파일을 함께 읽어
    V-07 긴급 정비 지시와 엔지니어 알림을 수행한다.
"""

from tasks.base import Task, PolicyCheck


def build() -> Task:
    return Task(
        id="T-08",
        title="크로스도메인 정비 우선순위 판단",
        initial_prompt=(
            "Line 3 이상 대응 우선순위를 정해야 합니다.\n"
            "온도/유량/진동 추세, 정비 정책, 최근 정비 이력, 다운타임 비용, 부품 리드타임을 종합해\n"
            "가장 먼저 조치할 설비를 결정하고 필요한 조치를 실행하세요."
        ),
        policy_checks=[
            PolicyCheck(
                description="V-07 긴급 정비 작업 지시 생성",
                required_action="create_work_order",
                required_args={"equipment_id": "V-07", "priority": "critical"},
            ),
            PolicyCheck(
                description="엔지니어에게 critical 알림 발송",
                required_action="notify_engineer",
                required_args={"level": "critical"},
            ),
            PolicyCheck(
                description="임계 초과 근거 없는 즉시 라인 차단 금지",
                forbidden_action="shutdown_line",
            ),
        ],
    )
