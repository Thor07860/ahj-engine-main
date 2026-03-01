<<<<<<< HEAD
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
=======
from sqlalchemy import Column, Integer, ForeignKey
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
from app.core.database import Base

class CombinationMapper(Base):
    __tablename__ = "combination_mapper"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=True)
<<<<<<< HEAD
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=True)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    category = relationship("Category", back_populates="combination_mappers")
    equipment = relationship("Equipment", back_populates="combination_mappers")
    code = relationship("Code", back_populates="combination_mappers")
    label = relationship("Label", back_populates="combination_mappers")

    def __repr__(self):
        return f"<CombinationMapper(id={self.id}, code_id={self.code_id}, label_id={self.label_id})>"
    
    def __str__(self):
        return f"Code {self.code_id} -> Label {self.label_id}"
=======
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
