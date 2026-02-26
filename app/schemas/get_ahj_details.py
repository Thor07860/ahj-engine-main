from pydantic import BaseModel
from typing import List, Dict

class AHJDetailRequest(BaseModel):
    ahj_name: str
    electrical_code: str
    structural_code: str
    fire_code: str



class CodeDetail(BaseModel):
    code_name: str
    labels: List[Dict]
    notes: List[str]
    formulas: List[str]

class AHJDetailResponse(BaseModel):
    ahj_name: str
    electrical: CodeDetail
    structural: CodeDetail
    fire: CodeDetail