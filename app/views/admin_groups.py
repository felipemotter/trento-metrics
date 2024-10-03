# views/admin_groups.py
import streamlit as st
from sqlalchemy.exc import IntegrityError
from database.database import SessionLocal
from database.models import Group

def admin_manage_groups():
    st.header("Gerenciamento de Grupos")

    # Formulário para criar um novo grupo
    with st.form("create_group_form"):
        group_name = st.text_input("Nome do Novo Grupo")
        submit_create = st.form_submit_button("Criar Grupo")

    if submit_create:
        if not group_name.strip():
            st.error("O nome do grupo não pode estar vazio.")
        else:
            session = SessionLocal()
            new_group = Group(name=group_name.strip())
            session.add(new_group)
            try:
                session.commit()
                st.success(f"Grupo '{group_name}' criado com sucesso!")
                st.rerun()  # Recarregar a página para refletir as mudanças
            except IntegrityError:
                session.rollback()
                st.error(f"Grupo '{group_name}' já existe.")
            finally:
                session.close()

    st.subheader("Lista de Grupos")

    session = SessionLocal()
    groups = session.query(Group).all()
    session.close()

    if groups:
        for group in groups:
            with st.expander(f"Grupo: {group.name}"):
                col1, col2 = st.columns([1, 1])

                # Botão para editar o grupo
                with col1:
                    if st.button(f"Editar {group.name}", key=f"edit_{group.id}"):
                        st.session_state['editing_group_id'] = group.id

                # Botão para excluir o grupo
                with col2:
                    if st.button(f"Excluir {group.name}", key=f"delete_{group.id}"):
                        st.session_state['deleting_group_id'] = group.id

        # Se estiver editando um grupo
        if 'editing_group_id' in st.session_state:
            edit_group(st.session_state['editing_group_id'])

        # Se estiver deletando um grupo
        if 'deleting_group_id' in st.session_state:
            delete_group(st.session_state['deleting_group_id'])
    else:
        st.write("Nenhum grupo encontrado.")

def edit_group(group_id):
    session = SessionLocal()
    group = session.query(Group).filter(Group.id == group_id).first()
    if group:
        st.subheader(f"Editar Grupo: {group.name}")

        with st.form(f"edit_group_form_{group.id}"):
            new_name = st.text_input("Novo Nome do Grupo", value=group.name)
            submit_edit = st.form_submit_button("Atualizar Grupo")

        if submit_edit:
            if not new_name.strip():
                st.error("O nome do grupo não pode estar vazio.")
            else:
                group.name = new_name.strip()
                try:
                    session.commit()
                    st.success(f"Grupo atualizado para '{new_name}' com sucesso!")
                    # Remover o estado de edição após a atualização
                    del st.session_state['editing_group_id']
                    st.rerun()
                except IntegrityError:
                    session.rollback()
                    st.error(f"Grupo '{new_name}' já existe.")
                finally:
                    session.close()
    else:
        st.error("Grupo não encontrado.")
        session.close()

def delete_group(group_id):
    session = SessionLocal()
    group = session.query(Group).filter(Group.id == group_id).first()
    if group:
        st.warning(f"Tem certeza que deseja excluir o grupo '{group.name}'?", icon="⚠️")

        if st.button("Confirmar Exclusão", key=f"confirm_delete_{group.id}"):
            try:
                session.delete(group)
                session.commit()
                st.success(f"Grupo '{group.name}' excluído com sucesso!")
                # Remover o estado de deleção após a exclusão
                del st.session_state['deleting_group_id']
                st.rerun()
            except Exception as e:
                session.rollback()
                st.error(f"Erro ao excluir o grupo: {e}")
            finally:
                session.close()
    else:
        st.error("Grupo não encontrado.")
        session.close()
