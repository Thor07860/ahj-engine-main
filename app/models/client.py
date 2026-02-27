from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    spex_client_code = Column(Integer, nullable=False)
    company_name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
