from sqlalchemy import Column, Integer, String
from app.core.database import Base

class CodeType(Base):
    __tablename__ = "code_types"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    key = Column(String(100), nullable=True, unique=True)
    description = Column(String(255), nullable=True)

   # def __str__(self):
        #return self.key 
    
    def __str__(self):
        return self.title or self.key or "Code Type"

    def __repr__(self):
        return f"<CodeType(id={self.id}, title='{self.title or self.key}')>"