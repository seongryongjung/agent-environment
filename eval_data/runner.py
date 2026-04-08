"""
QA 데이터셋 평가 러너

QA_DATASET의 모든 질문을 에이전트에게 던지고,
최종 응답에 정답 키워드가 포함됐는지 채점한다.

실행:
    cd "agent environment"
    python eval_data/runner.py                        # Anthropic (기본)
    python eval_data/runner.py --provider openai
    python eval_data/runner.py --provider openrouter --model z-ai/glm-4.7-flash
    python eval_data/runner.py --ids Q-01 Q-02 Q-06  # 특정 문제만
    python eval_data/runner.py --category 추론        # 특정 카테고리만
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from factory_data import load_factory
import agent
from eval_data.qa_dataset import QA_DATASET


def run_eval(
    provider: str = "anthropic",
    model: str = None,
    ids: list[str] = None,
    category: str = None,
    verbose: bool = False,
    save_log: bool = True,
) -> dict:
    """
    QA 데이터셋 전체(또는 필터된 일부)를 평가한다.

    Returns:
        {
            "provider": str,
            "model": str,
            "total": int,
            "passed": int,
            "percentage": float,
            "results": [{"id", "category", "question", "answer", "response", "passed"}, ...]
        }
    """
    load_factory()

    # 필터링
    dataset = QA_DATASET
    if ids:
        dataset = [q for q in dataset if q["id"] in ids]
    if category:
        dataset = [q for q in dataset if q["category"] == category]

    print(f"\n{'=' * 60}")
    print(f"  QA Evaluation  |  {provider}  |  {model or '(default)'}")
    print(f"  총 {len(dataset)}개 문제")
    print(f"{'=' * 60}\n")

    results = []
    for i, qa in enumerate(dataset, 1):
        print(f"[{i}/{len(dataset)}] {qa['id']} — {qa['question'][:40]}...")

        result = agent.run(
            prompt=qa["question"],
            provider=provider,
            model=model,
            verbose=verbose,
            save_log=save_log,
            scenario_id=qa["id"],
        )

        response = result.get("response", "")
        parsed_choice = None
        passed = _check(response, qa["answer"])
        answer_for_print = str(qa["answer"])

        icon = "✅" if passed else "❌"
        print(f"         {icon}  정답: {answer_for_print}")
        if not passed:
            preview = response[:80].replace("\n", " ")
            print(f"         응답 미리보기: {preview}...")
        print()

        results.append({
            "id": qa["id"],
            "category": qa["category"],
            "question": qa["question"],
            "answer": qa["answer"],
            "response": response,
            "passed": passed,
            "predicted_choice": parsed_choice,
            "tool_calls": [tc["name"] for tc in result.get("tool_calls", [])],
        })

    passed_count = sum(1 for r in results if r["passed"])
    total = len(results)
    pct = round(passed_count / total * 100) if total else 0

    summary = {
        "provider": provider,
        "model": model,
        "total": total,
        "passed": passed_count,
        "percentage": pct,
        "results": results,
    }

    _print_summary(summary)

    if save_log:
        _save_eval_log(summary)

    return summary


def _check(response: str, answer_keywords: list[str]) -> bool:
    """정답 키워드 중 하나라도 응답에 포함되면 정답."""
    resp_lower = response.lower()
    return any(kw.lower() in resp_lower for kw in answer_keywords)


def _print_summary(summary: dict) -> None:
    total = summary["total"]
    passed = summary["passed"]
    pct = summary["percentage"]
    mark = "PASS" if pct >= 70 else "FAIL"

    print("=" * 60)
    print(f"  최종 결과  [{mark}]")
    print(f"  {passed} / {total}  ({pct}%)")
    print()

    # 카테고리별 집계
    by_cat: dict[str, dict] = {}
    for r in summary["results"]:
        cat = r["category"]
        if cat not in by_cat:
            by_cat[cat] = {"total": 0, "passed": 0}
        by_cat[cat]["total"] += 1
        if r["passed"]:
            by_cat[cat]["passed"] += 1

    for cat, s in by_cat.items():
        cat_pct = round(s["passed"] / s["total"] * 100)
        bar = "█" * (cat_pct // 10) + "░" * (10 - cat_pct // 10)
        print(f"  {cat:6}  {bar}  {s['passed']}/{s['total']}  ({cat_pct}%)")

    print("=" * 60)

    # 실패 목록
    failed = [r for r in summary["results"] if not r["passed"]]
    if failed:
        print("\n  [ 오답 목록 ]")
        for r in failed:
            print(f"    ❌ {r['id']}  {r['question'][:45]}")
            print(f"        정답 키워드: {r['answer']}")


def _save_eval_log(summary: dict) -> None:
    log_dir = Path(__file__).parent.parent / "logs" / "eval"
    log_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    provider = summary["provider"]
    model = summary["model"] or "default"
    filename = f"qa_eval_{provider}_{model.replace('/', '-')}_{ts}.json"

    log_path = log_dir / filename
    log_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[로그] {log_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="anthropic",
                        choices=["anthropic", "openai", "openrouter"])
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--ids", nargs="+", default=None,
                        help="평가할 QA ID 목록 (예: Q-01 Q-02)")
    parser.add_argument("--category", type=str, default=None,
                        help="평가할 카테고리 (센서 | 추론 | 매뉴얼 | 이력 | 종합)")
    parser.add_argument("--verbose", action="store_true",
                        help="에이전트 각 스텝 출력")
    parser.add_argument("--no-log", action="store_true",
                        help="로그 파일 저장 안 함")
    args = parser.parse_args()

    run_eval(
        provider=args.provider,
        model=args.model,
        ids=args.ids,
        category=args.category,
        verbose=args.verbose,
        save_log=not args.no_log,
    )
