from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.combination_mapper_service import CombinationMapperService
from app.schemas.combination_mapper import (
	CombinationMapperCreate,
	CombinationMapperUpdate,
	CombinationMapperOut,
)


class CombinationMapperAPI:
	def __init__(self):
		self.router = APIRouter()
		self.service = CombinationMapperService()

		self.router.post("/create", response_model=CombinationMapperOut)(self.create)
		self.router.get("/{id}", response_model=CombinationMapperOut)(self.get)
		self.router.get("/", response_model=list[CombinationMapperOut])(self.get_all)
		self.router.put("/{id}", response_model=CombinationMapperOut)(self.update)
		self.router.delete("/{id}")(self.delete)

	def create(self, data: CombinationMapperCreate, db: Session = Depends(get_db)):
		return self.service.create(db, data)

	def get(self, id: int, db: Session = Depends(get_db)):
		return self.service.get(db, id)

	def get_all(self, db: Session = Depends(get_db)):
		return self.service.get_all(db)

	def update(self, id: int, data: CombinationMapperUpdate, db: Session = Depends(get_db)):
		return self.service.update(db, id, data)

	def delete(self, id: int, db: Session = Depends(get_db)):
		return self.service.delete(db, id)

