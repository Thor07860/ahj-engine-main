from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)

    code_name = Column(String(255), nullable=False)

    code_type_id = Column(Integer, ForeignKey("code_types.id"), nullable=False)
    code_amendments = Column(Integer, ForeignKey("code_amendments.id"), nullable=True)
    title = Column(String(255), nullable=False)

    description = Column(Text)
    edition = Column(String(100), nullable=True)
    applicable_code_category_id = Column(Integer, ForeignKey("applicable_code_categories.id"), nullable=True)
    issuing_body = Column(String(255), nullable=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    adopted_at = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

<<<<<<< HEAD
    # Relationships
=======
    # Relationship
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
    code_type = relationship("CodeType", backref="codes")
    amendment = relationship("CodeAmendment", backref="codes")
    applicable_category = relationship("ApplicableCodeCategory", backref="codes")
    state = relationship("State", backref="codes")
<<<<<<< HEAD
    combination_mappers = relationship(
        "CombinationMapper",
        back_populates="code",
        cascade="all, delete-orphan"
    )
=======
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af


    #def __str__(self):
        #return self.code_name
    
    def __str__(self):
        amendment_name = None
        if self.amendment is not None:
            amendment_name = self.amendment.name
        elif self.code_amendments is not None:
            amendment_name = str(self.code_amendments)

        title = self.title or self.code_name
        if self.edition and amendment_name:
            return f"{self.edition} {title} - {amendment_name}"
        if self.edition:
            return f"{self.edition} {title}"
        if amendment_name:
            return f"{title} - {amendment_name}"
        return title

    def __repr__(self):
        return f"<Code(id={self.id}, title='{self.title or self.code_name}')>"