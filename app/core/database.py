# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    from app.models.state import State
    from app.models.ahj import AHJ
    from app.models.utility import Utility
    from app.models.code import Code
    from app.models.code_type import CodeType
    from app.models.label import Label
    from app.models.note import Note
    from app.models.formula import Formula
    from app.models.combination_mapper import CombinationMapper
    from app.models.user import User

    Base.metadata.create_all(bind=engine)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()