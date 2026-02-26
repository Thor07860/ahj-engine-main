from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.state import StateCreate, StateUpdate, StateOut
from app.services.state_service import StateService

class StateAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = StateService()

        self.router.post("/create", response_model=StateOut)(self.create)
        self.router.get("/{state_id}", response_model=StateOut)(self.get)
        self.router.get("/", response_model=list[StateOut])(self.get_all)
        self.router.put("/{state_id}", response_model=StateOut)(self.update)
        self.router.delete("/{state_id}")(self.delete)

    def create(self, data: StateCreate, db: Session = Depends(get_db)):
        return self.service.create(db, data)

    def get(self, state_id: int, db: Session = Depends(get_db)):
        return self.service.get(db, state_id)

    def get_all(self, db: Session = Depends(get_db)):
        return self.service.get_all(db)

    def update(self, state_id: int, data: StateUpdate, db: Session = Depends(get_db)):
        return self.service.update(db, state_id, data)

    def delete(self, state_id: int, db: Session = Depends(get_db)):
        return self.service.delete(db, state_id)