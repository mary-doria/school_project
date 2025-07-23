from pydantic import BaseModel
from typing import Optional

class SchoolBase(BaseModel):
    name: str
    city: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id: int

    class Config:
        orm_mode = True
