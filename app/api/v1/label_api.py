from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.label_service import LabelService
from app.schemas.label import LabelCreate, LabelUpdate, LabelOut


class LabelAPI:
	def __init__(self):
		self.router = APIRouter()
		self.service = LabelService()

		self.router.post("/create", response_model=LabelOut)(self.create)
		self.router.get("/{id}", response_model=LabelOut)(self.get)
		self.router.get("/", response_model=list[LabelOut])(self.get_all)
		self.router.put("/{id}", response_model=LabelOut)(self.update)
		self.router.delete("/{id}")(self.delete)

	def create(self, data: LabelCreate, db: Session = Depends(get_db)):
		return self.service.create(db, data)

	def get(self, id: int, db: Session = Depends(get_db)):
		return self.service.get(db, id)

	def get_all(self, db: Session = Depends(get_db)):
		return self.service.get_all(db)

	def update(self, id: int, data: LabelUpdate, db: Session = Depends(get_db)):
		return self.service.update(db, id, data)

	def delete(self, id: int, db: Session = Depends(get_db)):
		return self.service.delete(db, id)

