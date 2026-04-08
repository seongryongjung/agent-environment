from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import List

ROOT = Path('/Users/seongryongjung/Desktop/agent environment')
QA_PATH = ROOT / 'eval_data' / 'qa_dataset.py'


TIME_RE = re.compile(r'^(\d{2}):(\d{2})$')
NUM_RE = re.compile(r'^[-+]?\d+(?:\.\d+)?$')
PCT_RE = re.compile(r'^([-+]?\d+(?:\.\d+)?)%$')

YN_SET = {"가능", "불가", "유효", "만료", "초과", "미달", "위험", "주의", "경고", "승인", "보류", "재검사", "증가", "하락", "맞다", "아니다", "yes", "no", "수행", "미수행", "완료"}
YN_DISTRACTORS = {
    "가능": ["불가", "미달", "아니다", "no"],
    "불가": ["가능", "유효", "맞다", "yes"],
    "유효": ["만료", "불가", "아니다", "no"],
    "만료": ["유효", "가능", "맞다", "yes"],
    "초과": ["미달", "주의", "경고", "아니다"],
    "미달": ["초과", "가능", "맞다", "yes"],
    "위험": ["주의", "경고", "유효", "가능"],
    "주의": ["위험", "경고", "안전", "유효"],
    "경고": ["주의", "위험", "유효", "가능"],
    "승인": ["보류", "재검사", "불가", "미달"],
    "보류": ["승인", "재검사", "가능", "유효"],
    "재검사": ["승인", "보류", "가능", "유효"],
    "증가": ["하락", "미달", "감소", "안정"],
    "하락": ["증가", "상승", "유지", "초과"],
    "맞다": ["아니다", "불가", "no", "미달"],
    "아니다": ["맞다", "가능", "yes", "초과"],
    "yes": ["no", "아니다", "불가", "미달"],
    "no": ["yes", "맞다", "가능", "초과"],
    "수행": ["미수행", "불가", "아니다", "no"],
    "미수행": ["수행", "완료", "맞다", "yes"],
    "완료": ["미수행", "불가", "아니다", "no"],
}


def load_qa() -> list[dict]:
    ns: dict = {}
    exec(QA_PATH.read_text(encoding='utf-8'), ns)
    return ns['QA_DATASET']


def fmt_num(v: float, decimals: int | None = None) -> str:
    if decimals is None:
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.1f}".rstrip('0').rstrip('.')
    if decimals == 0:
        return str(int(round(v)))
    return f"{v:.{decimals}f}".rstrip('0').rstrip('.')


def distractors_for_time(ans: str) -> List[str]:
    m = TIME_RE.match(ans)
    if not m:
        return []
    h = int(m.group(1))
    mi = int(m.group(2))
    base = h * 60 + mi
    vals = []
    for d in (-30, -15, 15, 30):
        t = (base + d) % (24 * 60)
        vals.append(f"{t // 60:02d}:{t % 60:02d}")
    return vals


def distractors_for_percent(ans: str) -> List[str]:
    m = PCT_RE.match(ans)
    if not m:
        return []
    x = float(m.group(1))
    return [f"{fmt_num(x - 2)}%", f"{fmt_num(x - 1)}%", f"{fmt_num(x + 1)}%", f"{fmt_num(x + 2)}%"]


def distractors_for_number(ans: str) -> List[str]:
    s = ans.replace(',', '')
    if not NUM_RE.match(s):
        return []
    x = float(s)

    if abs(x) < 10:
        deltas = (-0.8, -0.4, 0.4, 0.8)
    elif abs(x) < 100:
        deltas = (-3, -1, 1, 3)
    elif abs(x) < 1000:
        deltas = (-20, -8, 8, 20)
    else:
        deltas = (-80, -30, 30, 80)

    decimals = 0
    if '.' in s:
        decimals = len(s.split('.')[-1])

    out = []
    for d in deltas:
        v = max(0.0, x + d)
        out.append(fmt_num(v, decimals))
    return out


def token_set(s: str) -> set[str]:
    s = re.sub(r'[^0-9A-Za-z가-힣%:-]+', ' ', s)
    return {t for t in s.lower().split() if len(t) >= 2}


def build_distractors(item: dict, cat_pool: dict[str, list[str]]) -> list[str]:
    ans = (item.get('answer') or [''])[0]
    cands: list[str] = []

    # 1) type-consistent distractors first
    if ans in YN_SET:
        cands.extend(YN_DISTRACTORS.get(ans, []))
    else:
        cands.extend(distractors_for_time(ans))
        cands.extend(distractors_for_percent(ans))
        cands.extend(distractors_for_number(ans))

    # similar options from same category by token overlap
    ans_tokens = token_set(ans)
    same_cat = [x for x in cat_pool.get(item['category'], []) if x != ans]
    # keep type consistency where possible
    if ans in YN_SET:
        same_cat = [x for x in same_cat if x in YN_SET]
    elif TIME_RE.match(ans):
        same_cat = [x for x in same_cat if TIME_RE.match(x)]
    elif PCT_RE.match(ans):
        same_cat = [x for x in same_cat if PCT_RE.match(x)]
    elif NUM_RE.match(ans.replace(',', '')):
        same_cat = [x for x in same_cat if NUM_RE.match(x.replace(',', ''))]
    scored = []
    for x in same_cat:
        t = token_set(x)
        score = len(ans_tokens & t)
        scored.append((score, x))
    scored.sort(key=lambda z: (-z[0], z[1]))
    cands.extend([x for _, x in scored[:20]])

    # keep unique and non-trivial
    out: list[str] = []
    seen = {ans}
    for c in cands:
        c = str(c).strip()
        if not c or c in seen:
            continue
        seen.add(c)
        out.append(c)

    return out


def main() -> None:
    qa = load_qa()

    # category pool from all acceptable answers (not just first)
    cat_pool: dict[str, list[str]] = {}
    for q in qa:
        cat = q['category']
        for a in q.get('answer', []):
            if a:
                cat_pool.setdefault(cat, []).append(str(a))

    letters = ['A', 'B', 'C', 'D']
    rebuilt = []

    for q in qa:
        ans_list = q.get('answer', [])
        if not ans_list:
            rebuilt.append(q)
            continue

        correct = str(ans_list[0])
        distractors = build_distractors(q, cat_pool)

        # fallback when not enough hard distractors
        if len(distractors) < 3:
            fallback = [x for x in cat_pool.get(q['category'], []) if x != correct]
            for x in fallback:
                if x not in distractors and x != correct:
                    distractors.append(x)
                if len(distractors) >= 3:
                    break

        distractors = distractors[:3]
        while len(distractors) < 3:
            distractors.append('N/A')

        opts = distractors + [correct]
        rnd = random.Random(int(q['id'].split('-')[1]) * 17)
        rnd.shuffle(opts)
        choices = {letters[i]: opts[i] for i in range(4)}
        correct_choice = next(k for k, v in choices.items() if v == correct)

        nq = dict(q)
        nq['choices'] = choices
        nq['correct_choice'] = correct_choice
        rebuilt.append(nq)

    header = '"""\n초대형 QA 평가 데이터셋 (객관식, 하드 디스트랙터)\n\n- 채점 방식: 객관식 정답 문자(A/B/C/D) 매칭\n- 오답 선택지: 정답 근접값/유사값 중심으로 강화\n"""\n\nQA_DATASET = '
    QA_PATH.write_text(header + json.dumps(rebuilt, ensure_ascii=False, indent=4) + '\n', encoding='utf-8')
    print('rebuilt', len(rebuilt))


if __name__ == '__main__':
    main()
