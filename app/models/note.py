from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    note_description = Column(Text, nullable=False)

    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)

    code = relationship("Code", backref="notes")


    def __str__(self):
        # Show first 30 chars for readability
        return self.note_description[:30] + "..."