# utils/auth.py
import bcrypt
import streamlit as st
from database.database import SessionLocal
from database.models import User
from sqlalchemy.orm import joinedload


def authenticate_user():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        session = SessionLocal()
        user = (
            session.query(User)
            .options(joinedload(User.groups))
            .filter_by(username=username)
            .first()
        )
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            session.close()
            st.session_state["user"] = user
            st.success(f"Bem-vindo, {user.name}!")
            st.rerun()
        else:
            session.close()
            st.error("Usuário ou senha incorretos")
