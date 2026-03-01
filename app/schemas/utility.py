from app.schemas import BaseSchema

class UtilityBase(BaseSchema):
    name: str | None = None
    utility_name: str | None = None
    state_id: int | None = None
    ahj_id: int | None = None
    requirements: str | None = None
    eia_id: str | None = None
    utility_type: str | None = None
    service_territory: str | None = None
    phone: str | None = None
    website: str | None = None
    response_type: str | None = None

class UtilityCreate(UtilityBase):
    pass

class UtilityUpdate(UtilityBase):
    pass

class UtilityOut(UtilityBase):
    id: int
    created_at: str | None = None