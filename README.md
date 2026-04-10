# Industrial Agent Environment

공장 운영 AI 에이전트를 평가하기 위한 시뮬레이션 환경.  
에이전트는 실제 공장 데이터를 직접 탐색하고, 상황을 분석하여, 운전 정책에 맞는 조치를 실행해야 한다.

---

## 목적

LLM 에이전트가 단순히 "정답을 아는지"가 아니라 **"실제로 데이터를 읽고, 정책을 이해하고, 올바른 판단을 내리는지"** 를 평가한다.

평가 방식은 두 가지다.

| 방식 | 무엇을 테스트 | 채점 기준 |
|------|------------|----------|
| **Task Mode** | 정책 판단 + 액션 실행 | 어떤 툴을 어떤 인자로 호출했는가 |
| **QA Mode** | 데이터 탐색 + 분석 정확도 | 응답에 정답 키워드 포함 여부 |

---

## 전체 아키텍처

```
factory_data/           ← 공장 원본 데이터 (CSV, TXT, 읽기 전용)
      ↓ load_factory()
VFS (메모리 dict 트리)   ← 에이전트가 경로로 접근하는 가상 파일시스템
      ↓ read_file / list_dir / write_file
tools/                  ← 툴 스키마 정의 + LLM 포맷 변환 + 라우팅
      ↓ execute(name, args)
    ┌─────────────┬───────────────────┐
    │  VFS 접근   │  Runtime 액션     │
    │ (read/write)│(shutdown/valve/…) │
    └─────────────┴───────────────────┘
agent/loop.py           ← 멀티턴 LLM 루프 (tool_calls 반복 실행)
      ↓ result["tool_calls"]
task_evaluator.py       ← 액션 기반 채점 (PolicyCheck 검증)
```

데이터 흐름 요약:
1. `load_factory()` 가 `factory_data/` 디스크 파일을 읽어 VFS에 올린다
2. 에이전트 루프가 태스크 프롬프트를 받아 LLM과 멀티턴 대화를 시작한다
3. LLM이 tool_call을 반환하면, `tools/executor.py` 가 VFS 또는 Runtime으로 라우팅한다
4. 툴 실행 결과가 다음 메시지로 append되어 LLM이 다음 turn을 생성한다
5. tool_call이 없으면 루프 종료, `task_evaluator` 가 호출된 툴 목록을 검증한다

---

## 프로젝트 구조

```
agent environment/
│
├── factory_data/              # 공장 원본 데이터 (읽기 전용)
│   ├── loader.py              # load_factory() — 디스크 → VFS 초기화
│   ├── sensors/               # 시간별·고빈도·월별 센서 데이터
│   ├── manuals/               # 장비 매뉴얼, 임계값 기준
│   ├── policies/              # 운전·SLA·품질·에너지 정책
│   ├── reports/               # 정비이력, 알람, 포스트모템, 감사
│   ├── quality/               # 검사 결과, 불량 분류
│   ├── finance/               # 비용 모델, 에너지 요금, P&L
│   ├── procurement/           # 공급사, 발주서, 재고
│   ├── operations/            # 레시피, 교대 일정, 운전원 스킬
│   ├── environment/           # 기상, 냉각탑 효율
│   ├── experiments/           # 시뮬레이션, DOE, 회수 전략
│   └── topology/              # 자산 등록부, 의존성 그래프
│
├── vfs/                       # 가상 파일시스템
│   ├── core.py                # read_file, write_file, list_dir, tree 등
│   └── errors.py              # VFSError 계열 예외
│
├── runtime/                   # 액션 툴 구현체
│   ├── registry.py            # @register_function 데코레이터 + 레지스트리
│   ├── executor.py            # call(name, args) 디스패처
│   ├── actions.py             # shutdown_line, open_valve, create_work_order, notify_engineer, request_restart_approval
│   └── functions.py           # generate_report
│
├── tools/                     # LLM 툴 인터페이스 레이어
│   ├── schema.py              # VFS_TOOLS + Runtime 스키마 통합
│   ├── executor.py            # VFS / Runtime 라우팅
│   └── adapters/
│       ├── anthropic.py       # → input_schema 포맷
│       └── openai.py          # → function 포맷
│
├── agent/
│   └── loop.py                # 멀티턴 에이전트 루프
│
├── tasks/                     # Task Mode (시나리오 기반 평가)
│   ├── base.py                # Task, PolicyCheck 데이터클래스
│   ├── loader.py              # 태스크 레지스트리 (T-01 ~ T-09)
│   ├── runner.py              # CLI 실행기
│   ├── T01_cooling_emergency.py
│   ├── T02_vibration_escalation.py
│   ├── T03_energy_overconsumption.py
│   ├── T04_quality_hold.py
│   ├── T05_multi_sla_breach.py
│   ├── T06_emergency_shutdown_required.py
│   ├── T07_shutdown_and_stabilize.py
│   ├── T08_cross_domain_maintenance_triage.py
│   └── T09_quality_energy_tradeoff.py
│
├── eval_data/                 # QA Mode
│   ├── qa_dataset.py          # 150+ 질문-정답 데이터셋
│   ├── runner.py              # QA 평가 CLI
│   └── rebuild_mcq_choices.py
│
├── task_evaluator.py          # 액션 기반 채점 엔진
├── ask.py                     # 단일 질문 CLI
├── logs/                      # 실행 로그 (JSON)
└── requirements.txt
```

---

## 레이어 1 — 공장 데이터 (`factory_data/`)

에이전트가 탐색할 모든 원본 데이터. 읽기 전용이며 VFS를 통해서만 접근한다.

### 센서 데이터 (`sensors/`)

**시간별 (hourly)** — 4일치 수록 (2024-05-19 ~ 05-22)

| 파일 | 컬럼 | 비고 |
|------|------|------|
| `line1/2/3_temp_hourly.csv` | timestamp, value_celsius | Line 3: 05-21에 최대 116.2°C |
| `line1/2/3_flow_hourly.csv` | timestamp, flow_lpm | Line 3: 05-21에 최소 62.4 L/min |
| `line1/2/3_pressure_hourly.csv` | timestamp, pressure_bar | Line 3: 05-21에 2.97 bar까지 하락 |
| `line3_vibration_hourly.csv` | timestamp, vibration_rms_mm_s | 05-21 최대 5.7 mm/s |
| `ambient_temp_hourly.csv` | timestamp, ambient_celsius | 일중 18~31°C |
| `energy_daily_2024_05.csv` | date, line1/2/3_kwh, total | 5월 31일치 |
| `total_power_15min.csv` | timestamp, total_kw | 05-21 오후 15분 단위 |

**4일치 시나리오 타임라인:**

```
2024-05-19  정상 운영일
  Line 3: 온도 82~86°C / 유량 98~101 L/min / 진동 1.8~2.5 mm/s

2024-05-20  이상 조짐일 (V-07 stick-slip 시작)
  Line 3: 오후부터 유량 93 L/min 하락 / 진동 3.8 mm/s까지 상승

2024-05-21  사고 당일 (24시간)
  00:00  정상 (84°C / 100 L/min)
  05:31  유량 경보 (하락 시작)
  06:07  온도 경보 (87.6°C)
  10:12  진동 경보 (4.7 mm/s, cavitation 위험)
  12:00  113.4°C / 66.8 L/min  ← T-01, T-02, T-04, T-05 기준 시각
  13:00  115.0°C               ← T-06 기준 시각 (긴급차단 임계 도달)
  14:00  116.2°C / 62.4 L/min  ← T-07 기준 시각 (임계 초과)
  15:00~ 셧다운 후 냉각 (108→98→91→87°C)
  19:00~ 온도 안정 (~85°C)

2024-05-22  복구 완료일 (V-07 교체 후 재가동)
  00:00~05:00  셧다운 상태 (유량 0)
  06:00~       재가동 — 온도 정상화, 유량 98+ L/min 회복
```

**고빈도 (1분 단위)** — 2024-05-21 05:00~

```
line3_temp/flow/vibration_1min_2024-05-21.csv
line3_valve_position_1min_2024-05-21.csv   ← V-07 개도 (87→81% 감소)
pump_a_current_1min_2024-05-21.csv         ← 전류 상승 (121→123A)
cooling_header_1min_2024-05-21.csv
line1/2_temp/flow/pressure_1min_...csv
```

**월별 (`monthly/`)** — 2024-01 ~ 06, 일별 집계

```
line3_daily_summary_2024-0N.csv
  컬럼: date, avg_temp_c, avg_flow_lpm, alarm_count
line3_energy_temp_history_monthly.csv
  컬럼: month, line3_avg_kwh_day, line3_peak_kwh_day, flow_alarm_count
  범위: 2023-01 ~ 2024-04 (16개월)
```

### 매뉴얼 (`manuals/`)

| 파일 | 내용 |
|------|------|
| `cooling_system_map.txt` | V-05/06/07 배치, 정상 유량 95~105 L/min, 온도 임계값 (정상 80~90 / 경고 100 / 위험 110 / 긴급차단 115°C) |
| `pump_manual.txt` | PUMP-A/B 정격 15kW, 정상 RPM 1450~1550, cavitation 위험 임계 ≥4.5 mm/s |
| `emergency_playbook.txt` | 긴급 대응 절차, 재가동 조건 (30분 연속 ≤90°C + 유량 ≥95 L/min) |
| `sensor_handbook.txt` | 센서 단위 정의, 측정 범위, 교정 주기 |

### 정책 (`policies/`)

| 파일 | 핵심 내용 |
|------|----------|
| `operation_guardrail_policy.txt` | v3.1 현행 — >105°C: 15% 감속 / ≥110°C: 팀장 호출 + 근인 분석 / **≥115°C: 즉시 긴급차단** / 금지: ≥110°C에서 출력 증가 |
| `maintenance_sla_policy.txt` | V-05/06/07: 180일 주기 / PUMP-A/B: 120일 주기 / 초과 1~30일: 황색 / 31~60일: 주황 / 61+일: 적색 |
| `energy_demand_policy.txt` | 계약 수요전력 2,400 kW / 2,300 kW 도달 시 사전 감속 / 2,400 kW 초과 시 비필수 부하 차단 |
| `quality_release_policy.txt` | 수율 ≥96.5% / 불량률 ≤1.8% / 온도 편차 ≤±2.5°C 초과 시 홀드 또는 재검사 |
| `data_reliability_policy.txt` | 교정 주기: 온도 90일 / 압력·유량 120일 / 진동 60일 / 교정 만료 센서 단독으로 자동차단 금지 |

### 설비 구성 (`topology/`)

**asset_registry.csv** (9개 자산)

| 자산 | 유형 | 라인 | 중요도 |
|------|------|------|--------|
| V-05 | 밸브 | L1 | B |
| V-06 | 밸브 | L2 | B |
| **V-07** | 밸브 | L3 | **A** |
| **PUMP-A** | 펌프 | L3 | **A** |
| PUMP-B | 펌프 | L2 | B |
| HX-31 | 열교환기 | L3 | **A** |
| SENS-L3-T | 온도센서 | L3 | **A** |
| SENS-L3-F | 유량센서 | L3 | **A** |
| SENS-L3-VIB | 진동센서 | L3 | B |

**dependency_graph.csv** — `PUMP-A → V-07 → HX-31 → Line3-Reactor` 의존 체인

### 기타 도메인

| 디렉토리 | 주요 내용 |
|----------|----------|
| `reports/` | 알람 이벤트, 교대 인수인계, 정비이력, 감사기록, 포스트모템 |
| `quality/` | 검사 로트 결과, 불량 분류, 재작업 기록 |
| `finance/` | L3 다운타임 $78/분, 에너지 요금, 월별 P&L |
| `procurement/` | 공급사 5개 (V-07: CoreValve KR, OTD 96.2%), 발주서, 납기이력 |
| `operations/` | 레시피 버전, 교대 일정 (3교대), 운전원 스킬 매트릭스 |
| `environment/` | 기상 (05-21: 18→31°C), 냉각탑 효율 곡선 |
| `experiments/` | 출력 감속 실험, 회수 전략 시뮬레이션, 몬테카를로 100회 |

---

## 레이어 2 — 가상 파일시스템 (`vfs/`)

`factory_data/` 를 Python dict 트리로 메모리에 올려 에이전트가 경로로 접근하게 한다.

```python
from factory_data import load_factory

load_factory()  # factory_data/ 디스크 → VFS 초기화

# 에이전트가 실제로 호출하는 방식
read_file("/factory/sensors/line3_temp_hourly.csv")   # 파일 내용 반환
list_dir("/factory/policies")                          # 파일 목록 반환
write_file("/factory/workspace/memo.txt", "...")       # 자유 작업공간 쓰기
```

- `dict` 값이 `str` → 파일, `dict` → 디렉토리
- `/factory/workspace/` 는 에이전트 자유 작업 공간 (초기 비어 있음)
- 모든 경로는 `/factory/` 루트부터 시작
- `load_factory()` 호출마다 VFS가 완전히 재초기화된다

---

## 레이어 3 — 툴 (`tools/` + `runtime/`)

에이전트에게 제공되는 도구 전체 목록.

### 읽기/쓰기 툴 (항상 사용 가능)

| 툴 | 파라미터 | 설명 |
|----|----------|------|
| `read_file` | `path: str` | VFS 파일 내용 반환 |
| `list_dir` | `path: str` | 디렉토리 항목 목록 반환 |
| `write_file` | `path: str, content: str` | VFS 파일 쓰기 |

### 액션 툴 (Task Mode에서 채점 대상)

| 툴 | 파라미터 | 사용 조건 |
|----|----------|----------|
| `shutdown_line` | `line_id, reason` | 온도 **≥115°C** 시에만 사용 |
| `open_valve` | `valve_id` | 유량 회복이 필요할 때 |
| `create_work_order` | `equipment_id, description, priority` | SLA 초과 또는 이상 발생 시 |
| `notify_engineer` | `level, message` | 이상 감지 시 (level: info/warning/critical) |
| `request_restart_approval` | `line_id, reason` | 셧다운 후 재가동 전에만 |
| `generate_report` | `title, content` | 분석 결과를 파일로 저장 |

### 툴 스키마 라우팅

```
tools.get_all_schemas()   ← VFS_TOOLS + runtime.registry.get_schemas() 통합
      ↓ LLM provider 포맷 변환
tools.adapters.anthropic  → input_schema 형식
tools.adapters.openai     → function 형식 (OpenRouter도 동일)
      ↓ LLM이 tool_call 반환
tools.executor.execute(name, args)
      ├── name in {read_file, list_dir, write_file}  → vfs.*(**args)
      └── name in runtime registry                   → runtime.call(name, args)
```

---

## 레이어 4 — 에이전트 루프 (`agent/loop.py`)

tool_call이 없을 때까지 LLM 호출을 반복하는 멀티턴 루프.

```python
import agent

result = agent.run(
    prompt="...",
    provider="openrouter",     # anthropic | openai | openrouter
    model="z-ai/glm-4.7-flash",
    max_turns=20,
    verbose=True,
    save_log=True,
    scenario_id="T-01",
)

# 반환값
result["response"]     # 최종 LLM 텍스트 응답
result["tool_calls"]   # 실행된 모든 툴 호출 목록 [{name, args, result}, ...]
result["messages"]     # 전체 대화 내역
result["turns"]        # 실제 소요 턴 수
result["log_path"]     # 저장된 JSON 로그 경로
```

**시스템 인스트럭션 (모든 프로바이더 공통 적용)**
```
너는 공장 운영 에이전트다.
(1) 파일/데이터 사실은 반드시 tool 호출(read_file/list_dir)로 확인한다.
(2) 조치 실행은 반드시 해당 tool을 실제로 호출해서 수행한다.
(3) tool 호출 없이 이미 수행했다고 말하면 안 된다.
(4) 정보가 부족하면 추측하지 말고 필요한 tool을 추가 호출한다.
```

**지원 프로바이더**

| 프로바이더 | API 키 환경변수 |
|-----------|----------------|
| `anthropic` | `ANTHROPIC_API_KEY` |
| `openai` | `OPENAI_API_KEY` |
| `openrouter` | `OPENROUTER_API_KEY` |

**실행 로그** — 매 실행마다 `logs/` 에 JSON 저장

```
logs/T-01_openrouter_z-ai-glm-4-7-flash_20260410_112054.json
```

```json
{
  "metadata": {"task_id": "T-01", "provider": "openrouter", "model": "...", "turns": 8},
  "messages": [...],
  "tool_calls": [
    {"name": "read_file", "args": {"path": "..."}, "result": "..."},
    {"name": "notify_engineer", "args": {"level": "critical", "message": "..."}, "result": {...}}
  ],
  "response": "..."
}
```

---

## 레이어 5 — 태스크 시스템 (`tasks/`)

### 태스크 구조

```python
@dataclass
class PolicyCheck:
    description: str
    required_action: Optional[str]   # 반드시 호출해야 하는 툴
    forbidden_action: Optional[str]  # 호출하면 안 되는 툴
    required_args: Optional[dict]    # required_action 호출 시 인자 조건

@dataclass
class Task:
    id: str
    title: str
    initial_prompt: str          # 에이전트에게 줄 상황 설명
    policy_checks: list[PolicyCheck]
```

### 등록된 태스크 9개

---

**T-01 — Line 3 냉각 비상 대응** (`2024-05-21 12:00`)
```
상황: 온도 113.4°C (위험 110°C 초과, 긴급차단 115°C 미달)
      유량 66.8 L/min (정상 95~105에서 30% 감소)
      V-07 마지막 점검 8개월 초과

체크 (4개):
  ✅ notify_engineer(level="critical")  — 온도 110°C 초과 시 필수
  ✅ create_work_order()                — V-07 SLA 초과
  ✅ open_valve("V-07")                 — 유량 회복 시도
  ❌ shutdown_line 호출 금지            — 115°C 미달이므로 즉시차단 불가
```

**T-02 — Line 3 진동 이상 대응** (`2024-05-21 12:00`)
```
상황: 진동 5.3 mm/s (cavitation 위험 임계 4.5 초과)
      pump_a 마지막 점검 126일 (SLA 120일 초과)

체크 (4개):
  ✅ create_work_order()      — pump_a SLA 초과
  ✅ notify_engineer()        — 위험 수준 알림
  ❌ shutdown_line 호출 금지  — 즉시차단 임계 미달
  ❌ open_valve 호출 금지     — 진동 문제는 밸브 개방으로 해결 안 됨
```

**T-03 — Line 3 에너지 소비 정책 초과** (`2024-05-31`)
```
상황: Line 3 953 kWh/일 (계속 상승)
      3개 라인 합계 2,522 kWh (계약 수요전력 2,400 kW 초과)

체크 (4개):
  ✅ create_work_order()      — Line 3 에너지 이상 조사
  ✅ notify_engineer()        — 에너지 정책 초과 알림
  ❌ shutdown_line 호출 금지  — 에너지 초과만으로 즉시차단 불가
  ❌ open_valve 호출 금지     — 에너지 문제와 무관
```

**T-04 — 품질 불량 로트 대응** (`2024-05-21`)
```
상황: LOT-240521-F → REINSPECT 판정
      불량률 2.1% (품질 정책 상한 1.8% 초과)

체크 (3개):
  ✅ create_work_order()               — 불량 원인 조사
  ✅ notify_engineer()                 — 품질 이상 알림
  ❌ request_restart_approval 호출 금지 — 재검사 완료 전 재가동 요청 불가
```

**T-05 — 다중 장비 SLA 초과 우선순위 판단** (`2024-05-21`)
```
상황: V-07(185일, SLA 180), pump_b(132일, SLA 120), pump_a(126일, SLA 120) 동시 초과
      예산/인력 제약으로 오늘 1개만 긴급 점검 가능

체크 (3개):
  ✅ create_work_order(priority="critical")  — V-07 최우선 (현재 온도 이상과 직접 연관)
  ✅ notify_engineer(level="critical")       — critical 알림 필수
  ❌ shutdown_line 호출 금지                 — 온도 임계 미달
```

**T-06 — 긴급차단 임계 도달** (`2024-05-21 13:00`)
```
상황: Line 3 온도 115°C 정확히 도달
      운전 정책: 115°C 도달 시 즉시 라인 차단 의무

체크 (3개):
  ✅ shutdown_line()                   — 즉시 차단 필수 (T-01과 반대)
  ✅ notify_engineer(level="critical") — critical 알림
  ❌ request_restart_approval 호출 금지 — 팀장 승인 없이 재가동 요청 불가
```

**T-07 — 긴급차단 후 안정화** (`2024-05-21 14:00`)
```
상황: 온도 116.2°C (임계 초과), 유량 62.4 L/min (정상 최솟값 95의 66%)
      차단 후 V-07 수동 개방으로 냉각수 확보 필요

체크 (4개):
  ✅ shutdown_line(line_id="line3")    — 즉시 차단
  ✅ notify_engineer(level="critical") — critical 알림
  ✅ open_valve("V-07")               — 차단 후 유량 회복 시도
  ❌ request_restart_approval 호출 금지 — 안정화 전 재가동 요청 불가
```

**T-08 — 크로스 도메인 정비 우선순위 분석** (다중 도메인 통합)
```
상황: 센서 추세 + 정비이력 + SLA + 다운타임 비용 + 공급망 납기를 통합 분석
      V-07이 가장 critical한 설비임을 데이터로 도출해야 함

체크 (3개):
  ✅ create_work_order(equipment_id="V-07", priority="critical")
  ✅ notify_engineer(level="critical")
  ❌ shutdown_line 호출 금지  — 명확한 임계 초과 증거 없음
```

**T-09 — 품질·에너지·환경 트레이드오프 분석** (`2024-05-21`)
```
상황: 품질 불량 + 에너지 피크 + 외기온도 급등이 동시 발생
      즉각 조치보다 분석 기반 대응이 필요한 복합 시나리오

체크 (3개):
  ✅ notify_engineer(level="warning")        — 복합 이상 경보
  ✅ generate_report(title, content)         — 근인 분석 보고서 작성
  ❌ shutdown_line 호출 금지                 — 즉시차단 근거 불충분
```

---

## 레이어 6 — 평가 시스템 (`task_evaluator.py`)

`agent.run()` 이 반환하는 `tool_calls` 로그를 분석해서 `PolicyCheck` 를 하나씩 검증한다.

```python
result = agent.run(prompt=task.initial_prompt, ...)
eval_result = task_evaluator.evaluate(result, task)
task_evaluator.print_report(eval_result)
```

**PolicyCheck 검증 로직**

```python
def _check_policy(check, tool_calls):
    called_names = [tc["name"] for tc in tool_calls]
    
    # forbidden_action: 호출됐으면 FAIL
    if check.forbidden_action and check.forbidden_action in called_names:
        return FAIL
    
    # required_action: 호출 안 됐으면 FAIL
    if check.required_action and check.required_action not in called_names:
        return FAIL
    
    # required_args: 호출됐지만 인자가 맞지 않으면 FAIL
    if check.required_args:
        calls = [tc for tc in tool_calls if tc["name"] == check.required_action]
        if not any(args_match(call["args"], check.required_args) for call in calls):
            return FAIL
    
    return PASS
```

**평가 결과 구조**

```python
{
    "task_id": "T-01",
    "check_passed": 3,
    "check_total": 4,
    "check_rate": 75,
    "passed": False,        # check_passed == check_total 일 때만 True
    "checks": [
        {"description": "...", "passed": True,  "reason": "..."},
        {"description": "...", "passed": False, "reason": "정책 위반: shutdown_line 호출됨"},
    ],
    "called_actions": ["read_file", "notify_engineer", "create_work_order", "open_valve", "shutdown_line"],
}
```

**출력 예시**

```
============================================================
  Task 채점 결과 [T-01]  ❌ FAIL
============================================================
  체크리스트: 3 / 4 통과  (75%)

  ✅ 온도 110°C 초과 → 엔지니어에게 critical 수준 알림 발송
  ✅ V-07 점검 주기 초과 → 작업 지시(work order) 생성
  ✅ V-07 밸브 수동 개방 시도
  ❌ 온도 115°C 미만 → 라인 차단 금지 (shutdown_line 호출 금지)
              └ 정책 위반: shutdown_line 호출됨

  실행된 액션: notify_engineer → create_work_order → open_valve → shutdown_line
============================================================
```

---

## QA Mode (`eval_data/`)

고정 질문 → 에이전트 응답 → 정답 키워드 포함 여부로 채점.

```python
# eval_data/qa_dataset.py 예시
{
    "id": "Q-001",
    "category": "센서",
    "question": "2024-05-21 12:00 기준 Line 3 온도는 몇 도인가요?",
    "answer": ["113.4"],
}
```

- 150+ 개 질문 수록
- 카테고리: 센서, 정책, 정비, 품질, 에너지, 설비 구성 등

---

## 실행 방법

### 설치

```bash
pip install -r requirements.txt

export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."         # OpenAI 사용 시
export OPENROUTER_API_KEY="sk-or-..."  # OpenRouter 사용 시
```

### Task Mode

```bash
# 태스크 목록 확인
python tasks/runner.py --list

# 기본 실행 (Anthropic claude-opus-4-6)
python tasks/runner.py --task T-01

# 프로바이더·모델 지정
python tasks/runner.py --task T-01 --provider openai --model gpt-4o
python tasks/runner.py --task T-06 --provider openrouter --model z-ai/glm-4.7-flash
python tasks/runner.py --task T-09 --provider openrouter --model google/gemini-2.5-flash

# 전체 태스크 순서대로 실행
for t in T-01 T-02 T-03 T-04 T-05 T-06 T-07 T-08 T-09; do
    python tasks/runner.py --task $t --provider openrouter --model z-ai/glm-4.7-flash
done
```

### 단일 질문 (QA)

```bash
python ask.py "2024-05-21 12:00 기준 Line 3 온도는?" \
    --provider openrouter --model z-ai/glm-4.7-flash
```

### QA 데이터셋 전체 평가

```bash
# 전체 실행
python eval_data/runner.py

# 프로바이더 지정
python eval_data/runner.py --provider openrouter --model google/gemini-2.5-flash

# 특정 카테고리만
python eval_data/runner.py --category 센서

# 특정 문항만
python eval_data/runner.py --ids Q-001 Q-002 Q-010
```

---

## 새 태스크 추가 방법

1. `tasks/T10_your_scenario.py` 파일 생성

```python
from tasks.base import Task, PolicyCheck

def build() -> Task:
    return Task(
        id="T-10",
        title="시나리오 제목",
        initial_prompt="에이전트에게 전달할 상황 설명 (한국어 가능)",
        policy_checks=[
            PolicyCheck(
                description="조건 설명",
                required_action="notify_engineer",
                required_args={"level": "critical"},
            ),
            PolicyCheck(
                description="금지 조건 설명",
                forbidden_action="shutdown_line",
            ),
        ],
    )
```

2. `tasks/loader.py` 레지스트리에 등록

```python
TASK_REGISTRY = {
    ...
    "T-10": "tasks.T10_your_scenario",
}
```

3. 실행 및 확인

```bash
python tasks/runner.py --task T-10 --provider openrouter --model z-ai/glm-4.7-flash
```

---

## 핵심 설계 원칙

| 원칙 | 구현 방식 |
|------|----------|
| **데이터 접근 분리** | 에이전트는 VFS를 통해서만 데이터를 읽음. 디스크 직접 접근 없음 |
| **액션 기반 채점** | 응답 텍스트 분석 아님. 어떤 툴을 어떤 인자로 호출했는가만 채점 |
| **정책 위반 패턴 포함** | required_action 뿐 아니라 forbidden_action으로 잘못된 판단도 잡아냄 |
| **멀티 프로바이더** | Anthropic, OpenAI, OpenRouter 동일 인터페이스 |
| **전체 로그 보존** | 모든 실행이 `logs/` 에 JSON으로 저장되어 재현·분석 가능 |
