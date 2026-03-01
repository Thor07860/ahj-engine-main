from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class AHJCode(Base):
    """Junction table for many-to-many relationship between AHJs and Codes"""
    __tablename__ = "ahj_codes"

    id = Column(Integer, primary_key=True, index=True)
    ahj_id = Column(Integer, ForeignKey("ahjs.id"), nullable=False)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    ahj = relationship("AHJ", backref="ahj_codes")
    code = relationship("Code", backref="ahj_codes")

    def __str__(self):
        return f"AHJ {self.ahj_id} - Code {self.code_id}"

    def __repr__(self):
        return f"<AHJCode(id={self.id}, ahj_id={self.ahj_id}, code_id={self.code_id})>"
