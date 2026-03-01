<<<<<<< HEAD
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.formula_service import FormulaService
from app.schemas.formula import FormulaCreate, FormulaUpdate, FormulaOut


class FormulaAPI:
	def __init__(self):
		self.router = APIRouter()
		self.service = FormulaService()

		self.router.post("/create", response_model=FormulaOut)(self.create)
		self.router.get("/{id}", response_model=FormulaOut)(self.get)
		self.router.get("/", response_model=list[FormulaOut])(self.get_all)
		self.router.put("/{id}", response_model=FormulaOut)(self.update)
		self.router.delete("/{id}")(self.delete)

	def create(self, data: FormulaCreate, db: Session = Depends(get_db)):
		return self.service.create(db, data)

	def get(self, id: int, db: Session = Depends(get_db)):
		return self.service.get(db, id)

	def get_all(self, db: Session = Depends(get_db)):
		return self.service.get_all(db)

	def update(self, id: int, data: FormulaUpdate, db: Session = Depends(get_db)):
		return self.service.update(db, id, data)

	def delete(self, id: int, db: Session = Depends(get_db)):
		return self.service.delete(db, id)

=======
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.formula_service import FormulaService
from app.schemas.formula import FormulaCreate, FormulaUpdate, FormulaOut


class FormulaAPI:
	def __init__(self):
		self.router = APIRouter()
		self.service = FormulaService()

		self.router.post("/create", response_model=FormulaOut)(self.create)
		self.router.get("/{id}", response_model=FormulaOut)(self.get)
		self.router.get("/", response_model=list[FormulaOut])(self.get_all)
		self.router.put("/{id}", response_model=FormulaOut)(self.update)
		self.router.delete("/{id}")(self.delete)

	def create(self, data: FormulaCreate, db: Session = Depends(get_db)):
		return self.service.create(db, data)

	def get(self, id: int, db: Session = Depends(get_db)):
		return self.service.get(db, id)

	def get_all(self, db: Session = Depends(get_db)):
		return self.service.get_all(db)

	def update(self, id: int, data: FormulaUpdate, db: Session = Depends(get_db)):
		return self.service.update(db, id, data)

	def delete(self, id: int, db: Session = Depends(get_db)):
		return self.service.delete(db, id)

>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
