# app/main.py

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from app.core.error_handler import http_exception_handler, unhandled_exception_handler
from app.core.database import init_db
from fastapi.staticfiles import StaticFiles

# Routers
from app.api.v1.ahj_api import AHJAPI
from app.api.v1.utility_api import UtilityAPI
from app.api.v1.code_type_api import CodeTypeAPI
from app.api.v1.code_api import CodeAPI
from app.api.v1.ahj_engine_api import AHJEngineAPI
from app.api.v1.state_lookup_api import StateLookupAPI
from app.api.v1.auth_api import AuthAPI

# SQLAdmin
from app.admin.admin import setup_admin
MAIN_APP_VERSION = "v1"
<<<<<<< HEAD

=======
API_VERSION = "1.0.0"
>>>>>>> 97a533c (changes)
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


# -----------------------------------
# Admin Panel (SQLAdmin)
# -----------------------------------
setup_admin(app)


# -----------------------------------
# Root Route (Optional)
# -----------------------------------
@app.get("/")
def root():
    return {"message": "AHJ Engine Running Successfully 🚀"}