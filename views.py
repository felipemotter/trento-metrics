import streamlit as st

def view_grupo1_viz1():
    st.write("Visualização 1 do Grupo 1")
    st.line_chart([1, 2, 3, 4, 5])

def view_grupo1_viz2():
    st.write("Visualização 2 do Grupo 1")
    st.bar_chart([5, 4, 3, 2, 1])

def view_grupo2_viz1():
    st.write("Visualização 1 do Grupo 2")
    st.area_chart([3, 1, 2, 5, 4])

def view_grupo3_viz1():
    st.write("Visualização 1 do Grupo 3")
    st.map()
