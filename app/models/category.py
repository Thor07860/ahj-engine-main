<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    combination_mappers = relationship("CombinationMapper", back_populates="category")

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
=======
from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    def __str__(self):
        return self.name
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
