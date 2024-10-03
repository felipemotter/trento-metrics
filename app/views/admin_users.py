# views/admin_users.py
import streamlit as st
from sqlalchemy.exc import IntegrityError
from database.database import SessionLocal
from database.models import User, Group
import bcrypt

def admin_manage_users():
    st.header("Gerenciamento de Usuários")

    # Formulário para criar um novo usuário
    with st.form("create_user_form"):
        name = st.text_input("Nome Completo")
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")
        selected_groups = st.multiselect("Grupos", options=[group.name for group in get_all_groups()])
        submit_create = st.form_submit_button("Criar Usuário")

    if submit_create:
        if not all([name.strip(), username.strip(), password]):
            st.error("Todos os campos são obrigatórios.")
        elif not selected_groups:
            st.error("Selecione pelo menos um grupo para o usuário.")
        else:
            session = SessionLocal()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                name=name.strip(),
                username=username.strip(),
                password_hash=password_hash
            )
            try:
                groups = session.query(Group).filter(Group.name.in_(selected_groups)).all()
                new_user.groups.extend(groups)
                session.add(new_user)
                session.commit()
                st.success(f"Usuário '{username}' criado com sucesso!")
                st.rerun()  # Recarregar a página para refletir as mudanças
            except IntegrityError:
                session.rollback()
                st.error(f"Usuário '{username}' já existe.")
            finally:
                session.close()

    st.subheader("Lista de Usuários")

    session = SessionLocal()
    users = session.query(User).all()
    session.close()

    if users:
        for user in users:
            with st.expander(f"Usuário: {user.username}"):
                col1, col2 = st.columns([1, 1])

                # Botão para editar o usuário
                with col1:
                    if st.button(f"Editar {user.username}", key=f"edit_user_{user.id}"):
                        st.session_state['editing_user_id'] = user.id

                # Botão para excluir o usuário
                with col2:
                    if st.button(f"Excluir {user.username}", key=f"delete_user_{user.id}"):
                        st.session_state['deleting_user_id'] = user.id

        # Se estiver editando um usuário
        if 'editing_user_id' in st.session_state:
            edit_user(st.session_state['editing_user_id'])

        # Se estiver deletando um usuário
        if 'deleting_user_id' in st.session_state:
            delete_user(st.session_state['deleting_user_id'])
    else:
        st.write("Nenhum usuário encontrado.")

def edit_user(user_id):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        st.subheader(f"Editar Usuário: {user.username}")

        with st.form(f"edit_user_form_{user.id}"):
            name = st.text_input("Nome Completo", value=user.name)
            password = st.text_input("Nova Senha (deixe em branco para manter a atual)", type="password")
            selected_groups = st.multiselect("Grupos", options=[group.name for group in get_all_groups()], default=[group.name for group in user.groups])
            submit_edit = st.form_submit_button("Atualizar Usuário")

        if submit_edit:
            if not name.strip():
                st.error("O nome completo não pode estar vazio.")
            elif not selected_groups:
                st.error("Selecione pelo menos um grupo para o usuário.")
            else:
                user.name = name.strip()
                if password:
                    user.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                try:
                    groups = session.query(Group).filter(Group.name.in_(selected_groups)).all()
                    user.groups = groups  # Atualizar os grupos do usuário
                    session.commit()
                    st.success(f"Usuário '{user.username}' atualizado com sucesso!")
                    # Remover o estado de edição após a atualização
                    del st.session_state['editing_user_id']
                    st.rerun()
                except IntegrityError:
                    session.rollback()
                    st.error("Erro ao atualizar o usuário. Verifique se o nome de usuário não está duplicado.")
                finally:
                    session.close()
    else:
        st.error("Usuário não encontrado.")
        session.close()

def delete_user(user_id):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        st.warning(f"Tem certeza que deseja excluir o usuário '{user.username}'?", icon="⚠️")

        if st.button("Confirmar Exclusão", key=f"confirm_delete_user_{user.id}"):
            try:
                session.delete(user)
                session.commit()
                st.success(f"Usuário '{user.username}' excluído com sucesso!")
                # Remover o estado de deleção após a exclusão
                del st.session_state['deleting_user_id']
                st.rerun()
            except Exception as e:
                session.rollback()
                st.error(f"Erro ao excluir o usuário: {e}")
            finally:
                session.close()
    else:
        st.error("Usuário não encontrado.")
        session.close()

def get_all_groups():
    session = SessionLocal()
    groups = session.query(Group).all()
    session.close()
    return groups
