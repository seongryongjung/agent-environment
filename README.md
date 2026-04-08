# Industrial Agent Environment

공장 데이터를 탐색하고 분석하는 AI 에이전트를 평가하기 위한 환경.

---

## 개념

LLM 에이전트에게 공장 상황을 주고, 데이터를 직접 탐색해서 원인을 파악하고 조치를 취하도록 한다.
평가는 두 가지 방식을 지원한다.

| 방식 | 무엇을 테스트 | 채점 기준 |
|------|------------|----------|
| **QA Mode** | 데이터 탐색 정확도 | 응답에 정답 키워드 포함 여부 |
| **Task Mode** | 정책 준수 + 액션 실행 | 어떤 툴을 호출했는가 |

---

## 시스템 구조

```
┌──────────────────────────────────────────────────────┐
│                     LLM Agent                        │
│  (anthropic / openai / openrouter)                   │
└───────────────────┬──────────────────────────────────┘
                    │ tool calls
        ┌───────────┼─────────────────┐
        ▼           ▼                 ▼
   read_file     list_dir       generate_report     ← 데이터 접근
   write_file                   shutdown_line
                                 open_valve          ← 상태 변경
                                 create_work_order   (Task Mode)
                                 notify_engineer
                                 request_restart_approval
        │                              │
        ▼                              ▼
      VFS                          State DB
 (공장 파일 저장소)               (장비/라인 상태)
        │
        ▼
  factory_data/
 (실제 데이터 파일들)
```

---

## 레이어 설명

### VFS (`vfs/`)
Python dict 기반 가상 파일 시스템. `factory_data/`의 파일들을 메모리 dict 트리로 로드해서 에이전트가 경로로 접근하게 한다.

```python
vfs.read_file("/factory/sensors/line3_temp_hourly.csv")
vfs.list_dir("/factory/reports")
```

### factory_data/
에이전트가 탐색할 공장 데이터. 모두 읽기 전용이며 시나리오와 무관하게 항상 동일하다.

```
sensors/
├── line1/2/3_temp/flow/pressure_hourly.csv   # 시간별 센서
├── high_freq/                                 # 1분 단위 고주파
│   └── line3_temp/flow/valve_position/vibration
├── monthly/                                   # 월별 일별 요약
└── energy_daily, total_power_15min, ambient_temp

manuals/
├── cooling_system_map.txt    # 밸브-라인 매핑, 임계값
├── pump_manual.txt           # 펌프 사양, RPM 범위
├── emergency_playbook.txt    # 긴급 대응 절차
└── sensor_handbook.txt

reports/
├── maintenance_master_log.txt      # 전체 장비 점검 이력
├── incident_casebook_2022_2024.txt # 과거 사고 전례
├── alarm_raw_events_2024_05_21.csv
├── shift_handover_2024_05_21.txt
├── sensor_calibration_log.txt
└── postmortems/, tickets/, weekly/, audits/, compliance/

policies/
├── operation_guardrail_policy.txt  # 운전 정책 (온도 임계값, 감속 기준)
├── maintenance_sla_policy.txt      # 정비 주기 SLA
├── data_reliability_policy.txt
├── quality_release_policy.txt
├── energy_demand_policy.txt
└── versions/                       # 정책 변경 이력 (v2→v3)

experiments/
├── throttle_tests.csv              # 감속 실험 결과
├── load_shedding_options.csv       # 부하 분산 옵션
├── coolant_additive_tests.csv      # 냉각수 첨가제 실험
├── recovery_simulation.csv
└── doe/, simulations/, ablation/, monte_carlo/

finance/         # 다운타임 비용, 에너지 요금, 월 P&L
quality/         # 불량 분류, 검사 결과, 재작업 로그
procurement/     # 공급사, 발주서, 재고, 납기
operations/      # 레시피 버전, 교대 캘린더, 운전원 스킬
environment/     # 기상, 습도, 냉각탑 효율
topology/        # 자산 등록부, 의존성 그래프, 구역 맵
```

### State DB (`state_db/`)
장비/라인의 실시간 상태. Task Mode에서만 사용하며 에이전트의 action tool 호출로 상태가 변경된다.

```python
# 초기 상태 예시 (T-01)
{
    "lines": {
        "line3": {"status": "running", "temp": 113.4, "flow": 66.8}
    },
    "valves": {"V-07": {"position": "partial"}},
    "work_orders": [],
    "notifications": [],
}
```

### Tools

**데이터 접근 (항상 사용 가능)**

| 툴 | 설명 |
|----|------|
| `read_file` | 파일 읽기 (센서/매뉴얼/보고서/정책 등) |
| `list_dir` | 디렉토리 탐색 |
| `write_file` | 파일 쓰기 |
| `generate_report` | 분석 보고서 파일 생성 |

**액션 (Task Mode)**

| 툴 | 설명 |
|----|------|
| `shutdown_line` | 생산 라인 즉시 차단 |
| `open_valve` | 밸브 수동 완전 개방 |
| `create_work_order` | 장비 정비 작업 지시 생성 |
| `notify_engineer` | 엔지니어 알림 발송 |
| `request_restart_approval` | 재가동 승인 요청 |

### Agent Loop (`agent/loop.py`)
tool call이 없을 때까지 LLM 호출을 반복하는 멀티턴 루프.

```python
result = agent.run(
    prompt="...",
    provider="anthropic",   # anthropic | openai | openrouter
    model="claude-opus-4-6",
    max_turns=20,
)
# result = {response, messages, tool_calls, turns, log_path}
```

---

## 평가 방식

### QA Mode

고정 질문 → 에이전트 응답 → 키워드 포함 여부 채점.

```python
# eval_data/qa_dataset.py
{
    "id": "Q-001",
    "category": "센서",
    "question": "2024-05-21 12:00 기준 Line 3 온도는 몇 도인가요?",
    "answer": ["113.4"],
}
```

```
실행 흐름:
load_factory() → for qa in QA_DATASET: agent.run(question) → keyword in response?
```

```bash
python eval_data/runner.py
python eval_data/runner.py --provider openrouter --model z-ai/glm-4.7-flash
python eval_data/runner.py --category 센서
python eval_data/runner.py --ids Q-001 Q-002
```

### Task Mode

상황 제시 → 에이전트가 데이터 조회 후 action tool 호출 → 호출 이력 기반 채점.

```python
# tasks/T01_cooling_emergency.py
PolicyCheck("엔지니어 critical 알림 발송", 30, required_action="notify_engineer")
PolicyCheck("V-07 작업 지시 생성",         25, required_action="create_work_order")
PolicyCheck("V-07 밸브 수동 개방",         25, required_action="open_valve")
PolicyCheck("115°C 미만 → 라인 차단 금지", 20, forbidden_action="shutdown_line")
```

```
실행 흐름:
load_factory() → state_db.reset() → agent.run(prompt) → task_evaluator.evaluate()
```

```bash
python tasks/runner.py --task T-01
python tasks/runner.py --task T-01 --provider openrouter --model z-ai/glm-4.7-flash
python tasks/runner.py --list
```

---

## 프로젝트 구조

```
agent environment/
├── vfs/                    # Virtual File System
│   ├── core.py
│   └── errors.py
│
├── factory_data/           # 공장 데이터 (읽기 전용)
│   ├── loader.py           # load_factory() → VFS 초기화
│   ├── sensors/
│   ├── manuals/
│   ├── reports/
│   ├── policies/
│   ├── experiments/
│   ├── finance/
│   ├── quality/
│   ├── procurement/
│   ├── operations/
│   ├── environment/
│   └── topology/
│
├── state_db/               # 장비/라인 실시간 상태 (Task Mode)
│   └── core.py
│
├── runtime/                # 툴 구현체
│   ├── registry.py         # @register_function 데코레이터
│   ├── executor.py         # call(name, args)
│   ├── functions.py        # generate_report
│   └── actions.py          # shutdown_line, open_valve, ...
│
├── tools/                  # LLM 툴 인터페이스
│   ├── schema.py           # 툴 스키마 정의
│   ├── executor.py         # VFS/Runtime 라우팅
│   └── adapters/           # openai.py, anthropic.py (포맷 변환)
│
├── agent/
│   └── loop.py             # 멀티턴 에이전트 루프
│
├── eval_data/              # QA Mode
│   ├── qa_dataset.py       # 질문-정답 쌍
│   └── runner.py
│
├── tasks/                  # Task Mode
│   ├── base.py             # Task, PolicyCheck 데이터클래스
│   ├── loader.py
│   ├── T01_cooling_emergency.py
│   └── runner.py
│
├── task_evaluator.py       # 액션 기반 채점
├── requirements.txt
└── logs/                   # 실행 로그 JSON
    └── eval/
```

---

## 설치

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."        # OpenAI 사용 시
export OPENROUTER_API_KEY="..."    # OpenRouter 사용 시
```
