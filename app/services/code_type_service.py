from sqlalchemy.orm import Session
from app.models.code_type import CodeType
from app.schemas.code_type import CodeTypeCreate, CodeTypeUpdate

class CodeTypeService:

    def create(self, db: Session, data: CodeTypeCreate):
        payload = data.dict(exclude_none=True)
        canonical_title = payload.get("title") or payload.get("key") or "Untitled Code Type"
        payload["title"] = canonical_title
        payload["key"] = payload.get("key") or canonical_title
        obj = CodeType(**payload)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(CodeType).filter(CodeType.id == id).first()

    def get_all(self, db: Session):
        return db.query(CodeType).all()

    def update(self, db: Session, id: int, data: CodeTypeUpdate):
        obj = self.get(db, id)
        if not obj:
            return None
        payload = data.dict(exclude_none=True)
        canonical_title = payload.get("title") or payload.get("key")
        if canonical_title:
            payload["title"] = canonical_title
            payload["key"] = payload.get("key") or canonical_title
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