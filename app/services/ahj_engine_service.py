from sqlalchemy.orm import Session
from app.models.ahj import AHJ
from app.models.code import Code
from app.models.note import Note
from app.models.formula import Formula
from app.models.label import Label
from fastapi import HTTPException
from app.models.combination_mapper import CombinationMapper

class AHJEngineService:

    def get_code_id(self, db: Session, code_name: str):
        return db.query(Code).filter(Code.code_name == code_name).first()

    def fetch_details(self, db: Session, code_obj: Code):
        # Labels
        mappings = db.query(CombinationMapper).filter(
            CombinationMapper.code_id == code_obj.id
        ).all()

        label_ids = [m.label_id for m in mappings]
        labels = db.query(Label).filter(Label.id.in_(label_ids)).all()

        # Notes
        notes = db.query(Note).filter(Note.code_id == code_obj.id).all()

        # Formulas
        formulas = db.query(Formula).filter(Formula.code_id == code_obj.id).all()

        return {
            "code_name": code_obj.code_name,
            "labels": [{"id": l.id, "label_name": l.label_name, "field_type": l.field_type} for l in labels],
            "notes": [n.note_description for n in notes],
            "formulas": [f.description for f in formulas]
        }

    def process(
        self,
        db: Session,
        ahj_name: str,
        electrical_code: str,
        structural_code: str,
        fire_code: str
    ):
        # AHJ lookup
        ahj = db.query(AHJ).filter(AHJ.ahj_name == ahj_name).first()
        if not ahj:
            raise HTTPException(404, "AHJ not found")

        # Electrical code
        electrical = self.get_code_id(db, electrical_code)
        if not electrical:
            raise HTTPException(404, "Electrical code not found")

        # Structural code
        structural = self.get_code_id(db, structural_code)
        if not structural:
            raise HTTPException(404, "Structural code not found")

        # Fire code
        fire = self.get_code_id(db, fire_code)
        if not fire:
            raise HTTPException(404, "Fire code not found")

        return {
            "ahj_name": ahj_name,
            "electrical": self.fetch_details(db, electrical),
            "structural": self.fetch_details(db, structural),
            "fire": self.fetch_details(db, fire)
        }