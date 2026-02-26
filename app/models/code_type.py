from sqlalchemy import Column, Integer, String
from app.core.database import Base

class CodeType(Base):
    __tablename__ = "code_types"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), nullable=False, unique=True)      # Example: success / failed / initiated
    description = Column(String(255), nullable=True)

    def __str__(self):
        return self.key 