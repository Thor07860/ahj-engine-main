from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class AHJ(Base):
    __tablename__ = "ahjs"

    id = Column(Integer, primary_key=True, index=True)
    ahj_name = Column(String(255), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"))
    guidelines = Column(Text)

    # Relationship
    state = relationship("State", backref="ahjs")

    def __str__(self):
        return self.ahj_name