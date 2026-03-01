# app/schemas/__init__.py

from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True