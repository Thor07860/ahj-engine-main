from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class StateCode(Base):
    """Junction table for many-to-many relationship between States and Codes"""
    __tablename__ = "state_codes"

    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    state = relationship("State", backref="state_codes")
    code = relationship("Code", backref="state_codes")

    def __str__(self):
        return f"State {self.state_id} - Code {self.code_id}"

    def __repr__(self):
        return f"<StateCode(id={self.id}, state_id={self.state_id}, code_id={self.code_id})>"
