from app.schemas import BaseSchema

class AHJBase(BaseSchema):
    ahj_name: str
    state_id: int

class AHJCreate(AHJBase):
    pass

class AHJUpdate(AHJBase):
    pass

class AHJOut(AHJBase):
    id: int