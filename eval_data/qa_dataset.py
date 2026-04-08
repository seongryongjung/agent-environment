"""
QA 평가 데이터셋 (질문 + 키워드 매칭, 확장판)

- 형식: 자유응답 질문 + 정답 키워드 리스트
- 채점: 응답에 정답 키워드 중 하나라도 포함되면 정답
- 범위: 센서/정책/이력/실험/복합 + 조달/재무/환경/운영/품질/심화복합
"""

QA_DATASET = [
    {
        "id": "Q-001",
        "category": "센서",
        "question": "2024-05-21 12:00 기준 Line 3 온도는 몇 도인가요?",
        "answer": [
            "113.4",
            "113.4"
        ]
    },
    {
        "id": "Q-002",
        "category": "센서",
        "question": "Line 3 온도가 100°C를 처음 초과한 시각은 언제인가요?",
        "answer": [
            "09:00"
        ]
    },
    {
        "id": "Q-003",
        "category": "센서",
        "question": "Line 3 유량이 95 L/min 미만으로 처음 내려간 시각은 언제인가요?",
        "answer": [
            "05:00"
        ]
    },
    {
        "id": "Q-004",
        "category": "센서",
        "question": "2024-05-21 12:00 기준 Line 3 유량은 몇 L/min인가요?",
        "answer": [
            "66.8",
            "66.8"
        ]
    },
    {
        "id": "Q-005",
        "category": "센서",
        "question": "2024-05-21 12:00 기준 Line 3 압력은 몇 bar인가요?",
        "answer": [
            "3.05",
            "3.05"
        ]
    },
    {
        "id": "Q-006",
        "category": "센서",
        "question": "2024-05-21 10:00 기준 Line 3 진동 RMS는 얼마인가요?",
        "answer": [
            "4.7",
            "4.7"
        ]
    },
    {
        "id": "Q-007",
        "category": "센서",
        "question": "14:30의 총전력은 몇 kW인가요?",
        "answer": [
            "2425"
        ]
    },
    {
        "id": "Q-008",
        "category": "센서",
        "question": "14:45의 총전력은 몇 kW인가요?",
        "answer": [
            "2440"
        ]
    },
    {
        "id": "Q-009",
        "category": "센서",
        "question": "15:45의 총전력은 몇 kW인가요?",
        "answer": [
            "2335"
        ]
    },
    {
        "id": "Q-010",
        "category": "센서",
        "question": "Line 3 압력은 상승 추세인가요 하락 추세인가요?",
        "answer": [
            "하락",
            "감소"
        ]
    },
    {
        "id": "Q-011",
        "category": "센서",
        "question": "high_freq 데이터에서 valve_open_pct가 70% 미만으로 처음 내려가는 시각은?",
        "answer": [
            "07:03"
        ]
    },
    {
        "id": "Q-012",
        "category": "센서",
        "question": "high_freq 데이터에서 flow_lpm이 80 미만으로 처음 내려가는 시각은?",
        "answer": [
            "08:42"
        ]
    },
    {
        "id": "Q-013",
        "category": "센서",
        "question": "2024-05-21 13:30의 총전력은 몇 kW인가요?",
        "answer": [
            "2280"
        ]
    },
    {
        "id": "Q-014",
        "category": "센서",
        "question": "2024-05-21 13:45의 총전력은 몇 kW인가요?",
        "answer": [
            "2320"
        ]
    },
    {
        "id": "Q-015",
        "category": "센서",
        "question": "2024-05-21 14:00의 총전력은 몇 kW인가요?",
        "answer": [
            "2355"
        ]
    },
    {
        "id": "Q-016",
        "category": "센서",
        "question": "2024-05-21 14:15의 총전력은 몇 kW인가요?",
        "answer": [
            "2380"
        ]
    },
    {
        "id": "Q-017",
        "category": "센서",
        "question": "2024-05-21 14:30의 총전력은 몇 kW인가요?",
        "answer": [
            "2425"
        ]
    },
    {
        "id": "Q-018",
        "category": "센서",
        "question": "2024-05-21 14:45의 총전력은 몇 kW인가요?",
        "answer": [
            "2440"
        ]
    },
    {
        "id": "Q-019",
        "category": "센서",
        "question": "2024-05-21 15:00의 총전력은 몇 kW인가요?",
        "answer": [
            "2410"
        ]
    },
    {
        "id": "Q-020",
        "category": "센서",
        "question": "2024-05-21 15:15의 총전력은 몇 kW인가요?",
        "answer": [
            "2385"
        ]
    },
    {
        "id": "Q-021",
        "category": "센서",
        "question": "2024-05-21 15:30의 총전력은 몇 kW인가요?",
        "answer": [
            "2360"
        ]
    },
    {
        "id": "Q-022",
        "category": "센서",
        "question": "2024-05-01의 Line 3 일일 전력 사용량은 몇 kWh인가요?",
        "answer": [
            "863"
        ]
    },
    {
        "id": "Q-023",
        "category": "센서",
        "question": "2024-05-01의 total_kwh는 얼마인가요?",
        "answer": [
            "2430"
        ]
    },
    {
        "id": "Q-024",
        "category": "센서",
        "question": "2024-05-10의 Line 3 일일 전력 사용량은 몇 kWh인가요?",
        "answer": [
            "890"
        ]
    },
    {
        "id": "Q-025",
        "category": "센서",
        "question": "2024-05-10의 total_kwh는 얼마인가요?",
        "answer": [
            "2458"
        ]
    },
    {
        "id": "Q-026",
        "category": "센서",
        "question": "2024-05-21의 Line 3 일일 전력 사용량은 몇 kWh인가요?",
        "answer": [
            "923"
        ]
    },
    {
        "id": "Q-027",
        "category": "센서",
        "question": "2024-05-21의 total_kwh는 얼마인가요?",
        "answer": [
            "2489"
        ]
    },
    {
        "id": "Q-028",
        "category": "센서",
        "question": "2024-05-31의 Line 3 일일 전력 사용량은 몇 kWh인가요?",
        "answer": [
            "953"
        ]
    },
    {
        "id": "Q-029",
        "category": "센서",
        "question": "2024-05-31의 total_kwh는 얼마인가요?",
        "answer": [
            "2522"
        ]
    },
    {
        "id": "Q-030",
        "category": "정책",
        "question": "운전 가드레일 정책 v3.1에서 105°C 초과 시 최소 감속률은 몇 %인가요?",
        "answer": [
            "15%",
            "15"
        ]
    },
    {
        "id": "Q-031",
        "category": "정책",
        "question": "운전 가드레일 정책 v3.1에서 팀장 호출 임계 온도는 몇 도인가요?",
        "answer": [
            "110"
        ]
    },
    {
        "id": "Q-032",
        "category": "정책",
        "question": "운전 가드레일 정책 v3.1에서 긴급차단 임계 온도는 몇 도인가요?",
        "answer": [
            "115"
        ]
    },
    {
        "id": "Q-033",
        "category": "정책",
        "question": "운전 가드레일 정책 v3.1에서 금지된 조치는 무엇인가요?",
        "answer": [
            "증산"
        ]
    },
    {
        "id": "Q-034",
        "category": "정책",
        "question": "정비 SLA 정책에서 밸브(V-05~07) 점검 주기는 며칠인가요?",
        "answer": [
            "180"
        ]
    },
    {
        "id": "Q-035",
        "category": "정책",
        "question": "정비 SLA 정책에서 pump_a 점검 주기는 며칠인가요?",
        "answer": [
            "120"
        ]
    },
    {
        "id": "Q-036",
        "category": "정책",
        "question": "SLA 초과 61일 이상이면 어떤 등급인가요?",
        "answer": [
            "위험"
        ]
    },
    {
        "id": "Q-037",
        "category": "정책",
        "question": "에너지 정책의 피크 시간대는 언제인가요?",
        "answer": [
            "14:00~17:00",
            "14:00"
        ]
    },
    {
        "id": "Q-038",
        "category": "정책",
        "question": "계약 수요전력 기준은 몇 kW인가요?",
        "answer": [
            "2400"
        ]
    },
    {
        "id": "Q-039",
        "category": "정책",
        "question": "2300 kW 초과 시 권고되는 사전 감속률은 몇 %인가요?",
        "answer": [
            "5%",
            "5"
        ]
    },
    {
        "id": "Q-040",
        "category": "정책",
        "question": "2400 kW 초과 시 우선 차단 대상 부하는 무엇인가요?",
        "answer": [
            "비필수"
        ]
    },
    {
        "id": "Q-041",
        "category": "정책",
        "question": "데이터 신뢰도 정책에서 C 센서 단독 정지판단은 가능한가요?",
        "answer": [
            "금지",
            "불가"
        ]
    },
    {
        "id": "Q-042",
        "category": "정책",
        "question": "데이터 신뢰도 정책에서 교차 확인에 필요한 독립 지표 최소 개수는?",
        "answer": [
            "2"
        ]
    },
    {
        "id": "Q-043",
        "category": "정책",
        "question": "출하 승인 정책의 수율 하한은 몇 %인가요?",
        "answer": [
            "96.5"
        ]
    },
    {
        "id": "Q-044",
        "category": "정책",
        "question": "출하 승인 정책의 불량률 상한은 몇 %인가요?",
        "answer": [
            "1.8"
        ]
    },
    {
        "id": "Q-045",
        "category": "정책",
        "question": "출하 승인 정책의 핵심 온도 편차 상한은 얼마인가요?",
        "answer": [
            "2.5"
        ]
    },
    {
        "id": "Q-046",
        "category": "정책",
        "question": "대응 우선순위 매트릭스 1순위는 무엇인가요?",
        "answer": [
            "안전"
        ]
    },
    {
        "id": "Q-047",
        "category": "정책",
        "question": "대응 순서에서 원인 분석은 어느 순서인가요?",
        "answer": [
            "B"
        ]
    },
    {
        "id": "Q-048",
        "category": "정책",
        "question": "대응 순서에서 에너지 최적화는 어느 순서인가요?",
        "answer": [
            "C"
        ]
    },
    {
        "id": "Q-049",
        "category": "정책",
        "question": "policy change log 기준 v2.4에서 v3.1로 바뀌며 팀장 호출 임계는 몇 도에서 몇 도로 바뀌었나요?",
        "answer": [
            "112",
            "110"
        ]
    },
    {
        "id": "Q-050",
        "category": "정책",
        "question": "policy change log에서 감속 기준은 몇 %에서 몇 %로 상향되었나요?",
        "answer": [
            "10%",
            "15%"
        ]
    },
    {
        "id": "Q-051",
        "category": "정책",
        "question": "E-110 override 권한 역할은 누구인가요?",
        "answer": [
            "PlantManager"
        ]
    },
    {
        "id": "Q-052",
        "category": "정책",
        "question": "E-115 override 최대 허용 시간은 몇 분인가요?",
        "answer": [
            "15"
        ]
    },
    {
        "id": "Q-053",
        "category": "정책",
        "question": "결측률 5% 초과 파일은 어떤 용도로만 사용 가능한가요?",
        "answer": [
            "분석용"
        ]
    },
    {
        "id": "Q-055",
        "category": "이력",
        "question": "교대 인수인계 로그에서 감속 적용 시각은 언제인가요?",
        "answer": [
            "06:20"
        ]
    },
    {
        "id": "Q-056",
        "category": "이력",
        "question": "교대 인수인계 로그에서 적용된 감속률은 몇 %인가요?",
        "answer": [
            "10%",
            "10"
        ]
    },
    {
        "id": "Q-057",
        "category": "이력",
        "question": "교대 인수인계 로그의 설비팀장 내선 번호는?",
        "answer": [
            "201"
        ]
    },
    {
        "id": "Q-058",
        "category": "이력",
        "question": "알람 타임라인에서 첫 알람 코드는 무엇인가요?",
        "answer": [
            "ALM-FLOW-L3-LOW"
        ]
    },
    {
        "id": "Q-059",
        "category": "이력",
        "question": "유량 저하 알람은 온도 고경보보다 몇 분 선행했나요?",
        "answer": [
            "36"
        ]
    },
    {
        "id": "Q-060",
        "category": "이력",
        "question": "정비 마스터 로그에서 V-07 마지막 점검일은?",
        "answer": [
            "2023-11-18"
        ]
    },
    {
        "id": "Q-061",
        "category": "이력",
        "question": "정비 마스터 로그에서 V-06 마지막 점검일은?",
        "answer": [
            "2024-02-14"
        ]
    },
    {
        "id": "Q-062",
        "category": "이력",
        "question": "품질 배치 M240518 판정은 무엇인가요?",
        "answer": [
            "승인"
        ]
    },
    {
        "id": "Q-063",
        "category": "이력",
        "question": "품질 배치 M240520 판정은 무엇인가요?",
        "answer": [
            "보류"
        ]
    },
    {
        "id": "Q-064",
        "category": "이력",
        "question": "품질 배치 M240521 판정은 무엇인가요?",
        "answer": [
            "재검사"
        ]
    },
    {
        "id": "Q-065",
        "category": "이력",
        "question": "M240521의 불량률은 몇 %인가요?",
        "answer": [
            "2.1"
        ]
    },
    {
        "id": "Q-066",
        "category": "이력",
        "question": "M240521의 온도 편차는 얼마인가요?",
        "answer": [
            "2.8"
        ]
    },
    {
        "id": "Q-067",
        "category": "이력",
        "question": "센서 교정 로그에서 line3_flow_sensor 교정일은?",
        "answer": [
            "2024-01-15"
        ]
    },
    {
        "id": "Q-068",
        "category": "이력",
        "question": "센서 교정 로그에서 line3_temp_sensor 교정일은?",
        "answer": [
            "2024-04-10"
        ]
    },
    {
        "id": "Q-069",
        "category": "이력",
        "question": "예비품 재고에서 V-07 교체용 밸브는 몇 개인가요?",
        "answer": [
            "1"
        ]
    },
    {
        "id": "Q-070",
        "category": "이력",
        "question": "예비품 재고에서 라인3 유량 센서는 몇 개인가요?",
        "answer": [
            "2"
        ]
    },
    {
        "id": "Q-071",
        "category": "이력",
        "question": "예비품 재고에서 보조 히터 컨택터는 몇 개인가요?",
        "answer": [
            "3"
        ]
    },
    {
        "id": "Q-072",
        "category": "이력",
        "question": "incident ticket INC-240521-03의 suspected root cause는?",
        "answer": [
            "V-07"
        ]
    },
    {
        "id": "Q-073",
        "category": "이력",
        "question": "incident ticket INC-240521-03의 resolution 상태는?",
        "answer": [
            "pending"
        ]
    },
    {
        "id": "Q-074",
        "category": "이력",
        "question": "audit finding 중 high severity open 항목 ID는?",
        "answer": [
            "F-2024-031"
        ]
    },
    {
        "id": "Q-075",
        "category": "이력",
        "question": "audit finding F-2024-044의 영역(area)은?",
        "answer": [
            "maintenance"
        ]
    },
    {
        "id": "Q-076",
        "category": "이력",
        "question": "raw alarm events에서 10:12 알람 자산은?",
        "answer": [
            "PUMP-A"
        ]
    },
    {
        "id": "Q-077",
        "category": "이력",
        "question": "raw alarm events에서 09:03 알람 priority는?",
        "answer": [
            "P1"
        ]
    },
    {
        "id": "Q-078",
        "category": "이력",
        "question": "multi day shift note에서 05-20에 반복 보고된 의심 이슈는?",
        "answer": [
            "응답 지연",
            "stick-slip"
        ]
    },
    {
        "id": "Q-079",
        "category": "실험",
        "question": "throttle test에서 T2의 예상 절감량은 몇 kW인가요?",
        "answer": [
            "92"
        ]
    },
    {
        "id": "Q-080",
        "category": "실험",
        "question": "throttle test에서 전체 5% 감속(T4)의 품질 리스크는?",
        "answer": [
            "high"
        ]
    },
    {
        "id": "Q-081",
        "category": "실험",
        "question": "load shedding L1의 예상 절감량은?",
        "answer": [
            "45"
        ]
    },
    {
        "id": "Q-082",
        "category": "실험",
        "question": "load shedding L2의 예상 절감량은?",
        "answer": [
            "65"
        ]
    },
    {
        "id": "Q-083",
        "category": "실험",
        "question": "load shedding L2의 리스크는?",
        "answer": [
            "low"
        ]
    },
    {
        "id": "Q-084",
        "category": "실험",
        "question": "coolant additive C2(1.0%)의 회복률은?",
        "answer": [
            "7.5"
        ]
    },
    {
        "id": "Q-085",
        "category": "실험",
        "question": "coolant additive C3의 부작용은?",
        "answer": [
            "foam"
        ]
    },
    {
        "id": "Q-086",
        "category": "실험",
        "question": "V-07 valve 교체 비용은 얼마인가요?",
        "answer": [
            "6800"
        ]
    },
    {
        "id": "Q-087",
        "category": "실험",
        "question": "V-07 seal kit 리드타임은 며칠인가요?",
        "answer": [
            "1"
        ]
    },
    {
        "id": "Q-088",
        "category": "실험",
        "question": "R2 시나리오의 temp_to_90_time_min은?",
        "answer": [
            "52"
        ]
    },
    {
        "id": "Q-089",
        "category": "실험",
        "question": "temp_to_90이 가장 빠른 recovery 시나리오는?",
        "answer": [
            "R2"
        ]
    },
    {
        "id": "Q-090",
        "category": "실험",
        "question": "whatif 시나리오 중 risk_score가 가장 높은 것은?",
        "answer": [
            "S3"
        ]
    },
    {
        "id": "Q-091",
        "category": "실험",
        "question": "whatif에서 temp 111에서 policy compliant인 action은?",
        "answer": [
            "slowdown_18pct_and_call"
        ]
    },
    {
        "id": "Q-092",
        "category": "실험",
        "question": "DOE에서 temp=88, flow=100, valve=85 조건의 yield_pct는?",
        "answer": [
            "96.45"
        ]
    },
    {
        "id": "Q-093",
        "category": "실험",
        "question": "DOE에서 temp=92, flow=90, valve=55 조건의 total_kw는?",
        "answer": [
            "2454"
        ]
    },
    {
        "id": "Q-094",
        "category": "복합",
        "question": "운전 정책(>105°C에서 15% 감속)과 교대 로그(06:20 10% 감속)를 비교하면 조치 적합성은?",
        "answer": [
            "미달",
            "부족"
        ]
    },
    {
        "id": "Q-095",
        "category": "복합",
        "question": "운전 정책과 12:00 온도(113.4°C)를 함께 보면 즉시 필요한 커뮤니케이션 조치는?",
        "answer": [
            "설비팀장"
        ]
    },
    {
        "id": "Q-096",
        "category": "복합",
        "question": "운전 정책과 12:00 온도 기준으로 긴급차단까지 남은 온도 여유는 몇 도인가요?",
        "answer": [
            "1.6"
        ]
    },
    {
        "id": "Q-097",
        "category": "복합",
        "question": "에너지 정책(2400)과 14:30 전력(2425)을 함께 보면 현재 상태를 한 단어로 말하면?",
        "answer": [
            "초과"
        ]
    },
    {
        "id": "Q-099",
        "category": "복합",
        "question": "14:45 전력 2440에서 L1+L2(110) 적용 후 추정 전력은?",
        "answer": [
            "2330"
        ]
    },
    {
        "id": "Q-100",
        "category": "복합",
        "question": "line3_flow_sensor 교정일과 주기(120일)를 비교하면 2024-05-21 기준 상태는?",
        "answer": [
            "만료"
        ]
    },
    {
        "id": "Q-101",
        "category": "복합",
        "question": "line3_temp_sensor 교정일과 주기(90일)를 비교하면 2024-05-21 기준 상태는?",
        "answer": [
            "유효"
        ]
    },
    {
        "id": "Q-102",
        "category": "복합",
        "question": "data reliability + exceptions를 함께 보면 C 센서 단독 자동정지 판단은?",
        "answer": [
            "금지",
            "불가"
        ]
    },
    {
        "id": "Q-103",
        "category": "복합",
        "question": "알람 첫 이벤트(유량저하)와 사례집 전례를 합치면 우선 점검 대상 장비는?",
        "answer": [
            "V-07"
        ]
    },
    {
        "id": "Q-104",
        "category": "복합",
        "question": "품질 정책(불량<=1.8, 편차<=2.5)과 M240521(2.1,2.8)을 비교한 판정은?",
        "answer": [
            "재검사",
            "보류"
        ]
    },
    {
        "id": "Q-105",
        "category": "복합",
        "question": "SLA(180일)와 V-07 점검일(2023-11-18)을 2024-05-21 기준으로 비교하면 상태는?",
        "answer": [
            "초과"
        ]
    },
    {
        "id": "Q-106",
        "category": "복합",
        "question": "response priority에서 고온+전력초과 동시 발생 시 우선순위 1은?",
        "answer": [
            "안전"
        ]
    },
    {
        "id": "Q-107",
        "category": "복합",
        "question": "whatif S3(action increase_output_5pct)와 금지조항을 비교한 정책 준수 여부는?",
        "answer": [
            "미준수",
            "금지"
        ]
    },
    {
        "id": "Q-108",
        "category": "복합",
        "question": "whatif S4는 정책 준수 시나리오인가요?",
        "answer": [
            "yes",
            "준수"
        ]
    },
    {
        "id": "Q-109",
        "category": "복합",
        "question": "pump manual 진동 임계(4.5)와 10:00 값(4.7) 비교 결과 위험 판정은?",
        "answer": [
            "초과",
            "위험"
        ]
    },
    {
        "id": "Q-110",
        "category": "복합",
        "question": "dependency graph에서 Line3-Reactor cooling 체인 핵심 자산 3개는?",
        "answer": [
            "PUMP-A",
            "V-07",
            "HX-31"
        ]
    },
    {
        "id": "Q-111",
        "category": "복합",
        "question": "v2.4와 v3.1 비교 시 더 엄격한 버전은?",
        "answer": [
            "v3.1"
        ]
    },
    {
        "id": "Q-112",
        "category": "복합",
        "question": "policy change log에서 팀장 호출 임계는 몇 도에서 몇 도로 강화됐나요?",
        "answer": [
            "112",
            "110"
        ]
    },
    {
        "id": "Q-113",
        "category": "복합",
        "question": "13:45 전력(2320)은 정책상 어떤 조치 권고 대상인가요?",
        "answer": [
            "사전 감속"
        ]
    },
    {
        "id": "Q-115",
        "category": "복합",
        "question": "line3 12:00 유량(66.8)과 정상하한(95) 차이는?",
        "answer": [
            "28.2"
        ]
    },
    {
        "id": "Q-116",
        "category": "복합",
        "question": "ticket INC-240521-03과 2022 사례집을 함께 보면 공통 root cause 키워드는?",
        "answer": [
            "V-07"
        ]
    },
    {
        "id": "Q-117",
        "category": "복합",
        "question": "audit F-2024-031(open, high)와 교대 감속 10%를 함께 보면 운영 리스크 유형은?",
        "answer": [
            "준수",
            "미달"
        ]
    },
    {
        "id": "Q-118",
        "category": "복합",
        "question": "E-110 override role은 ShiftLeader인가 PlantManager인가?",
        "answer": [
            "PlantManager"
        ]
    },
    {
        "id": "Q-120",
        "category": "복합",
        "question": "historical monthly에서 line3_avg_kwh_day 추세는?",
        "answer": [
            "증가"
        ]
    },
    {
        "id": "Q-123",
        "category": "복합",
        "question": "교대 로그에 팀장 보고 완료가 있어도 감속 기준 미달이면 정책 준수 평가 키워드는?",
        "answer": [
            "미달"
        ]
    },
    {
        "id": "Q-124",
        "category": "조달",
        "question": "supplier SUP-001의 업체명은 무엇인가요?",
        "answer": [
            "CoreValve Systems"
        ]
    },
    {
        "id": "Q-125",
        "category": "조달",
        "question": "flow sensor module의 주요 공급사 country는 어디인가요?",
        "answer": [
            "JP"
        ]
    },
    {
        "id": "Q-126",
        "category": "조달",
        "question": "V-07 valve body의 계약 티어는 무엇인가요?",
        "answer": [
            "A"
        ]
    },
    {
        "id": "Q-127",
        "category": "조달",
        "question": "supplier 중 otd_score가 가장 높은 업체 ID는?",
        "answer": [
            "SUP-005"
        ]
    },
    {
        "id": "Q-128",
        "category": "조달",
        "question": "2024-W14 기준 V-07 valve body의 actual_days는?",
        "answer": [
            "3"
        ]
    },
    {
        "id": "Q-129",
        "category": "조달",
        "question": "2024-W20 기준 V-07 valve body의 p95_days는?",
        "answer": [
            "5"
        ]
    },
    {
        "id": "Q-130",
        "category": "조달",
        "question": "open 상태인 PO 수는 몇 개인가요?",
        "answer": [
            "2"
        ]
    },
    {
        "id": "Q-131",
        "category": "조달",
        "question": "PO-240519-06의 unit_cost_usd는 얼마인가요?",
        "answer": [
            "6900"
        ]
    },
    {
        "id": "Q-132",
        "category": "조달",
        "question": "critical spares 정책에서 flow sensor module의 reorder_point는?",
        "answer": [
            "2"
        ]
    },
    {
        "id": "Q-133",
        "category": "조달",
        "question": "pump seal kit의 review_cycle_days는?",
        "answer": [
            "14"
        ]
    },
    {
        "id": "Q-134",
        "category": "조달",
        "question": "V-07 valve body의 min_onhand와 target_onhand는 각각 얼마인가요?",
        "answer": [
            "1",
            "2"
        ]
    },
    {
        "id": "Q-135",
        "category": "조달",
        "question": "purchase order 중 supplier SUP-001가 발행한 PO 개수는?",
        "answer": [
            "2"
        ]
    },
    {
        "id": "Q-136",
        "category": "조달",
        "question": "supplier SUP-004의 critical_part는 무엇인가요?",
        "answer": [
            "motor inverter"
        ]
    },
    {
        "id": "Q-137",
        "category": "조달",
        "question": "SUP-003의 contract_tier는 무엇인가요?",
        "answer": [
            "B"
        ]
    },
    {
        "id": "Q-138",
        "category": "조달",
        "question": "V-07 valve body의 최근 open PO ID는?",
        "answer": [
            "PO-240519-06"
        ]
    },
    {
        "id": "Q-139",
        "category": "재무",
        "question": "2024-Q2 peak rate_usd_per_kwh는 얼마인가요?",
        "answer": [
            "0.159"
        ]
    },
    {
        "id": "Q-140",
        "category": "재무",
        "question": "2024-Q2 peak demand_charge_usd_per_kw는?",
        "answer": [
            "9.5"
        ]
    },
    {
        "id": "Q-141",
        "category": "재무",
        "question": "L3의 cost_usd_per_min은 얼마인가요?",
        "answer": [
            "78"
        ]
    },
    {
        "id": "Q-142",
        "category": "재무",
        "question": "L3의 penalty_risk_level은 무엇인가요?",
        "answer": [
            "high"
        ]
    },
    {
        "id": "Q-143",
        "category": "재무",
        "question": "2024-05-07 PUMP-A corrective 작업의 total_usd는?",
        "answer": [
            "1520"
        ]
    },
    {
        "id": "Q-144",
        "category": "재무",
        "question": "2024-05의 monthly_pnl_proxy는 얼마인가요?",
        "answer": [
            "109600"
        ]
    },
    {
        "id": "Q-145",
        "category": "재무",
        "question": "2024-05의 quality_loss_usd는 얼마인가요?",
        "answer": [
            "8700"
        ]
    },
    {
        "id": "Q-146",
        "category": "재무",
        "question": "2024-03 대비 2024-05의 energy_cost_usd 증감폭은?",
        "answer": [
            "3300"
        ]
    },
    {
        "id": "Q-147",
        "category": "재무",
        "question": "L1과 L3의 분당 다운타임 비용 차이는?",
        "answer": [
            "36"
        ]
    },
    {
        "id": "Q-148",
        "category": "재무",
        "question": "2024-Q2 midpeak rate는 offpeak보다 높은가요? 키워드로 답하면?",
        "answer": [
            "높"
        ]
    },
    {
        "id": "Q-149",
        "category": "재무",
        "question": "maintenance ledger에서 가장 큰 total_usd 작업은 어떤 asset_id인가요?",
        "answer": [
            "PUMP-A"
        ]
    },
    {
        "id": "Q-150",
        "category": "재무",
        "question": "2024-01에서 2024-05로 net_margin_proxy는 증가했나요 감소했나요?",
        "answer": [
            "감소"
        ]
    },
    {
        "id": "Q-151",
        "category": "재무",
        "question": "2024-04의 maintenance_cost_usd는 얼마인가요?",
        "answer": [
            "10100"
        ]
    },
    {
        "id": "Q-152",
        "category": "재무",
        "question": "L2의 lost_output_units_per_min은?",
        "answer": [
            "1.6"
        ]
    },
    {
        "id": "Q-153",
        "category": "환경",
        "question": "2024-05-21 12:00의 ambient_celsius는?",
        "answer": [
            "23.69"
        ]
    },
    {
        "id": "Q-154",
        "category": "환경",
        "question": "2024-05-21 12:00의 wetbulb_celsius는?",
        "answer": [
            "21.89"
        ]
    },
    {
        "id": "Q-155",
        "category": "환경",
        "question": "2024-05-21 12:00의 humidity_pct는?",
        "answer": [
            "55.96"
        ]
    },
    {
        "id": "Q-156",
        "category": "환경",
        "question": "ambient 24°C일 때 cooling tower efficiency_pct는?",
        "answer": [
            "85.7"
        ]
    },
    {
        "id": "Q-157",
        "category": "환경",
        "question": "ambient 28°C에서 approach_temp_c는?",
        "answer": [
            "7.4"
        ]
    },
    {
        "id": "Q-158",
        "category": "환경",
        "question": "weather 데이터에서 00:00 대비 23:00 ambient 온도 추세는 상승/하락 중 무엇인가요?",
        "answer": [
            "상승"
        ]
    },
    {
        "id": "Q-159",
        "category": "환경",
        "question": "humidity 데이터에서 00:00 대비 23:00 습도 추세는 상승/하락 중 무엇인가요?",
        "answer": [
            "하락"
        ]
    },
    {
        "id": "Q-160",
        "category": "환경",
        "question": "ambient 22°C에서 efficiency_pct는 얼마인가요?",
        "answer": [
            "88.2"
        ]
    },
    {
        "id": "Q-161",
        "category": "환경",
        "question": "ambient 18°C와 28°C의 efficiency 차이는 몇 %p인가요?",
        "answer": [
            "10.9"
        ]
    },
    {
        "id": "Q-162",
        "category": "환경",
        "question": "2024-05-21 08:00의 wind_mps는?",
        "answer": [
            "2.1"
        ]
    },
    {
        "id": "Q-163",
        "category": "환경",
        "question": "wetbulb가 ambient보다 항상 낮은가요? 키워드로 답하면?",
        "answer": [
            "낮"
        ]
    },
    {
        "id": "Q-164",
        "category": "환경",
        "question": "humidity_hourly의 최소 humidity 값은 대략 몇 %인가요?",
        "answer": [
            "42.42"
        ]
    },
    {
        "id": "Q-165",
        "category": "운영",
        "question": "2024-05-21의 shift_a_lead는 누구인가요?",
        "answer": [
            "Kim"
        ]
    },
    {
        "id": "Q-166",
        "category": "운영",
        "question": "2024-05-20의 planned_line3_rate_pct는 몇 %인가요?",
        "answer": [
            "95"
        ]
    },
    {
        "id": "Q-167",
        "category": "운영",
        "question": "operator skill matrix에서 cert_level이 L4인 작업자는?",
        "answer": [
            "Choi"
        ]
    },
    {
        "id": "Q-168",
        "category": "운영",
        "question": "Kim의 process_control 점수는?",
        "answer": [
            "5"
        ]
    },
    {
        "id": "Q-169",
        "category": "운영",
        "question": "line3_recipe 최신 버전은 무엇인가요?",
        "answer": [
            "R3-2.3"
        ]
    },
    {
        "id": "Q-170",
        "category": "운영",
        "question": "R3-2.3의 target_temp_c는?",
        "answer": [
            "86"
        ]
    },
    {
        "id": "Q-171",
        "category": "운영",
        "question": "R3-2.1 대비 R3-2.3에서 target_pressure_bar는 몇 bar 낮아졌나요?",
        "answer": [
            "0.1"
        ]
    },
    {
        "id": "Q-172",
        "category": "운영",
        "question": "ops_shift에서 planned_line3_rate_pct가 95인 날짜는 5월 기준 몇 일 간격으로 나타나나요? 키워드로 답하면?",
        "answer": [
            "5"
        ]
    },
    {
        "id": "Q-173",
        "category": "운영",
        "question": "Lee의 pump_diagnostics 점수는?",
        "answer": [
            "4"
        ]
    },
    {
        "id": "Q-174",
        "category": "운영",
        "question": "Park의 cert_level은?",
        "answer": [
            "L2"
        ]
    },
    {
        "id": "Q-175",
        "category": "품질",
        "question": "LOT-240521-F의 decision은 무엇인가요?",
        "answer": [
            "reinspect"
        ]
    },
    {
        "id": "Q-176",
        "category": "품질",
        "question": "LOT-240503-C의 yield_pct는?",
        "answer": [
            "96.4"
        ]
    },
    {
        "id": "Q-177",
        "category": "품질",
        "question": "defect code D-101의 severity는?",
        "answer": [
            "high"
        ]
    },
    {
        "id": "Q-178",
        "category": "품질",
        "question": "dimension drift의 defect_code는?",
        "answer": [
            "D-142"
        ]
    },
    {
        "id": "Q-179",
        "category": "품질",
        "question": "LOT-240521-F rework 결과(result)는?",
        "answer": [
            "conditional"
        ]
    },
    {
        "id": "Q-180",
        "category": "품질",
        "question": "LOT-240521-F raw surface index 첫 값은?",
        "answer": [
            "1.0"
        ]
    },
    {
        "id": "Q-181",
        "category": "품질",
        "question": "LOT-240521-F raw surface index 마지막 값은?",
        "answer": [
            "1.24"
        ]
    },
    {
        "id": "Q-182",
        "category": "품질",
        "question": "LOT-240521-F의 surface_defect_index는 전반적으로 LOT-240503-C보다 높은가요? 키워드로 답하면?",
        "answer": [
            "높"
        ]
    },
    {
        "id": "Q-183",
        "category": "품질",
        "question": "inspection lot 결과에서 line L3의 release 건수는?",
        "answer": [
            "1"
        ]
    },
    {
        "id": "Q-184",
        "category": "품질",
        "question": "inspection lot 결과에서 reinspect 건수는?",
        "answer": [
            "1"
        ]
    },
    {
        "id": "Q-185",
        "category": "품질",
        "question": "D-121의 typical_root_cause는?",
        "answer": [
            "cooling instability"
        ]
    },
    {
        "id": "Q-186",
        "category": "품질",
        "question": "rework_log에서 thermal re-balance 작업 시간은 몇 시간인가요?",
        "answer": [
            "5.5"
        ]
    },
    {
        "id": "Q-187",
        "category": "심화복합",
        "question": "주간 리뷰 week21과 total_power_15min을 함께 보면 peak demand 위반 시각 2개는?",
        "answer": [
            "14:30",
            "14:45"
        ]
    },
    {
        "id": "Q-188",
        "category": "심화복합",
        "question": "postmortem INC-240401-17의 root cause와 사례집 전례를 함께 보면 공통 키워드는?",
        "answer": [
            "V-07"
        ]
    },
    {
        "id": "Q-189",
        "category": "심화복합",
        "question": "policy violations에서 open인 operation_guardrail 위반 건수는?",
        "answer": [
            "2"
        ]
    },
    {
        "id": "Q-190",
        "category": "심화복합",
        "question": "control_strategy_ablation에서 peak_temp가 가장 높은 전략은?",
        "answer": [
            "aggressive_speedup"
        ]
    },
    {
        "id": "Q-191",
        "category": "심화복합",
        "question": "ablation에서 energy_kwh가 가장 낮은 전략은?",
        "answer": [
            "shed_bundle_L1L2"
        ]
    },
    {
        "id": "Q-192",
        "category": "심화복합",
        "question": "ablation baseline 대비 slowdown_15의 defect_pct 개선폭은?",
        "answer": [
            "0.4"
        ]
    },
    {
        "id": "Q-193",
        "category": "심화복합",
        "question": "monte carlo 100runs에서 failure_risk_score가 0.5를 초과하는 run 수는?",
        "answer": [
            "14"
        ]
    },
    {
        "id": "Q-194",
        "category": "심화복합",
        "question": "zone map에서 safety_class가 critical인 zone은?",
        "answer": [
            "Cooling-B"
        ]
    },
    {
        "id": "Q-195",
        "category": "심화복합",
        "question": "zone map의 Cooling-B assets 목록에 포함된 핵심 밸브는?",
        "answer": [
            "V-07"
        ]
    },
    {
        "id": "Q-196",
        "category": "심화복합",
        "question": "공급망 critical spares policy와 spare inventory를 함께 보면 V-07 valve body는 최소 재고를 충족하나요? 키워드로 답하면?",
        "answer": [
            "충족"
        ]
    },
    {
        "id": "Q-197",
        "category": "심화복합",
        "question": "finance downtime 모델과 operation priority를 함께 보면 L3 downtime은 high risk인가요?",
        "answer": [
            "high"
        ]
    },
    {
        "id": "Q-198",
        "category": "심화복합",
        "question": "weather(고온 상승)와 cooling tower curve를 함께 보면 오후로 갈수록 효율은 상승/하락 중?",
        "answer": [
            "하락"
        ]
    },
    {
        "id": "Q-199",
        "category": "심화복합",
        "question": "purchase order open 건 중 V-07 valve body의 최신 unit_cost_usd는?",
        "answer": [
            "6900"
        ]
    },
    {
        "id": "Q-200",
        "category": "심화복합",
        "question": "recipe 버전 변경(R3-2.1->2.3)과 quality lot 결과를 함께 볼 때 안정화 의도 지표는 target_temp 하향인가 상향인가?",
        "answer": [
            "하향"
        ]
    },
    {
        "id": "Q-201",
        "category": "심화복합",
        "question": "policy violation PV-240521-03 설명과 operation guardrail 정책을 함께 보면 위반 키워드는?",
        "answer": [
            "output increase",
            "증산"
        ]
    },
    {
        "id": "Q-202",
        "category": "심화복합",
        "question": "weekly review week20 권고사항과 shift 로그를 함께 볼 때 강화가 필요한 항목은 15% slowdown rule인가요?",
        "answer": [
            "15%"
        ]
    },
    {
        "id": "Q-203",
        "category": "심화복합",
        "question": "risk/cost 관점에서 monte carlo의 평균 mttr_min은 대략 몇 분대인가요? (정수 반올림)",
        "answer": [
            "55"
        ]
    }
]
