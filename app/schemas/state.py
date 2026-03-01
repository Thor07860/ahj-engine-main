from app.schemas import BaseSchema

class StateBase(BaseSchema):
    abbrev: str
    name: str
    fips_code: str | None = None
    region: str | None = None

class StateCreate(StateBase):
    pass

class StateUpdate(StateBase):
    pass

class StateOut(StateBase):
    id: int
    created_at: str | None = None