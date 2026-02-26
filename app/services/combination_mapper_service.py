from sqlalchemy.orm import Session
from app.models.combination_mapper import CombinationMapper

class CombinationMapperService:
    def get_label_ids(self, db: Session, code_id: int):
        mappings = db.query(CombinationMapper).filter(CombinationMapper.code_id == code_id).all()
        return [m.label_id for m in mappings]