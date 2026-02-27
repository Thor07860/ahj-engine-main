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
