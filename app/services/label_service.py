from sqlalchemy.orm import Session
from app.models.label import Label

class LabelService:
    def get_by_ids(self, db: Session, ids: list[int]):
        return db.query(Label).filter(Label.id.in_(ids)).all()