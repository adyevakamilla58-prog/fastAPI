from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    login: str
    birthday: date


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    surname: Optional[str] = None
    birthday: Optional[date] = None


class UserRead(UserBase):
    id: int
    registered_at: datetime

    model_config = {"from_attributes": True}