from app.schemas import BaseSchema

class NoteBase(BaseSchema):
    note_type_id: int | None = None
    note_description: str
    code_id: int | None = None
    page_no: int | None = None
    length: float | None = None
    width: float | None = None
    equipment_id: int | None = None
    section_no: int | None = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int