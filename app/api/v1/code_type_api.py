from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.code_type_service import CodeTypeService
from app.schemas.code_type import CodeTypeCreate, CodeTypeUpdate, CodeTypeOut

class CodeTypeAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = CodeTypeService()

        self.router.post("/create", response_model=CodeTypeOut)(self.create)
        self.router.get("/{id}", response_model=CodeTypeOut)(self.get)
        self.router.get("/", response_model=list[CodeTypeOut])(self.get_all)
        self.router.put("/{id}", response_model=CodeTypeOut)(self.update)
        self.router.delete("/{id}")(self.delete)

    def create(self, data: CodeTypeCreate, db: Session = Depends(get_db)):
        return self.service.create(db, data)

    def get(self, id: int, db: Session = Depends(get_db)):
        return self.service.get(db, id)

    def get_all(self, db: Session = Depends(get_db)):
        return self.service.get_all(db)

    def update(self, id: int, data: CodeTypeUpdate, db: Session = Depends(get_db)):
        return self.service.update(db, id, data)

    def delete(self, id: int, db: Session = Depends(get_db)):
        return self.service.delete(db, id)