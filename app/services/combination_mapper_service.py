from sqlalchemy.orm import Session
from app.models.combination_mapper import CombinationMapper
from app.schemas.combination_mapper import CombinationMapperCreate, CombinationMapperUpdate

class CombinationMapperService:
    def create(self, db: Session, data: CombinationMapperCreate):
        obj = CombinationMapper(**data.dict(exclude_none=True))
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(CombinationMapper).filter(CombinationMapper.id == id).first()

    def get_all(self, db: Session):
        return db.query(CombinationMapper).all()

    def update(self, db: Session, id: int, data: CombinationMapperUpdate):
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

    def get_label_ids(self, db: Session, code_id: int):
        mappings = db.query(CombinationMapper).filter(CombinationMapper.code_id == code_id).all()
        return [m.label_id for m in mappings]