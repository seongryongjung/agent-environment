"""
Task 베이스 클래스

TAU-bench 스타일 태스크 정의.
에이전트가 어떤 액션을 실행했는지, 정책을 준수했는지 기반으로 채점한다.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PolicyCheck:
    """
    정책 준수 항목 하나.

    required_action:  이 액션을 반드시 호출해야 통과
    forbidden_action: 이 액션을 호출하면 실패 (정책 위반)
    둘 다 None이면 custom_check 함수로 판단 (추후 확장용)
    """
    description: str
    points: int
    required_action: Optional[str] = None
    forbidden_action: Optional[str] = None
    required_args: Optional[dict] = None  # required_action 호출 시 확인할 args 조건


@dataclass
class Task:
    id: str
    title: str
    initial_prompt: str
    initial_state: dict          # state_db 초기 상태
    policy_checks: list[PolicyCheck] = field(default_factory=list)
    context: str = ""            # 에이전트에게 주는 추가 컨텍스트 (정책 요약 등)

    @property
    def total_points(self) -> int:
        return sum(p.points for p in self.policy_checks)
