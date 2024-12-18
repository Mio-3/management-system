from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from bson import ObjectId
import pytz


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ShiftStatus(str, Enum):
    PENDING = "未確認"
    APPROVED = "確認済み"


class ShiftPost(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    staff_name: str
    message: Optional[str] = None


class ShiftPostDB(ShiftPost):
    created_at: datetime = Field(
      default_factory=lambda: datetime.now(pytz.timezone("Asia/Tokyo"))
    )
    status: ShiftStatus = ShiftStatus.PENDING

    class Config:
        json_encoders = {
          ObjectId: str,
          datetime: lambda dt: (
            dt.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Tokyo'))
            if dt.tzinfo is None else dt.astimezone(pytz.timezone('Asia/Tokyo'))
          ).strftime("%Y/%m/%d %H:%M:%S")
        }
        allow_population_by_field_name = True