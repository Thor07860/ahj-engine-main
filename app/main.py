# app/main.py

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles

from app.core.error_handler import http_exception_handler, unhandled_exception_handler
from app.core.database import init_db

# Routers
from app.api.v1.ahj_api import AHJAPI
from app.api.v1.utility_api import UtilityAPI
from app.api.v1.code_type_api import CodeTypeAPI
from app.api.v1.code_api import CodeAPI
from app.api.v1.ahj_engine_api import AHJEngineAPI
from app.api.v1.state_lookup_api import StateLookupAPI
from app.api.v1.auth_api import AuthAPI
from app.api.v1.state_api import StateAPI
from app.api.v1.label_api import LabelAPI
from app.api.v1.note_api import NoteAPI
from app.api.v1.formula_api import FormulaAPI
from app.api.v1.combination_mapper_api import CombinationMapperAPI

# SQLAdmin
from app.admin.admin import setup_admin
MAIN_APP_VERSION = "v1"

# -----------------------------------
# Initialize FastAPI App
# -----------------------------------
app = FastAPI(title="AHJ Engine")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup():
    init_db()


# -----------------------------------
# Exception Handlers
# -----------------------------------
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# -----------------------------------
# Register API Routers
# -----------------------------------
app.include_router(AHJAPI().router, prefix="/api/v1/ahj", tags=["AHJ"])
app.include_router(UtilityAPI().router, prefix="/api/v1/utility", tags=["Utility"])
app.include_router(CodeTypeAPI().router, prefix="/api/v1/code-type", tags=["Code Type"])
app.include_router(CodeAPI().router, prefix="/api/v1/code", tags=["Code"])
app.include_router(AHJEngineAPI().router, prefix="/api/v1/ahj-engine", tags=["AHJ Engine"])
app.include_router(StateLookupAPI().router, prefix="/api/v1/state", tags=["State Lookup"])
app.include_router(AuthAPI().router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(StateAPI().router, prefix="/api/v1/states", tags=["States"])
app.include_router(LabelAPI().router, prefix="/api/v1/label", tags=["Label"])
app.include_router(NoteAPI().router, prefix="/api/v1/note", tags=["Note"])
app.include_router(FormulaAPI().router, prefix="/api/v1/formula", tags=["Formula"])
app.include_router(CombinationMapperAPI().router, prefix="/api/v1/combination-mapper", tags=["Combination Mapper"])


# -----------------------------------
# Admin Panel (SQLAdmin)
# -----------------------------------
setup_admin(app)


# -----------------------------------
# Root Route (Optional)
# -----------------------------------
@app.get("/")
def root():
    return {"message": "AHJ Engine Running Successfully"}
