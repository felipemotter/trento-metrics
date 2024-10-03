# database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import get_config

config = get_config()
DATABASE_URL = config["database"]["url"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
