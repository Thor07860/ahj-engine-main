from sqlalchemy import Column, Integer, String
from app.core.database import Base


class ApplicableCodeCategory(Base):
    __tablename__ = "applicable_code_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    def __str__(self):
        return self.name
