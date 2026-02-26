from sqlalchemy.orm import Session
from app.models.formula import Formula

class FormulaService:
    def get_by_code(self, db: Session, code_id: int):
        return db.query(Formula).filter(Formula.code_id == code_id).all()