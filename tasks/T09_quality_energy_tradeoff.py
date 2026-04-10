"""
T-09 — 품질/에너지/환경 트레이드오프 대응

목표:
    품질 기준 이탈, 피크 전력, 외기 악화를 함께 보고
    즉시 차단 없이 보고/정비/분석 보고서를 수행한다.
"""

from tasks.base import Task, PolicyCheck


def build() -> Task:
    return Task(
        id="T-09",
        title="품질-에너지-환경 트레이드오프 대응",
        initial_prompt=(
            "동일 일자에 품질 지표 이탈과 전력 피크, 외기 악화가 동시에 보고됐습니다.\n"
            "품질 정책, 전력 정책, 기상/냉각 효율, 사고 이력을 교차 검토해\n"
            "즉시 실행 조치와 근거 요약 보고서를 남기세요."
        ),
        policy_checks=[
            PolicyCheck(
                description="엔지니어 경고 알림 발송",
                required_action="notify_engineer",
                required_args={"level": "warning"},
            ),
            PolicyCheck(
                description="원인 분석 보고서 생성",
                required_action="generate_report",
            ),
            PolicyCheck(
                description="즉시 라인 차단 금지 (근거 부족)",
                forbidden_action="shutdown_line",
            ),
        ],
    )
