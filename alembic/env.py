from logging.config import fileConfig
import os

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

from app.core.database import Base

# Import all models to register metadata for autogenerate
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

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
EXCLUDED_TABLES = {"admin_users"}


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in EXCLUDED_TABLES:
        return False
    return True


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise Exception("DATABASE_URL is not set")
    return database_url


def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(get_database_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
