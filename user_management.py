import hashlib
import requests
import pandas as pd
import streamlit as st

import envars
import utils.data_processing as data_proc


def load_data():
    data = data_proc.load_api_data(url="users")
    df_users = pd.DataFrame(data)
    df_users["phone"] = df_users["phone"].astype(str)
    return df_users


def add_user():
    st.write("Введите данные сотрудника")
    st.caption("Обратите внимание, что все поля обязательны к заполнению")
    col1, col2, col3 = st.columns(3)
    with col1:
        middle_name = st.text_input("Фамилия").strip().capitalize()
    with col2:
        first_name = st.text_input("Имя").strip().capitalize()
    with col3:
        last_name = st.text_input("Отчество").strip().capitalize()

    col1, col2 = st.columns(2)
    with col1:
        valid_username = False
        username = st.text_input("Логин").strip().lower()
        if username:
            try:
                response = requests.post(f"{envars.API_BASE_URL}users/check_username?username={username}")
                response.raise_for_status()
                valid_username = True
            except Exception:
                st.error("Данный логин уже используется")
    with col2:
        password = st.text_input("Пароль", type="password")

    user_type = st.selectbox("Тип пользователя",
                             options=sorted(["administrator", "employee"]),
                             index=None,
                             placeholder="Выберите из списка")
    phone = st.text_input("Контактный телефон")
    email = st.text_input("Email")

    confirm = st.button("Добавить", use_container_width=True)
    if confirm:
        if all((middle_name,
                first_name,
                last_name,
                username,
                valid_username,
                user_type,
                password,
                phone,
                email)):
            fio = " ".join((middle_name, first_name, last_name))
            try:
                response = requests.post(f"{envars.API_BASE_URL}users/add",
                                         json={"fio": fio,
                                               "username": username,
                                               "hashed_password": hashlib.sha256(password.encode()).hexdigest(),
                                               "user_type": user_type,
                                               "phone": phone,
                                               "email": email})
                response.raise_for_status()
                st.success("Пользователь успешно добавлен")
                st.rerun()
            except Exception:
                st.error("Ошибка добавления пользователя")
                st.stop()
        else:
            st.error("Не все поля заполнены")


def delete_users():
    df_users = load_data()
    options = sorted(df_users["fio"] + " | " + df_users["email"])
    choice = st.multiselect("", placeholder="Выберите пользователей для удаления", options=options)
    emails = [metadata.split(" | ")[1] for metadata in choice]
    usernames = df_users[df_users["email"].isin(emails)]["username"].to_list()
    confirm = st.button("Удалить", type="primary", use_container_width=True)
    if confirm and usernames:
        try:
            json = usernames
            response = requests.post(f"{envars.API_BASE_URL}users/delete", json=json)
            response.raise_for_status()
            st.success("Выбранные пользователи успешно удалены")
            st.rerun()
        except Exception:
            st.error("Ошибка удаления пользователей")
            st.stop()


@st.dialog("Что Вы хотите сделать?")
def edit_users():
    with st.expander("Добавить пользователей"):
        add_user()
    with st.expander("Удалить пользователей"):
        delete_users()


def display():
    st.title("Управление пользователями")
    st.header("Текущие сотрудники")
    df_users = load_data()
    df_users = st.session_state.src_dfs["df_users"].drop(columns="hashed_password")
    if st.button("Редактировать"):
        edit_users()


display()
