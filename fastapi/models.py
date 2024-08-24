from pydantic import BaseModel
from uuid import UUID
from datetime import date


class ShiftBase(BaseModel):
    date: date
    category: str
    employee_id: UUID


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(ShiftBase):
    pass


class Shift(ShiftBase):
    id: UUID

    class Config:
        orm_mode = True