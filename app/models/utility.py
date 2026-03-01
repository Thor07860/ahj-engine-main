from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Utility(Base):
    __tablename__ = "utilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    utility_name = Column(String(255), nullable=False)

    requirements = Column(Text)

    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    ahj_id = Column(Integer, ForeignKey("ahjs.id"), nullable=True)
    eia_id = Column(String(100), nullable=True)
    utility_type = Column(String(100), nullable=True)
    service_territory = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Response type (this will later connect to ENUM logic)
    response_type = Column(String(50), nullable=True)

    # Relationship
    ahj = relationship("AHJ", backref="utilities")
<<<<<<< HEAD
    state = relationship("State", back_populates="utilities")

    def __str__(self):
        return self.name or self.utility_name
    
=======
    state = relationship("State", backref="utilities")

    #def __str__(self):
        #return self.utility_name
    

    def __str__(self):
        return self.name or self.utility_name

>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
    def __repr__(self):
        return f"<Utility(id={self.id}, name='{self.name or self.utility_name}')>"