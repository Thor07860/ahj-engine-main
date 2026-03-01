from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, synonym
from app.core.database import Base


class State(Base):
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True, default=1)
    name = Column(String(100), nullable=False)
    abbrev = Column(String(2), unique=True, nullable=False)
    abbreviation = synonym("abbrev")
    fips_code = Column(String(2), nullable=True)
    region = Column(String(50), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    country = relationship("Country", back_populates="states")
    ahjs = relationship("AHJ", back_populates="state")
    utilities = relationship("Utility", back_populates="state")
    clients = relationship("Client", back_populates="state")

    def __str__(self):
        return f"{self.abbrev} - {self.name}"

    def __repr__(self):
        return (
            f"<State(id={self.id}, "
            f"abbreviation='{self.abbrev}', "
            f"name='{self.name}', "
            f"created_at='{self.created_at}')>"
        )