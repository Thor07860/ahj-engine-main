from sqlalchemy.orm import Session
from app.models.utility import Utility
from app.models.ahj import AHJ
from app.schemas.utility import UtilityCreate, UtilityUpdate

class UtilityService:

    def create(self, db: Session, data: UtilityCreate):
        payload = data.dict()
        payload["name"] = payload.get("utility_name")

        ahj = db.query(AHJ).filter(AHJ.id == payload.get("ahj_id")).first()
        payload["state_id"] = ahj.state_id if ahj else None

        utility = Utility(**payload)
        db.add(utility)
        db.commit()
        db.refresh(utility)
        return utility

    def get(self, db: Session, utility_id: int):
        return db.query(Utility).filter(Utility.id == utility_id).first()

    def get_all(self, db: Session):
        return db.query(Utility).all()

    def update(self, db: Session, utility_id: int, data: UtilityUpdate):
        utility = self.get(db, utility_id)
        if not utility:
            return None
        payload = data.dict()
        payload["name"] = payload.get("utility_name")

        ahj = db.query(AHJ).filter(AHJ.id == payload.get("ahj_id")).first()
        payload["state_id"] = ahj.state_id if ahj else utility.state_id

        for key, value in payload.items():
            setattr(utility, key, value)
        db.commit()
        db.refresh(utility)
        return utility

    def delete(self, db: Session, utility_id: int):
        utility = self.get(db, utility_id)
        if not utility:
            return None
        db.delete(utility)
        db.commit()
        return True