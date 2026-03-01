from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Formula(Base):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    formula_link_type_id = Column(Integer, ForeignKey("formula_linker_types.id"), nullable=True)
    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)

    code = relationship("Code", backref="formulas")
    formula_link_type = relationship("FormulaLinkerType", backref="formulas")

    def __repr__(self):
        summary = (self.description or "")[:30]
        suffix = "..." if self.description and len(self.description) > 30 else ""
        return f"<Formula(id={self.id}, description='{summary}{suffix}')>"

    def __str__(self):
        return self.__repr__()