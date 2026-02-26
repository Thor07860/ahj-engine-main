from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Formula(Base):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(Text, nullable=False)

    code_id = Column(Integer, ForeignKey("codes.id"), nullable=False)

    code = relationship("Code", backref="formulas")


    def __str__(self):
        return self.description[:30] + "..."