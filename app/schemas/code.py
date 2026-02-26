from app.schemas import BaseSchema

class CodeBase(BaseSchema):
    code_name: str
    code_type_id: int

class CodeCreate(CodeBase):
    pass

class CodeUpdate(CodeBase):
    pass

class CodeOut(CodeBase):
    id: int