from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from backend.app.models.enums import City


class UserBase(BaseModel):
	first_name: str
	second_name: str
	email: str
	date_of_birth: date
	city: City

class UserCreate(UserBase):
	password: str
	pass

class UserUpdate(BaseModel):
	first_name: Optional[str] = None
	second_name: Optional[str] = None
	email: Optional[str] = None
	city: Optional[City] = None
	password: Optional[str] = None

class UserResponse(UserBase):
	id: int
	is_active: bool
	is_verified: bool
	created_at: datetime

	class Config:
		orm_mode=True

class UserInDB(UserResponse):
	password_hash: str







