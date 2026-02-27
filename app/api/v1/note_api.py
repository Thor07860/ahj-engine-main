from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.note_service import NoteService
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut


class NoteAPI:
	def __init__(self):
		self.router = APIRouter()
		self.service = NoteService()

		self.router.post("/create", response_model=NoteOut)(self.create)
		self.router.get("/{id}", response_model=NoteOut)(self.get)
		self.router.get("/", response_model=list[NoteOut])(self.get_all)
		self.router.put("/{id}", response_model=NoteOut)(self.update)
		self.router.delete("/{id}")(self.delete)

	def create(self, data: NoteCreate, db: Session = Depends(get_db)):
		return self.service.create(db, data)

	def get(self, id: int, db: Session = Depends(get_db)):
		return self.service.get(db, id)

	def get_all(self, db: Session = Depends(get_db)):
		return self.service.get_all(db)

	def update(self, id: int, data: NoteUpdate, db: Session = Depends(get_db)):
		return self.service.update(db, id, data)

	def delete(self, id: int, db: Session = Depends(get_db)):
		return self.service.delete(db, id)

