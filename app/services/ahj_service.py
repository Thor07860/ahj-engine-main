from sqlalchemy.orm import Session
from app.models.ahj import AHJ
from app.schemas.ahj import AHJCreate, AHJUpdate

class AHJService:

    def create(self, db: Session, data: AHJCreate):
        payload = data.dict(exclude_none=True)
        canonical_name = payload.get("name") or payload.get("ahj_name") or "Unknown AHJ"
        payload["name"] = canonical_name
        payload["ahj_name"] = payload.get("ahj_name") or canonical_name
        ahj = AHJ(**payload)
        db.add(ahj)
        db.commit()
        db.refresh(ahj)
        return ahj

    def get(self, db: Session, ahj_id: int):
        return db.query(AHJ).filter(AHJ.id == ahj_id).first()

    def get_all(self, db: Session):
        return db.query(AHJ).all()

    def update(self, db: Session, ahj_id: int, data: AHJUpdate):
        ahj = self.get(db, ahj_id)
        if not ahj:
            return None
        payload = data.dict(exclude_none=True)
        canonical_name = payload.get("name") or payload.get("ahj_name")
        if canonical_name:
            payload["name"] = canonical_name
            payload["ahj_name"] = payload.get("ahj_name") or canonical_name
        for key, value in payload.items():
            setattr(ahj, key, value)
        db.commit()
        db.refresh(ahj)
        return ahj

    def delete(self, db: Session, ahj_id: int):
        ahj = self.get(db, ahj_id)
        if not ahj:
            return None
        db.delete(ahj)
        db.commit()
        return True