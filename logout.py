import streamlit as st


def logout() -> None:
    st.session_state.user_type = None
    st.rerun()


logout()
