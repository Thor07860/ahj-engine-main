# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

Base = declarative_base()

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
from app.models.country import Country
from app.models.code_amendment import CodeAmendment
from app.models.applicable_code_category import ApplicableCodeCategory
from app.models.state_code import StateCode
from app.models.ahj_code import AHJCode
from app.models.client import Client
from app.models.preference import Preference
from app.models.equipment import Equipment
from app.models.category import Category
from app.models.note_type import NoteType
from app.models.formula_linker_type import FormulaLinkerType
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    

    Base.metadata.create_all(bind=engine)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()