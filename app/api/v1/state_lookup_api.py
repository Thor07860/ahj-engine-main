from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.get_state import StateNameResponse
from app.services.state_lookup_service import StateLookupService

class StateLookupAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = StateLookupService()

        self.router.get("/get-state-name", response_model=StateNameResponse)(self.get_state)

    def get_state(self, abbrev: str, db: Session = Depends(get_db)):
        """
        Example:
        GET /api/v1/state/get-state-name?abbrev=TX
        """
        return self.service.get_state_details(db, abbrev)