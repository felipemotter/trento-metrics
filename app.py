# app.py
import streamlit as st
from database import SessionLocal
from models import User
import bcrypt
from sqlalchemy.orm import joinedload

from views import (
    view_grupo1_viz1, view_grupo1_viz2,
)

# Mapeamento de grupos para visualizações
group_views = {
    'faturamento': {
        'Visualização 1 do Grupo 1': view_grupo1_viz1,
        'Visualização 2 do Grupo 1': view_grupo1_viz2,
    },
}

def authenticate_user(username, password):
    session = SessionLocal()
    user = session.query(User).options(joinedload(User.groups)).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        session.close()
        return user
    session.close()
    return None

def login():
    st.title('Login')
    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')

    if st.button('Entrar'):
        user = authenticate_user(username, password)
        if user:
            st.session_state['user'] = user
            st.success(f'Bem-vindo, {user.name}!')
            st.rerun()
        else:
            st.error('Usuário ou senha incorretos')

def get_user_groups(user):
    return [group.name for group in user.groups]

def main():
    if 'user' not in st.session_state:
        login()
    else:
        user = st.session_state['user']
        user_groups = get_user_groups(user)

        # Mapeamento de todas as visualizações disponíveis para o usuário
        available_views = {}

        for group_name in user_groups:
            if group_name in group_views:
                available_views[group_name] = group_views[group_name]

        if available_views:
            # Criar uma lista de nomes de abas e suas funções correspondentes
            tab_names = []
            tab_contents = []

            for group_name, views in available_views.items():
                for view_name, view_func in views.items():
                    tab_names.append(f'{view_name}')
                    tab_contents.append(view_func)

            # Criar as abas
            tabs = st.tabs(tab_names)

            # Exibir o conteúdo de cada aba
            for tab, view_func in zip(tabs, tab_contents):
                with tab:
                    view_func()
        else:
            st.write("Nenhuma visualização disponível.")

if __name__ == '__main__':
    main()
