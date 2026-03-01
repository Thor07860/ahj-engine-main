from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.utility_service import UtilityService
from app.schemas.utility import UtilityCreate, UtilityUpdate, UtilityOut

class UtilityAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = UtilityService()

        self.router.post("/create", response_model=UtilityOut)(self.create)
        self.router.get("/{utility_id}", response_model=UtilityOut)(self.get)
        self.router.get("/", response_model=list[UtilityOut])(self.get_all)
        self.router.put("/{utility_id}", response_model=UtilityOut)(self.update)
        self.router.delete("/{utility_id}")(self.delete)

    def create(self, data: UtilityCreate, db: Session = Depends(get_db)):
        return self.service.create(db, data)

    def get(self, utility_id: int, db: Session = Depends(get_db)):
        return self.service.get(db, utility_id)

    def get_all(self, db: Session = Depends(get_db)):
        return self.service.get_all(db)

    def update(self, utility_id: int, data: UtilityUpdate, db: Session = Depends(get_db)):
        return self.service.update(db, utility_id, data)

    def delete(self, utility_id: int, db: Session = Depends(get_db)):
        return self.service.delete(db, utility_id)