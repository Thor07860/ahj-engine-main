from app.schemas import BaseSchema

class UtilityBase(BaseSchema):
    utility_name: str
    ahj_id: int
    response_type: str

class UtilityCreate(UtilityBase):
    pass

class UtilityUpdate(UtilityBase):
    pass

class UtilityOut(UtilityBase):
    id: int