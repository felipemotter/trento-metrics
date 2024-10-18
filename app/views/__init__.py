from . import classic_revenue_report
from .sidebar import create_sidebar

# from . import admin

group_views = {
    "faturamento": {
        "Faturamento Clássico": classic_revenue_report.view_revenue,
    },
    # "admin": {
    #     "Configurações": admin.admin_manage,
    # },
}


def load_views(user):
    import streamlit as st

    st.set_page_config(
        page_title="Trento Metrics",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    create_sidebar()
    user_groups = [group.name for group in user.groups]
    available_views = {}

    for group_name in user_groups:
        if group_name in group_views:
            available_views[group_name] = group_views[group_name]

    if available_views:
        tab_names = []
        tab_contents = []

        for _, views in available_views.items():
            for view_name, view_func in views.items():
                tab_names.append(f"{view_name}")
                tab_contents.append(view_func)

        tabs = st.tabs(tab_names)

        for tab, view_func in zip(tabs, tab_contents):
            with tab:
                view_func()
    else:
        st.write("Nenhuma visualização disponível.")
