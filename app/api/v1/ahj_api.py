from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.ahj_service import AHJService
from app.schemas.ahj import AHJCreate, AHJUpdate, AHJOut

class AHJAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = AHJService()

        self.router.post("/create", response_model=AHJOut)(self.create)
        self.router.get("/{ahj_id}", response_model=AHJOut)(self.get)
        self.router.get("/", response_model=list[AHJOut])(self.get_all)
        self.router.put("/{ahj_id}", response_model=AHJOut)(self.update)
        self.router.delete("/{ahj_id}")(self.delete)

    def create(self, data: AHJCreate, db: Session = Depends(get_db)):
        return self.service.create(db, data)

    def get(self, ahj_id: int, db: Session = Depends(get_db)):
        return self.service.get(db, ahj_id)

    def get_all(self, db: Session = Depends(get_db)):
        return self.service.get_all(db)

    def update(self, ahj_id: int, data: AHJUpdate, db: Session = Depends(get_db)):
        return self.service.update(db, ahj_id, data)

    def delete(self, ahj_id: int, db: Session = Depends(get_db)):
        return self.service.delete(db, ahj_id)