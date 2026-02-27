from datetime import date

from app.schemas import BaseSchema

class CodeBase(BaseSchema):
    title: str | None = None
    code_name: str | None = None
    code_type_id: int
    code_amendments: int | None = None
    description: str | None = None
    edition: str | None = None
    applicable_code_category_id: int | None = None
    issuing_body: str | None = None
    state_id: int | None = None
    adopted_at: date | None = None

class CodeCreate(CodeBase):
    pass

class CodeUpdate(CodeBase):
    pass

class CodeOut(CodeBase):
    id: int
    created_at: str | None = None