from app.schemas import BaseSchema

class CodeTypeBase(BaseSchema):
    key: str
    description: str | None = None

class CodeTypeCreate(CodeTypeBase):
    pass

class CodeTypeUpdate(CodeTypeBase):
    pass

class CodeTypeOut(CodeTypeBase):
    id: int