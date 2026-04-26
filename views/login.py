# 로그인 / 회원가입 화면
import streamlit as st

from utils import auth

_LOGIN_KEYS = ("login_id", "login_pw")
_SIGNUP_KEYS = ("signup_id", "signup_pw")


def _switch_mode(mode):
    if st.session_state.get("auth_mode") == mode:
        return
    drop = _SIGNUP_KEYS if mode == "login" else _LOGIN_KEYS
    for k in drop:
        st.session_state.pop(k, None)
    st.session_state["auth_mode"] = mode


def render():
    st.markdown("### 로그인")
    st.caption("테스트를 시작하려면 로그인하거나 간단히 가입해주세요.")

    mode = st.session_state.setdefault("auth_mode", "login")

    col_login, col_signup = st.columns(2)
    with col_login:
        if st.button(
            "로그인",
            use_container_width=True,
            type="primary" if mode == "login" else "secondary",
            key="tab_login_btn",
        ):
            _switch_mode("login")
            st.rerun()
    with col_signup:
        if st.button(
            "회원가입",
            use_container_width=True,
            type="primary" if mode == "signup" else "secondary",
            key="tab_signup_btn",
        ):
            _switch_mode("signup")
            st.rerun()

    st.write("")

    if mode == "login":
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("아이디", key="login_id")
            password = st.text_input("비밀번호", type="password", key="login_pw")
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            if auth.verify(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["nickname"] = auth.get_nickname(username)
                st.session_state["page"] = "intro"
                st.success(f"환영해요, {st.session_state['nickname']}님!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 맞지 않아요.")
    else:
        with st.form("signup_form", clear_on_submit=True):
            new_id = st.text_input("아이디", key="signup_id")
            new_pw = st.text_input("비밀번호 (4자 이상)", type="password", key="signup_pw")
            created = st.form_submit_button("가입하기", use_container_width=True)

        if created:
            ok, msg = auth.register(new_id, new_pw, "")
            if ok:
                st.success(msg)
            else:
                st.error(msg)
