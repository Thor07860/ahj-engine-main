from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class StateCode(Base):
    __tablename__ = "state_codes"

    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)
