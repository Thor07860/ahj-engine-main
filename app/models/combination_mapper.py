from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class CombinationMapper(Base):
    __tablename__ = "combination_mapper"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)