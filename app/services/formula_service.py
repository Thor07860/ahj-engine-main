from sqlalchemy.orm import Session
from app.models.formula import Formula
from app.schemas.formula import FormulaCreate, FormulaUpdate

class FormulaService:
    def create(self, db: Session, data: FormulaCreate):
        obj = Formula(**data.dict(exclude_none=True))
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(Formula).filter(Formula.id == id).first()

    def get_all(self, db: Session):
        return db.query(Formula).all()

    def update(self, db: Session, id: int, data: FormulaUpdate):
        obj = self.get(db, id)
        if not obj:
            return None
        for key, value in data.dict(exclude_none=True).items():
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

    def get_by_code(self, db: Session, code_id: int):
        return db.query(Formula).filter(Formula.code_id == code_id).all()