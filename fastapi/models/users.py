from pydantic import BaseModel


class User(BaseModel):
    staff_id: str
    name: str
    hashed_password: str
    role: str = "staff"
    is_active: bool = True


class UserCreate(BaseModel):
    staff_id: str
    name: str
    password: str
    role: str = "staff"


class UserResponse(BaseModel):
    staff_id: str
    name: str
    role: str
    is_active: bool