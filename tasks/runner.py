"""
Task Runner — TAU-bench 스타일 평가

실행:
    cd "agent environment"
    python tasks/runner.py                              # T-01, Anthropic 기본
    python tasks/runner.py --task T-01 --provider openrouter --model z-ai/glm-4.7-flash
    python tasks/runner.py --list                       # 등록된 task 목록
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from factory_data import load_factory
from tasks.loader import load_task, list_tasks
import agent
import task_evaluator


def run_task(
    task_id: str,
    provider: str = "anthropic",
    model: str = None,
    verbose: bool = True,
) -> dict:
    # 1. 공장 데이터 → VFS
    load_factory()
    print("✓ 공장 데이터 로드 완료")

    # 2. 태스크 로드
    task = load_task(task_id)
    print(f"✓ Task 로드: [{task.id}] {task.title}")
    print(f"  정책 항목: {len(task.policy_checks)}개")

    print()
    print("=" * 60)
    print("[ 상황 ]")
    print(task.initial_prompt)
    print("=" * 60)
    print()

    # 3. 에이전트 실행
    result = agent.run(
        prompt=task.initial_prompt,
        provider=provider,
        model=model,
        verbose=verbose,
        scenario_id=task.id,
    )

    # 4. 채점
    eval_result = task_evaluator.evaluate(result, task)
    task_evaluator.print_report(eval_result)

    return eval_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default="T-01", help="Task ID (예: T-01)")
    parser.add_argument("--provider", default="anthropic",
                        choices=["anthropic", "openai", "openrouter"])
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--no-verbose", action="store_true")
    parser.add_argument("--list", action="store_true", help="등록된 task 목록 출력")
    args = parser.parse_args()

    if args.list:
        print("\n[ 등록된 Tasks ]")
        for t in list_tasks():
            print(f"  {t['id']}  {t['title']}  ({t['policy_checks']}개 정책)")
        sys.exit(0)

    run_task(args.task, args.provider, args.model, not args.no_verbose)
