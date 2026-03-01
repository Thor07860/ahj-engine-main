from app.schemas import BaseSchema

class CodeTypeBase(BaseSchema):
    title: str | None = None
    key: str | None = None
    description: str | None = None

class CodeTypeCreate(CodeTypeBase):
    pass

class CodeTypeUpdate(CodeTypeBase):
    pass

class CodeTypeOut(CodeTypeBase):
    id: int