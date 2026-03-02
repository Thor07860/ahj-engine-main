from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class AHJ(Base):
    __tablename__ = "ahjs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    ahj_name = Column(String(255), nullable=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    county = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    guidelines = Column(Text)
    fireset_back = Column(Float, nullable=True)
    jurisdiction_type = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    state = relationship("State", back_populates="ahjs")

    def __str__(self):
        return self.name or self.ahj_name or "AHJ"

    def __repr__(self):
        return f"<AHJ(id={self.id}, name='{self.name or self.ahj_name}')>"