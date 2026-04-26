# 4축 점수 계산과 16유형 매핑
import streamlit as st

AXES = ["CI", "HL", "VR", "GF"]
DOMINANT_LEFT = {"CI": "C", "HL": "H", "VR": "V", "GF": "G"}
DOMINANT_RIGHT = {"CI": "I", "HL": "L", "VR": "R", "GF": "F"}

# 네 글자 중 C/H/V/G의 개수 (관계 몰입도 지표)
IMMERSION_LETTERS = {"C", "H", "V", "G"}


@st.cache_data(show_spinner=False)
def _score_lookup(question_key):
    return {q[0]: {"axis": q[1], "direction": q[2]} for q in question_key}


def compute(answers, questions):
    key = tuple((q["id"], q["axis"], q["direction"]) for q in questions)
    meta = _score_lookup(key)

    axis_scores = {a: [] for a in AXES}
    for qid, value in answers.items():
        info = meta.get(qid)
        if info is None:
            continue
        axis = info["axis"]
        direction = info["direction"]
        signed = (value - 3) if direction == DOMINANT_LEFT[axis] else -(value - 3)
        axis_scores[axis].append(signed)

    axis_percent = {}
    code = ""
    for axis in AXES:
        values = axis_scores[axis]
        total = sum(values)
        max_abs = 2 * len(values) if values else 1
        percent = 50 + (total / max_abs) * 50
        axis_percent[axis] = round(percent, 1)
        code += DOMINANT_LEFT[axis] if total >= 0 else DOMINANT_RIGHT[axis]

    immersion = sum(1 for ch in code if ch in IMMERSION_LETTERS)

    return {
        "code": code,
        "axis_percent": axis_percent,
        "immersion": immersion,
    }
