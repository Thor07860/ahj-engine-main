from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

class NoteService:
    def create(self, db: Session, data: NoteCreate):
        obj = Note(**data.dict(exclude_none=True))
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(Note).filter(Note.id == id).first()

    def get_all(self, db: Session):
        return db.query(Note).all()

    def update(self, db: Session, id: int, data: NoteUpdate):
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
        return db.query(Note).filter(Note.code_id == code_id).all()