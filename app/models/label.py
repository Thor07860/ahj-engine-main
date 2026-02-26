from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)

    label_name = Column(String(255), nullable=False)
    field_type = Column(String(100), nullable=False)