# 결과 화면
import plotly.graph_objects as go
import streamlit as st

from utils.loader import load_types
from utils.scoring import AXES, DOMINANT_LEFT, DOMINANT_RIGHT


def _radar(axis_percent, types_data):
    labels = [types_data["axes"][a]["name"] for a in AXES]
    values = [axis_percent[a] for a in AXES]
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            name="당신",
            line=dict(color="#6C63FF", width=2),
            fillcolor="rgba(108, 99, 255, 0.25)",
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
            angularaxis=dict(tickfont=dict(size=13)),
        ),
        showlegend=False,
        height=380,
        margin=dict(l=30, r=30, t=20, b=20),
    )
    return fig


def _axis_bar(axis_key, percent, types_data):
    left = DOMINANT_LEFT[axis_key]
    right = DOMINANT_RIGHT[axis_key]
    ax = types_data["axes"][axis_key]
    left_meta = ax[left]
    right_meta = ax[right]

    left_percent = percent
    right_percent = 100 - percent
    left_dominant = left_percent >= 50

    left_weight = "700" if left_dominant else "400"
    right_weight = "400" if left_dominant else "700"

    col_l, col_c, col_r = st.columns([3, 4, 3])
    with col_l:
        st.markdown(
            f"<div style='font-weight:{left_weight}'>{left_meta['label']}</div>",
            unsafe_allow_html=True,
        )
        st.caption(left_meta["short"])
    with col_c:
        st.progress(percent / 100)
        st.markdown(
            f"""
            <div style='display:flex; justify-content:space-between; font-size:0.85rem; margin-top:4px;'>
              <span style='font-weight:{left_weight}'>{left_percent:.0f}%</span>
              <span style='font-weight:{right_weight}'>{right_percent:.0f}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_r:
        st.markdown(
            f"<div style='text-align:right; font-weight:{right_weight}'>{right_meta['label']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='text-align:right; color:gray; font-size:0.85rem'>{right_meta['short']}</div>",
            unsafe_allow_html=True,
        )


def render():
    result = st.session_state.get("quiz_result")
    if not result:
        st.warning("아직 결과가 없어요. 테스트를 먼저 진행해주세요.")
        if st.button("테스트 시작"):
            st.session_state["page"] = "quiz"
            st.rerun()
        return

    types_data = load_types()
    code = result["code"]
    type_info = types_data["types"][code]

    st.markdown(f"## {type_info['name']}")
    st.markdown(f"**유형 코드: `{code}`**")
    st.write(type_info["summary"])

    st.divider()

    st.markdown("#### 관계 스타일 그래프")
    st.plotly_chart(_radar(result["axis_percent"], types_data), use_container_width=True)

    st.markdown("#### 축별 기울기")
    st.write("")
    for axis in AXES:
        _axis_bar(axis, result["axis_percent"][axis], types_data)
        st.write("")

    st.divider()

    st.markdown("#### 당신에 대한 해설")
    st.write(type_info["description"])

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### 당신과 잘 맞는 관계")
        st.write(type_info["good_fit"])
    with col_b:
        st.markdown("##### 조심하면 좋은 점")
        st.write(type_info["watch_out"])

    st.divider()
    immersion = result["immersion"]
    st.markdown("#### 관계 몰입도")
    st.progress(immersion / 4)
    immersion_comments = {
        0: "관계에 들이는 에너지가 매우 낮은 상태예요. 지금의 고요함을 즐기되, 최소한의 연결은 남겨두세요.",
        1: "관계보다는 나만의 세계에 더 무게중심이 가 있어요.",
        2: "관계와 고독 사이에서 균형을 잡고 있는 상태예요.",
        3: "타인과의 연결에 비교적 깊이 몰입하는 편이에요.",
        4: "관계에 깊이 몰입하며 감정 에너지를 많이 쓰는 타입이에요.",
    }
    st.caption(f"{immersion} / 4 - {immersion_comments[immersion]}")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("다시 테스트하기", use_container_width=True):
            for key in ("quiz_idx", "quiz_answers", "quiz_result"):
                st.session_state.pop(key, None)
            st.session_state["page"] = "quiz"
            st.rerun()
    with col2:
        if st.button("처음 화면으로", use_container_width=True):
            st.session_state["page"] = "intro"
            st.rerun()
