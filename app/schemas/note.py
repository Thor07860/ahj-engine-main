from app.schemas import BaseSchema

class NoteBase(BaseSchema):
    note_description: str
    code_id: int

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int