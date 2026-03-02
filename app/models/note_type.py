from sqlalchemy import Column, Integer, String
from app.core.database import Base


class NoteType(Base):
    __tablename__ = "note_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    variation_type = Column(String(100), nullable=True)

    def __str__(self):
        return f"{self.name or ''} - {self.variation_type or ''}".strip(" -")
