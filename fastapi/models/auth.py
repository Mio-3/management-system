from pydantic import BaseModel


class LoginRequest(BaseModel):
    staff_id: str
    password: str