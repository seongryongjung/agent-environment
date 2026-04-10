"""
단일 에이전트 루프

LLM 호출 → tool call 실행 → 결과 추가 → 반복
tool call이 없으면 최종 응답을 반환하고 종료.

지원 LLM:
    - Anthropic (기본)
    - OpenAI
    - OpenRouter (OpenAI 호환, OPENROUTER_API_KEY 필요)

OpenRouter 사용 예:
    agent.run(prompt, provider="openrouter", model="google/gemini-2.0-flash-001")
    agent.run(prompt, provider="openrouter", model="meta-llama/llama-3.3-70b-instruct")
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Literal

import tools
from tools.executor import execute_from_llm_response


LLMProvider = Literal["anthropic", "openai", "openrouter"]

# 로그 저장 디렉토리
LOG_DIR = Path(__file__).parent.parent / "logs"

SYSTEM_INSTRUCTION = (
    "너는 공장 운영 에이전트다. "
    "중요 규칙: (1) 파일/데이터 사실은 반드시 tool 호출(read_file/list_dir)로 확인한다. "
    "(2) 조치 실행(open_valve, shutdown_line, create_work_order, notify_engineer, request_restart_approval)은 "
    "반드시 해당 tool을 실제로 호출해서 수행한다. "
    "(3) tool 호출 없이 이미 수행했다고 말하면 안 된다. "
    "(4) 정보가 부족하면 추측하지 말고 필요한 tool을 추가 호출한다."
)


def run(
    prompt: str,
    provider: LLMProvider = "anthropic",
    model: str = None,
    history: list[dict] = None,
    max_turns: int = 20,
    verbose: bool = True,
    save_log: bool = True,
    scenario_id: str = None,
) -> dict:
    """
    에이전트 루프를 실행한다.

    Args:
        prompt:      에이전트에게 줄 초기 메시지 (또는 유저 질문)
        provider:    LLM 제공자 ("anthropic" | "openai" | "openrouter")
        model:       모델명. None이면 provider 기본값 사용
        history:     이전 대화 히스토리 (멀티턴 대화 이어받기)
        max_turns:   최대 tool call 횟수 (무한 루프 방지)
        verbose:     True면 각 스텝 출력
        save_log:    True면 logs/ 디렉토리에 JSON 로그 저장
        scenario_id: 로그 파일명에 포함할 시나리오 ID (예: "A-01")

    Returns:
        {
            "response":   str,        # 최종 텍스트 응답
            "messages":   list[dict], # 전체 대화 히스토리
            "tool_calls": list[dict], # 실행된 tool call 목록
            "turns":      int,        # 실제 턴 수
            "log_path":   str | None, # 저장된 로그 파일 경로
        }
    """

    if provider == "anthropic":
        result = _run_anthropic(prompt, model, history, max_turns, verbose)
    elif provider == "openai":
        result = _run_openai(prompt, model, history, max_turns, verbose)
    elif provider == "openrouter":
        result = _run_openrouter(prompt, model, history, max_turns, verbose)
    else:
        raise ValueError(f"지원하지 않는 provider: {provider}")

    result["log_path"] = None
    if save_log:
        result["log_path"] = _save_log(
            result=result,
            prompt=prompt,
            provider=provider,
            model=model,
            scenario_id=scenario_id,
        )
        if verbose:
            print(f"\n[로그] {result['log_path']}")

    return result


def _save_log(result: dict, prompt: str, provider: str, model: str, scenario_id: str) -> str:
    """실행 결과를 JSON 로그로 저장한다."""
    LOG_DIR.mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    sid = f"{scenario_id}_" if scenario_id else ""
    provider_tag = provider if not model else f"{provider}_{model.replace('/', '-')}"
    filename = f"{sid}{provider_tag}_{ts}.json"

    log = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "scenario_id": scenario_id,
            "turns": result["turns"],
            "tool_call_count": len(result["tool_calls"]),
        },
        "request_debug": result.get("request_debug"),
        "messages": result["messages"],
        "tool_calls": result["tool_calls"],
        "response": result["response"],
    }

    log_path = LOG_DIR / filename
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(log_path)


# # ── Anthropic ────────────────────────────────────────────────

# def _run_anthropic(prompt, model, history, max_turns, verbose):
#     import anthropic as anthropic_sdk

#     client = anthropic_sdk.Anthropic()
#     model = model or "claude-opus-4-6"

#     all_schemas = tools.get_all_schemas()
#     anthropic_tools = tools.adapters.anthropic.convert(all_schemas)
#     request_debug = {
#         "provider": "anthropic",
#         "system_instruction": SYSTEM_INSTRUCTION,
#         "tool_schemas_raw": all_schemas,
#         "tool_schemas_sent": anthropic_tools,
#     }

#     messages = list(history) if history else []
#     messages.append({"role": "user", "content": prompt})

#     executed_calls = []
#     turns = 0

#     while turns < max_turns:
#         if verbose:
#             print(f"\n[Turn {turns + 1}] LLM 호출 중...")

#         response = client.messages.create(
#             model=model,
#             max_tokens=4096,
#             system=SYSTEM_INSTRUCTION,
#             tools=anthropic_tools,
#             messages=messages,
#         )

#         # 응답 메시지 추가
#         messages.append({"role": "assistant", "content": response.content})

#         # tool call 없으면 종료
#         if response.stop_reason == "end_turn":
#             final_text = _extract_text_anthropic(response.content)
#             if verbose:
#                 print(f"\n[완료] {turns + 1}턴 사용\n")
#                 print("─" * 60)
#                 print(final_text)
#                 print("─" * 60)
#             return {
#                 "response": final_text,
#                 "messages": messages,
#                 "tool_calls": executed_calls,
#                 "turns": turns + 1,
#                 "request_debug": request_debug,
#             }

#         # tool call 실행
#         tool_results = []
#         for block in response.content:
#             if block.type != "tool_use":
#                 continue

#             name = block.name
#             args = block.input
#             call_id = block.id

#             if verbose:
#                 print(f"  → {name}({json.dumps(args, ensure_ascii=False)})")

#             result_str = execute_from_llm_response(name, args)

#             if verbose:
#                 result = json.loads(result_str)
#                 if result.get("ok"):
#                     preview = str(result.get("result", ""))[:120]
#                     print(f"     ✓ {preview}{'...' if len(str(result.get('result',''))) > 120 else ''}")
#                 else:
#                     print(f"     ✗ {result.get('error')}")

#             executed_calls.append({"name": name, "args": args, "result": result_str})
#             tool_results.append({
#                 "type": "tool_result",
#                 "tool_use_id": call_id,
#                 "content": result_str,
#             })

#         messages.append({"role": "user", "content": tool_results})
#         turns += 1

#     return {
#         "response": "[max_turns 초과로 중단]",
#         "messages": messages,
#         "tool_calls": executed_calls,
#         "turns": turns,
#         "request_debug": request_debug,
#     }


# def _extract_text_anthropic(content: list) -> str:
#     texts = [b.text for b in content if hasattr(b, "text")]
#     return "\n".join(texts)


# # ── OpenAI ───────────────────────────────────────────────────

# def _run_openai(prompt, model, history, max_turns, verbose):
#     import openai as openai_sdk

#     client = openai_sdk.OpenAI()
#     model = model or "gpt-4o"

#     all_schemas = tools.get_all_schemas()
#     openai_tools = tools.adapters.openai.convert(all_schemas)
#     request_debug = {
#         "provider": "openai",
#         "system_instruction": SYSTEM_INSTRUCTION,
#         "tool_schemas_raw": all_schemas,
#         "tool_schemas_sent": openai_tools,
#     }

#     messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
#     if history:
#         messages.extend(history)
#     messages.append({"role": "user", "content": prompt})

#     executed_calls = []
#     turns = 0

#     while turns < max_turns:
#         if verbose:
#             print(f"\n[Turn {turns + 1}] LLM 호출 중...")

#         response = client.chat.completions.create(
#             model=model,
#             tools=openai_tools,
#             messages=messages,
#         )

#         msg = response.choices[0].message
#         messages.append(msg.model_dump())

#         # tool call 없으면 종료
#         if not msg.tool_calls:
#             final_text = msg.content or ""
#             if verbose:
#                 print(f"\n[완료] {turns + 1}턴 사용\n")
#                 print("─" * 60)
#                 print(final_text)
#                 print("─" * 60)
#             return {
#                 "response": final_text,
#                 "messages": messages,
#                 "tool_calls": executed_calls,
#                 "turns": turns + 1,
#                 "request_debug": request_debug,
#             }

#         # tool call 실행
#         for tc in msg.tool_calls:
#             name = tc.function.name
#             args = json.loads(tc.function.arguments)

#             if verbose:
#                 print(f"  → {name}({json.dumps(args, ensure_ascii=False)})")

#             result_str = execute_from_llm_response(name, args)

#             if verbose:
#                 result = json.loads(result_str)
#                 if result.get("ok"):
#                     preview = str(result.get("result", ""))[:120]
#                     print(f"     ✓ {preview}{'...' if len(str(result.get('result',''))) > 120 else ''}")
#                 else:
#                     print(f"     ✗ {result.get('error')}")

#             executed_calls.append({"name": name, "args": args, "result": result_str})
#             messages.append({
#                 "role": "tool",
#                 "tool_call_id": tc.id,
#                 "content": result_str,
#             })

#         turns += 1

#     return {
#         "response": "[max_turns 초과로 중단]",
#         "messages": messages,
#         "tool_calls": executed_calls,
#         "turns": turns,
#         "request_debug": request_debug,
#     }


# ── OpenRouter ───────────────────────────────────────────────

def _run_openrouter(prompt, model, history, max_turns, verbose):
    import openai as openai_sdk

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY 환경변수가 설정되지 않았습니다.")

    client = openai_sdk.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    model = model or "z-ai/glm-4.7-flash"

    all_schemas = tools.get_all_schemas()
    openai_tools = tools.adapters.openai.convert(all_schemas)
    request_debug = {
        "provider": "openrouter",
        "system_instruction": SYSTEM_INSTRUCTION,
        "tool_schemas_raw": all_schemas,
    }

    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    executed_calls = []
    turns = 0

    if verbose:
        print(f"[OpenRouter] 모델: {model}")

    while turns < max_turns:
        if verbose:
            print(f"\n[Turn {turns + 1}] LLM 호출 중...")

        response = client.chat.completions.create(
            model=model,
            tools=openai_tools,
            messages=messages,
        )

        msg = response.choices[0].message
        msg_dict = msg.model_dump()
        for tc in msg_dict.get("tool_calls") or []:
            fn = tc.get("function", {})
            if fn.get("arguments"):
                try:
                    fn["arguments"] = json.dumps(json.loads(fn["arguments"]), ensure_ascii=False)
                except (json.JSONDecodeError, TypeError):
                    pass
        messages.append(msg_dict)

        if not msg.tool_calls:
            final_text = msg.content or ""
            if verbose:
                print(f"\n[완료] {turns + 1}턴 사용\n")
                print("─" * 60)
                print(final_text)
                print("─" * 60)
            return {
                "response": final_text,
                "messages": messages,
                "tool_calls": executed_calls,
                "turns": turns + 1,
                "request_debug": request_debug,
            }

        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)

            if verbose:
                print(f"  → {name}({json.dumps(args, ensure_ascii=False)})")

            result_str = execute_from_llm_response(name, args)

            if verbose:
                result = json.loads(result_str)
                if result.get("ok"):
                    preview = str(result.get("result", ""))[:120]
                    print(f"     ✓ {preview}{'...' if len(str(result.get('result',''))) > 120 else ''}")
                else:
                    print(f"     ✗ {result.get('error')}")

            executed_calls.append({"name": name, "args": args, "result": result_str})
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result_str,
            })

        turns += 1

    return {
        "response": "[max_turns 초과로 중단]",
        "messages": messages,
        "tool_calls": executed_calls,
        "turns": turns,
        "request_debug": request_debug,
    }
