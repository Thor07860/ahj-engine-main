from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Utility(Base):
    __tablename__ = "utilities"

    id = Column(Integer, primary_key=True, index=True)
    utility_name = Column(String(255), nullable=False)

    ahj_id = Column(Integer, ForeignKey("ahjs.id"), nullable=False)

    # Response type (this will later connect to ENUM logic)
    response_type = Column(String(50), nullable=False)

    # Relationship
    ahj = relationship("AHJ", backref="utilities")

    def __str__(self):
        return self.utility_name