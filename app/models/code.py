from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)

    code_name = Column(String(255), nullable=False)

    code_type_id = Column(Integer, ForeignKey("code_types.id"), nullable=False)

    # Relationship
    code_type = relationship("CodeType", backref="codes")


    def __str__(self):
        return self.code_name