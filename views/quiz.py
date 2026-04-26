# 퀴즈 화면
import streamlit as st

from utils.loader import load_questions
from utils.scoring import compute

LIKERT = [
    (1, "전혀 그렇지 않다"),
    (2, "그렇지 않다"),
    (3, "보통이다"),
    (4, "그런 편이다"),
    (5, "매우 그렇다"),
]


def _init_state():
    st.session_state.setdefault("quiz_idx", 0)
    st.session_state.setdefault("quiz_answers", {})


def render():
    _init_state()
    questions = load_questions()
    total = len(questions)
    idx = st.session_state["quiz_idx"]

    st.markdown(f"### 테스트 {idx + 1} / {total}")
    st.progress((idx + 1) / total)

    q = questions[idx]
    st.markdown(f"#### Q{idx + 1}. {q['text']}")

    prev_answer = st.session_state["quiz_answers"].get(q["id"], 3)
    labels = [f"{v}. {label}" for v, label in LIKERT]
    choice = st.radio(
        label="가장 가까운 쪽을 골라주세요.",
        options=labels,
        index=prev_answer - 1,
        key=f"q_{q['id']}",
    )
    selected_value = int(choice.split(".")[0])
    st.session_state["quiz_answers"][q["id"]] = selected_value

    st.write("")
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])

    with col_prev:
        if st.button("← 이전", disabled=idx == 0, use_container_width=True):
            st.session_state["quiz_idx"] = max(0, idx - 1)
            st.rerun()

    with col_next:
        is_last = idx == total - 1
        label = "결과 보기" if is_last else "다음 →"
        if st.button(label, use_container_width=True, type="primary"):
            if is_last:
                result = compute(st.session_state["quiz_answers"], questions)
                st.session_state["quiz_result"] = result
                st.session_state["page"] = "result"
            else:
                st.session_state["quiz_idx"] = idx + 1
            st.rerun()

    with st.sidebar:
        st.markdown("**진행 상황**")
        st.write(f"응답 완료: {len(st.session_state['quiz_answers'])} / {total}")
        if st.button("처음으로", use_container_width=True):
            st.session_state["quiz_idx"] = 0
            st.session_state["quiz_answers"] = {}
            st.session_state["page"] = "intro"
            st.rerun()
