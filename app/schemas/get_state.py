from pydantic import BaseModel
from typing import List, Dict

class StateNameRequest(BaseModel):
    abbrev: str


class UtilityOut(BaseModel):
    id: int
    utility_name: str
    response_type: str

class AHJOut(BaseModel):
    id: int
    ahj_name: str
    utilities: List[UtilityOut]

class StateNameResponse(BaseModel):
    abbrev: str
    name: str
    ahjs: List[AHJOut]