from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class AHJCode(Base):
    __tablename__ = "ahj_codes"

    id = Column(Integer, primary_key=True, index=True)
    ahj_id = Column(Integer, ForeignKey("ahjs.id"), nullable=False)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)
