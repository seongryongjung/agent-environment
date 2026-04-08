"""
Task Evaluator — 액션 기반 채점

에이전트가 실행한 액션 목록과 state_db 최종 상태를 보고 정책 준수 여부를 채점한다.
QA evaluator(키워드 매칭)와 달리, 어떤 액션을 호출했는지가 기준이다.
"""

import state_db
from tasks.base import Task, PolicyCheck


def evaluate(result: dict, task: Task) -> dict:
    """
    Args:
        result: agent.run()의 반환값
        task:   load_task()의 반환값

    Returns:
        {
            "task_id":        "T-01",
            "total_earned":   75,
            "total_possible": 100,
            "percentage":     75,
            "passed":         True,
            "scores":         [...],
            "called_actions": ["notify_engineer", "open_valve", ...],
            "final_state":    {...},
            "action_log":     [...],
        }
    """
    action_log = state_db.get_action_log()
    called_actions = [entry["action"] for entry in action_log]
    final_state = state_db.get_all()

    scores = []
    for check in task.policy_checks:
        passed, reason = _check_policy(check, action_log)
        scores.append({
            "description": check.description,
            "points":      check.points,
            "earned":      check.points if passed else 0,
            "passed":      passed,
            "reason":      reason,
        })

    total_earned   = sum(s["earned"] for s in scores)
    total_possible = task.total_points

    return {
        "task_id":        task.id,
        "total_earned":   total_earned,
        "total_possible": total_possible,
        "percentage":     round(total_earned / total_possible * 100) if total_possible else 0,
        "passed":         total_earned >= total_possible * 0.7,
        "scores":         scores,
        "called_actions": called_actions,
        "final_state":    final_state,
        "action_log":     action_log,
    }


def print_report(eval_result: dict) -> None:
    r = eval_result
    mark = "✅ PASS" if r["passed"] else "❌ FAIL"

    print()
    print("=" * 60)
    print(f"  Task 채점 결과 [{r['task_id']}]  {mark}")
    print("=" * 60)
    print(f"  총점: {r['total_earned']} / {r['total_possible']}점  ({r['percentage']}%)")
    print()

    for s in r["scores"]:
        icon   = "✅" if s["passed"] else "❌"
        earned = f"+{s['earned']}점" if s["passed"] else f" 0점 (/{s['points']}점)"
        print(f"  {icon} {earned:12}  {s['description']}")
        if not s["passed"]:
            print(f"              └ {s['reason']}")

    print()
    actions_str = " → ".join(r["called_actions"]) if r["called_actions"] else "없음"
    print(f"  실행된 액션: {actions_str}")
    print()

    state = r["final_state"]
    line3 = state.get("lines", {}).get("line3", {})
    v07   = state.get("valves", {}).get("V-07", {})
    wo_count = len(state.get("work_orders", []))
    notif_count = len(state.get("notifications", []))
    print(f"  최종 상태:")
    print(f"    Line 3  : {line3.get('status', '-')}  (temp={line3.get('temp', '-')}, flow={line3.get('flow', '-')})")
    print(f"    V-07    : {v07.get('position', '-')}")
    print(f"    작업지시 : {wo_count}건  |  알림 발송: {notif_count}건")
    print("=" * 60)


def _check_policy(check: PolicyCheck, action_log: list[dict]) -> tuple[bool, str]:
    called_names = [e["action"] for e in action_log]

    # 금지 액션
    if check.forbidden_action:
        if check.forbidden_action in called_names:
            return False, f"정책 위반: {check.forbidden_action} 호출됨"
        return True, f"{check.forbidden_action} 미호출 (정상)"

    # 필수 액션
    if check.required_action:
        if check.required_action not in called_names:
            return False, f"{check.required_action} 미호출"

        # args 조건 추가 확인
        if check.required_args:
            matching = [
                e for e in action_log
                if e["action"] == check.required_action
                and all(e["args"].get(k) == v for k, v in check.required_args.items())
            ]
            if not matching:
                return False, (
                    f"{check.required_action} 호출됐지만 "
                    f"조건 불일치: {check.required_args}"
                )
        return True, f"{check.required_action} 호출됨"

    return False, "검증 조건 없음"
