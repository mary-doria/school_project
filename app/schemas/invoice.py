from pydantic import BaseModel
from typing import Optional

class InvoiceBase(BaseModel):
    amount: float
    paid: Optional[bool] = False
    student_id: int

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int

    class Config:
        orm_mode = True
