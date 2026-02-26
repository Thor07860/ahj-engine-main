from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.code_service import CodeService
from app.schemas.code import CodeCreate, CodeUpdate, CodeOut

class CodeAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = CodeService()

        self.router.post("/create", response_model=CodeOut)(self.create)
        self.router.get("/{id}", response_model=CodeOut)(self.get)
        self.router.get("/", response_model=list[CodeOut])(self.get_all)
        self.router.put("/{id}", response_model=CodeOut)(self.update)
        self.router.delete("/{id}")(self.delete)

    def create(self, data: CodeCreate, db: Session = Depends(get_db)):
        return self.service.create(db, data)

    def get(self, id: int, db: Session = Depends(get_db)):
        return self.service.get(db, id)

    def get_all(self, db: Session = Depends(get_db)):
        return self.service.get_all(db)

    def update(self, id: int, data: CodeUpdate, db: Session = Depends(get_db)):
        return self.service.update(db, id, data)

    def delete(self, id: int, db: Session = Depends(get_db)):
        return self.service.delete(db, id)