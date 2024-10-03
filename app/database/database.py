# database/database.py
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_url():
    # Obter as configurações do banco de dados a partir das variáveis de ambiente
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    # Codificar a senha para lidar com caracteres especiais
    db_password_encoded = quote_plus(db_password)

    # Construir a URL de conexão com a senha codificada
    return f"postgresql://{db_user}:{db_password_encoded}@{db_host}:{db_port}/{db_name}"


db_url = get_db_url()
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
