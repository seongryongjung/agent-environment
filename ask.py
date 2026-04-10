"""
간단 질의 실행기

사용 예:
  ./.venv/bin/python ask.py "2024-05-21 12:00 기준 Line 3 진동은?"
  ./.venv/bin/python ask.py "Line 3 온도 알려줘" --provider openrouter --model google/gemini-2.5-flash
"""

import argparse

import agent
from factory_data import load_factory


def main() -> None:
    parser = argparse.ArgumentParser(description="데이터 기반 단일 질문 실행")
    parser.add_argument("question", help="에이전트에게 보낼 질문")
    parser.add_argument(
        "--provider",
        default="openrouter",
        choices=["anthropic", "openai", "openrouter"],
        help="LLM 제공자",
    )
    parser.add_argument("--model", default=None, help="모델명 (생략 시 provider 기본값)")
    parser.add_argument("--scenario-id", default="ASK-001", help="로그 시나리오 ID")
    parser.add_argument("--no-verbose", action="store_true", help="중간 출력 숨김")
    parser.add_argument("--no-log", action="store_true", help="실행 로그 저장 안 함")
    args = parser.parse_args()

    load_factory()

    result = agent.run(
        prompt=args.question,
        provider=args.provider,
        model=args.model,
        verbose=not args.no_verbose,
        save_log=not args.no_log,
        scenario_id=args.scenario_id,
    )

    print("\n[최종 답변]")
    print(result["response"])
    print(f"\n[툴 호출 수] {len(result['tool_calls'])}")
    if result.get("log_path"):
        print(f"[로그] {result['log_path']}")


if __name__ == "__main__":
    main()

