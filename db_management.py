import requests
import streamlit as st
import pandas as pd

import envars
import utils.data_processing as data_proc


def display_database():
    tables = ["app_users",
              "goods_availability",
              "markets",
              "products",
              "sales",
              "supply_details",
              "supply_metadata"]
    table_dict = data_proc.load_api_data(url="tables", json=tables)
    table_dict = {key: pd.DataFrame(val) for key, val in table_dict.items()}
    for table_name in tables:
        st.subheader(table_name)
        df = table_dict[table_name].copy()
        df.index += 1
        st.dataframe(df, use_container_width=True)


def backup_database():
    try:
        response = requests.post(f"{envars.API_BASE_URL}backup_database")
        response.raise_for_status()
        st.success("Резервная копия успешно создана")
    except requests.exceptions.ConnectionError:
        st.error("Ошибка подключения к серверу")
        st.stop()
    except Exception:
        st.error("Непредвиденная ошибка")
        st.stop()


def restore_database(filename):
    json = {"filename": filename}
    try:
        response = requests.post(f"{envars.API_BASE_URL}restore_database", json=json)
        response.raise_for_status()
        st.success("База данных успешно восстановлена")
    except requests.exceptions.ConnectionError as connection_error:
        st.error(f"Ошибка подключения к серверу: {connection_error}")
        st.stop()
    except Exception:
        st.error("Непредвиденная ошибка")
        st.stop()


@st.dialog("Резервное копирование и восстановление")
def backup_and_restore():
    if st.button("Создать резервную копию", use_container_width=True):
        backup_database()
    with st.expander("Восстановить базу данных"):
        listdir = data_proc.load_api_data(url="list_backups")
        filename = st.selectbox(label="Выберите файл для восстановления",
                                placeholder="Выберите из списка",
                                options=listdir,
                                index=None)
        if st.button("Восстановить", type="primary", use_container_width=True) and filename:
            with st.spinner("Пожалуйста, подождите... база данных восстанавливается."):
                restore_database(filename)


def display():
    st.title("Состояние базы данных")
    display_database()
    if st.button("Резервное копирование и восстановление"):
        backup_and_restore()


display()
