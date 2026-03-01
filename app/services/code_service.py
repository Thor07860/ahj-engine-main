from sqlalchemy.orm import Session
from app.models.code import Code
from app.schemas.code import CodeCreate, CodeUpdate

class CodeService:

    def create(self, db: Session, data: CodeCreate):
        payload = data.dict(exclude_none=True)
        canonical_title = payload.get("title") or payload.get("code_name") or "Untitled Code"
        payload["title"] = canonical_title
        payload["code_name"] = payload.get("code_name") or canonical_title
        obj = Code(**payload)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(Code).filter(Code.id == id).first()

    def get_all(self, db: Session):
        return db.query(Code).all()

    def update(self, db: Session, id: int, data: CodeUpdate):
        obj = self.get(db, id)
        if not obj:
            return None
        payload = data.dict(exclude_none=True)
        canonical_title = payload.get("title") or payload.get("code_name")
        if canonical_title:
            payload["title"] = canonical_title
            payload["code_name"] = payload.get("code_name") or canonical_title
        for k, v in payload.items():
            setattr(obj, k, v)
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