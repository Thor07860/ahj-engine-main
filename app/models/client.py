<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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

    # Relationships
    state = relationship("State", back_populates="clients")
    country = relationship("Country", back_populates="clients")
    preferences = relationship("Preference", back_populates="client", uselist=False)

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip() or self.company_name or f"Client {self.id}"
        return name

    def __repr__(self):
        return f"<Client(id={self.id}, email='{self.email}', company='{self.company_name}')>"
=======
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
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
