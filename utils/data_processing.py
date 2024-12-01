import requests
import streamlit as st

import envars


def load_api_data(url: str, json: dict = {}):
    with st.spinner("Пожалуйста, подождите... данные обновляются."):
        try:
            response = (requests.post(f"{envars.API_BASE_URL}{url}", json=json) if json
                        else requests.post(f"{envars.API_BASE_URL}{url}"))
            response.raise_for_status()
            data = response.json()
            return data
        except Exception:
            st.error("Ошибка подключения к серверу")
            st.stop()
