from sqlalchemy import Column, Integer, String
from app.core.database import Base

class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    abbrev = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name