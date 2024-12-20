from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    session_id: str
    staff_id: str
    expires_at: datetime