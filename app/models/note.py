<<<<<<< HEAD
from sqlalchemy import Column, Integer, ForeignKey, Text, Float, DateTime
from sqlalchemy.sql import func
=======
from sqlalchemy import Column, Integer, ForeignKey, Text, Float
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
from sqlalchemy.orm import relationship
from app.core.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    note_type_id = Column(Integer, ForeignKey("note_types.id"), nullable=True)
    note_description = Column(Text, nullable=False)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=True)
    page_no = Column(Integer, nullable=True)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)
    section_no = Column(Integer, nullable=True)
<<<<<<< HEAD
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    code = relationship("Code", backref="notes")
    note_type = relationship("NoteType", backref="notes")
    equipment = relationship("Equipment", back_populates="notes")
=======

    code = relationship("Code", backref="notes")
    note_type = relationship("NoteType", backref="notes")
    equipment = relationship("Equipment", backref="notes")
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af

    def __repr__(self):
        summary = (self.note_description or "")[:30]
        suffix = "..." if self.note_description and len(self.note_description) > 30 else ""
        return f"<Note(id={self.id}, note_description='{summary}{suffix}')>"

    def __str__(self):
        return self.__repr__()