from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
    text_color = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    combination_mappers = relationship("CombinationMapper", back_populates="label")

    def __str__(self):
        code = self.upc_code or self.label_number
        display_name = self.name or self.label_name
        return f"{code} - {display_name}"

    def __repr__(self):
        return f"<Label(id={self.id}, code='{self.upc_code or self.label_number}', name='{self.name or self.label_name}')>"
