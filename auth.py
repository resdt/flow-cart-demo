import hashlib
import time
import streamlit as st

import utils.data_processing as data_proc


def display() -> None:
    st.title("FlowCart")
    with st.form("login_form"):
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if st.form_submit_button("Войти"):
            st.session_state.user_type = "administrator"
            st.rerun()
            json = {"username": username, "hashed_password": hashed_password}
            data = data_proc.load_api_data(url="login", json=json)

            if not data["success"]:
                st.error("Неправильный логин или пароль")
                st.stop()

            st.session_state.user_type = data["user_type"]
            st.toast("Авторизация прошла успешно")
            time.sleep(1)
            st.rerun()


display()
