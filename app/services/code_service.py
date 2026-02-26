from sqlalchemy.orm import Session
from app.models.code import Code
from app.schemas.code import CodeCreate, CodeUpdate

class CodeService:

    def create(self, db: Session, data: CodeCreate):
        obj = Code(**data.dict())
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
        for k, v in data.dict().items():
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