from datetime import datetime

import streamlit as st


def create_sidebar():
    current_year = datetime.now().year
    # Gerar uma lista de anos em ordem decrescente
    years = list(range(current_year, 2023, -1))
    if years:
        default_index = 0
        selected_year = st.sidebar.selectbox(
            "Selecione o Ano de Referência", options=years, index=default_index
        )
        st.session_state["selected_year"] = selected_year
    else:
        st.sidebar.write("Nenhum ano disponível.")
        st.session_state["selected_year"] = None
