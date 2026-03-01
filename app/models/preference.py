<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, unique=True)
    language = Column(String(20), nullable=False, server_default="en")
    timezone = Column(String(100), nullable=True)
    date_format = Column(String(50), nullable=True)
    unit_system = Column(String(20), nullable=True)
    notifications_enabled = Column(Boolean, nullable=False, server_default="1")
    theme = Column(String(50), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    client = relationship("Client", back_populates="preferences")

    def __str__(self):
        return f"Preferences for Client {self.client_id} ({self.language}, {self.timezone})"

    def __repr__(self):
        return f"<Preference(id={self.id}, client_id={self.client_id}, language='{self.language}')>"
=======
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, unique=True)
    language = Column(String(20), nullable=False, server_default="en")
    timezone = Column(String(100), nullable=True)
    date_format = Column(String(50), nullable=True)
    unit_system = Column(String(20), nullable=True)
    notifications_enabled = Column(Boolean, nullable=False, server_default="1")
    theme = Column(String(50), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
