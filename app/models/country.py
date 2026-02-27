from sqlalchemy import Column, Integer, String
from app.core.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    iso2 = Column(String(2), nullable=False, unique=True)
    iso3 = Column(String(3), nullable=False, unique=True)
    calling_code = Column(String(20), nullable=True)
    currency_code = Column(String(3), nullable=True)
