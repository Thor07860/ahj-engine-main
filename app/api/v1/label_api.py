<<<<<<< HEAD
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.label_service import LabelService
from app.schemas.label import LabelCreate, LabelUpdate, LabelOut
from app.models.label import Label


class LabelAPI:
	def __init__(self):
		self.router = APIRouter()
		self.service = LabelService()

		self.router.post("/create", response_model=LabelOut)(self.create)
		self.router.get("/{id}", response_model=LabelOut)(self.get)
		self.router.get("/", response_model=list[LabelOut])(self.get_all)
		self.router.put("/{id}", response_model=LabelOut)(self.update)
		self.router.delete("/{id}")(self.delete)
		self.router.get("/{label_id}/details")(self.get_label_details)
		self.router.get("/by-upc/{upc_code}/details")(self.get_label_by_upc)

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

	def get_label_details(self, label_id: int, db: Session = Depends(get_db)):
		"""Get label details for form auto-population."""
		label = self.service.get(db, label_id)
		if not label:
			return {"error": "Label not found"}
		return {
			"id": label.id,
			"upc_code": label.upc_code,
			"name": label.name,
			"label_number": label.label_number,
			"label_name": label.label_name,
			"length": label.length,
			"width": label.width,
			"description": label.description,
			"background_color": label.background_color,
			"text_color": label.text_color,
			"image_url": label.image_url,
			"field_type": label.field_type,
			"is_active": label.is_active,
		}

	def get_label_by_upc(self, upc_code: str, db: Session = Depends(get_db)):
		"""Get label by UPC code."""
		label = db.query(Label).filter_by(upc_code=upc_code).first()
		if not label:
			return {"error": "Label not found"}
		return {
			"id": label.id,
			"upc_code": label.upc_code,
			"name": label.name,
			"label_number": label.label_number,
			"label_name": label.label_name,
			"length": label.length,
			"width": label.width,
			"description": label.description,
			"background_color": label.background_color,
			"text_color": label.text_color,
			"image_url": label.image_url,
			"field_type": label.field_type,
			"is_active": label.is_active,
		}
=======
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

>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
