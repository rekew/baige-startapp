from datetime import date, datetime
from typing import Annotated, Optional

import phonenumbers
from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.models.enums import City


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Annotated[PhoneNumber, "KZ"]
    date_of_birth: date
    city: City

    @field_validator ("phone_number", mode = "before")
    def normalize_phone (cls, value):
        num = phonenumbers.parse (value, "KZ")
        return phonenumbers.format_number (num, phonenumbers.PhoneNumberFormat.E164)


class UserCreate(UserBase):
    password: str
    pass


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    city: Optional[City] = None
    phone_number: Optional[Annotated[PhoneNumber, "KZ"]] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserInDB(UserResponse):
    password_hash: str


class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class UserLogin(BaseModel):
    email: str
    password: str
