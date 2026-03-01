from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.get_ahj_details import AHJDetailRequest, AHJDetailResponse
from app.services.ahj_engine_service import AHJEngineService

class AHJEngineAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = AHJEngineService()

        self.router.post("/get-ahj-details", response_model=AHJDetailResponse)(self.get_details)

    def get_details(self, request: AHJDetailRequest, db: Session = Depends(get_db)):
        result = self.service.process(
            db,
            request.ahj_name,
            request.electrical_code,
            request.structural_code,
            request.fire_code
        )
        return result