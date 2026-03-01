from typing import Optional

from app.schemas import BaseSchema

class AHJBase(BaseSchema):
    name: Optional[str] = None
    ahj_name: Optional[str] = None
    state_id: int
    county: Optional[str] = None
    city: Optional[str] = None
    guidelines: Optional[str] = None
    fireset_back: Optional[float] = None
    jurisdiction_type: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None

class AHJCreate(AHJBase):
    pass

class AHJUpdate(AHJBase):
    pass

class AHJOut(AHJBase):
    id: int
    created_at: Optional[str] = None