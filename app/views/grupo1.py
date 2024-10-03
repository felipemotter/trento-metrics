# views/grupo1.py
import streamlit as st
from database.external import ExternalSessionLocal


def view_viz1():
    st.write("Visualização 1 do Grupo 1")
    session = ExternalSessionLocal()
    # Exemplo de consulta ao banco de dados externo
    result = session.execute("SELECT * FROM tabela_exemplo LIMIT 10")
    data = result.fetchall()
    st.write(data)
    session.close()


def view_viz2():
    st.write("Visualização 2 do Grupo 1")
    st.bar_chart([5, 4, 3, 2, 1])
