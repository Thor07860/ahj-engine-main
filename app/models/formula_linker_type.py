from sqlalchemy import Column, Integer, String
from app.core.database import Base


class FormulaLinkerType(Base):
    __tablename__ = "formula_linker_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)

    def __str__(self):
        return self.name
