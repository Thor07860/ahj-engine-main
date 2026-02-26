from app.schemas import BaseSchema

class UserBase(BaseSchema):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int