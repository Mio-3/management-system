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
    id: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    staff_id: str
    role: str


class UserRequest(UserBase):
    id: str


class LoginRequest(BaseModel):
    staff_id: str
    password: str


class TokenData(BaseModel):
    staff_id: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse