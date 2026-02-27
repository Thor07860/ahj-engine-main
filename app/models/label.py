from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)

    upc_code = Column(String(100), unique=True, nullable=True)
    name = Column(String(255), nullable=True)
    label_number = Column(String(100), unique=True, nullable=False)
    label_name = Column(String(255), nullable=False)
    field_type = Column(String(100), nullable=True)
    description = Column(Text)

    # Newly added after seeing the Xl sheet 

    length = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    image_url = Column(String(500), nullable=True)
    background_color = Column(String(100) , nullable=True)
    text_color = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # for adding the image over here 
    # image_url = Column(String(500), nullable=True )


    def __str__(self):
        code = self.upc_code or self.label_number
        display_name = self.name or self.label_name
        return f"{code} - {display_name}"

    def __repr__(self):
        return f"<Label(id={self.id}, code='{self.upc_code or self.label_number}', name='{self.name or self.label_name}')>"
