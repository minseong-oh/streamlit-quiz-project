# 외로움 성향 테스트 메인 엔트리
# 과제 제출자: 2021204018 오민성
import streamlit as st

from views import login, quiz, result

STUDENT_ID = "2021204018"
STUDENT_NAME = "오민성"

st.set_page_config(
    page_title="외로움 성향 테스트",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def _render_header():
    st.markdown(
        f"""
        <div style="padding: 14px 18px; border-radius: 12px;
                    background: linear-gradient(135deg, #EEF0FF, #F9E7FF);
                    border: 1px solid #E2E2F5; margin-bottom: 18px;">
          <div style="font-size: 0.85rem; color: #5A5A7A;">중간고사 대체 과제, 오픈소스소프트웨어실습</div>
          <div style="font-size: 1rem; font-weight: 600; color: #2E2E4F;">
            학번 {STUDENT_ID}, 이름 {STUDENT_NAME}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_sidebar():
    with st.sidebar:
        st.markdown("### 외로움 성향 테스트")
        if st.session_state.get("logged_in"):
            st.success(f"{st.session_state.get('nickname', '게스트')}님 접속 중")
            if st.button("로그아웃", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        else:
            st.info("로그인이 필요합니다.")


def _render_intro():
    st.markdown("## 외로움 성향 테스트")
    st.markdown(
        """
        요즘 당신은 어떤 **거리감**을 원하고 있나요?

        이 테스트는 20개의 문항으로 당신의
        **친밀 욕구, 관계 에너지, 감정 반경, 일상 감각**, 네 가지 축을 살펴보고
        16가지 유형 중 하나로 당신의 현재 관계 스타일을 알려드려요.

        - 소요 시간: 약 3분
        - 정답은 없어요. 지금 이 순간의 감각에 가까운 쪽을 골라주세요.
        """
    )
    st.caption("이 결과는 향후 'AI 친구 챗봇' 개발의 사용자 유형 분포 데이터로 활용될 예정입니다.")
    st.write("")
    if st.button("테스트 시작하기", type="primary", use_container_width=True):
        for key in ("quiz_idx", "quiz_answers", "quiz_result"):
            st.session_state.pop(key, None)
        st.session_state["page"] = "quiz"
        st.rerun()


def main():
    _render_sidebar()

    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("page", "intro")

    if not st.session_state["logged_in"]:
        _render_header()
        login.render()
        return

    page = st.session_state["page"]
    if page == "intro":
        _render_intro()
    elif page == "quiz":
        quiz.render()
    elif page == "result":
        result.render()
    else:
        st.session_state["page"] = "intro"
        st.rerun()


if __name__ == "__main__":
    main()
