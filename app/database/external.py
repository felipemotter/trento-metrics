# database/external.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import get_config

config = get_config()
EXTERNAL_DATABASE_URL = config["external_database"]["url"]

external_engine = create_engine(EXTERNAL_DATABASE_URL)
ExternalSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=external_engine
)
