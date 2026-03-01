from sqlalchemy.orm import Session
from app.models.label import Label
from app.schemas.label import LabelCreate, LabelUpdate

class LabelService:
    def create(self, db: Session, data: LabelCreate):
        payload = data.dict(exclude_none=True)

        display_name = payload.get("name") or payload.get("label_name") or "Unnamed Label"
        payload["name"] = display_name
        payload["label_name"] = payload.get("label_name") or display_name

        code = payload.get("upc_code") or payload.get("label_number")
        if not code:
            code = display_name.upper().replace(" ", "_")
        payload["upc_code"] = payload.get("upc_code") or code
        payload["label_number"] = payload.get("label_number") or code

        obj = Label(**payload)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(Label).filter(Label.id == id).first()

    def get_all(self, db: Session):
        return db.query(Label).all()

    def update(self, db: Session, id: int, data: LabelUpdate):
        obj = self.get(db, id)
        if not obj:
            return None

        payload = data.dict(exclude_none=True)
        if "name" in payload or "label_name" in payload:
            display_name = payload.get("name") or payload.get("label_name")
            payload["name"] = display_name
            payload["label_name"] = payload.get("label_name") or display_name

        if "upc_code" in payload or "label_number" in payload:
            code = payload.get("upc_code") or payload.get("label_number")
            payload["upc_code"] = payload.get("upc_code") or code
            payload["label_number"] = payload.get("label_number") or code

        for key, value in payload.items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return True

    def get_by_ids(self, db: Session, ids: list[int]):
        return db.query(Label).filter(Label.id.in_(ids)).all()