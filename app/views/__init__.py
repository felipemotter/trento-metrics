# views/__init__.py
from . import admin_groups, admin_users

group_views = {
    # 'faturamento': {
    #     'Visualização 1 do Grupo 1': grupo1.view_grupo1_viz1,
    #     'Visualização 2 do Grupo 1': grupo1.view_grupo1_viz2,
    # },
    'admin': {
        'Gerenciar Grupos': admin_groups.admin_manage_groups,
        'Gerenciar Usuários': admin_users.admin_manage_users,
    },
    # Adicione outros grupos conforme necessário
}

def load_views(user):
    import streamlit as st
    st.set_page_config(
        page_title="Trento Metrics",
        layout="wide",  # Define o layout para ocupar toda a largura da tela
        # initial_sidebar_state="expanded",  # Opcional: define o estado inicial da barra lateral
    )
    user_groups = [group.name for group in user.groups]
    available_views = {}

    for group_name in user_groups:
        if group_name in group_views:
            available_views[group_name] = group_views[group_name]

    if available_views:
        tab_names = []
        tab_contents = []

        for group_name, views in available_views.items():
            for view_name, view_func in views.items():
                tab_names.append(f'{view_name}')
                tab_contents.append(view_func)

        tabs = st.tabs(tab_names)

        for tab, view_func in zip(tabs, tab_contents):
            with tab:
                view_func()
    else:
        st.write("Nenhuma visualização disponível.")
