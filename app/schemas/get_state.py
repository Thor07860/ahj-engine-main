from pydantic import BaseModel
from typing import List

class StateNameRequest(BaseModel):
    abbrev: str


class UtilityOut(BaseModel):
    id: int
    name: str | None = None
    utility_name: str | None = None
    response_type: str | None = None
    utility_type: str | None = None
    service_territory: str | None = None
    eia_id: str | None = None
    phone: str | None = None
    website: str | None = None

class AHJOut(BaseModel):
    id: int
    name: str | None = None
    ahj_name: str | None = None
    county: str | None = None
    city: str | None = None
    utilities: List[UtilityOut]

class StateNameResponse(BaseModel):
    abbrev: str
    name: str
    fips_code: str | None = None
    region: str | None = None
    ahjs: List[AHJOut]