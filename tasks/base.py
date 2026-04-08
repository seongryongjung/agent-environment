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
    required_args:    required_action 호출 시 확인할 args 조건
    """
    description: str
    # legacy 필드: 과거 점수 기반 평가와의 호환용 (현재 체크리스트 평가는 미사용)
    points: Optional[int] = None
    required_action: Optional[str] = None
    forbidden_action: Optional[str] = None
    required_args: Optional[dict] = None


@dataclass
class Task:
    id: str
    title: str
    initial_prompt: str
    policy_checks: list[PolicyCheck] = field(default_factory=list)

    @property
    def total_points(self) -> int:
        # legacy 지표 (체크리스트 모드에서는 의미 없음)
        return sum((p.points or 0) for p in self.policy_checks)
