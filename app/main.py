# app/main.py
import streamlit as st
from utils.auth import authenticate_user
from views import load_views

def main():
    if 'user' not in st.session_state:
        authenticate_user()
    else:
        user = st.session_state['user']
        load_views(user)

if __name__ == '__main__':
    main()
