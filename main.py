import streamlit as st


def main() -> None:
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    if "src_dfs" not in st.session_state:
        st.session_state.src_dfs = {}

    user_type = st.session_state.user_type
    if user_type is None:
        display_pages = st.navigation([st.Page("auth.py", title="Login")])
    elif user_type == "administrator":
        display_pages = st.navigation([st.Page("home.py", title="Home"), st.Page("logout.py", title="Log out")]
                                      + [st.Page("user_management.py", title="Управление пользователями"), st.Page("db_management.py", title="Состояние базы данных")])
    else:
        display_pages = st.navigation([st.Page("home.py", title="Home"), st.Page("logout.py", title="Log out")])

    display_pages.run()


if __name__ == "__main__":
    main()
