from app.schemas import BaseSchema

class StateBase(BaseSchema):
    abbrev: str
    name: str

class StateCreate(StateBase):
    pass

class StateUpdate(StateBase):
    pass

class StateOut(StateBase):
    id: int