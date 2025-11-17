from sqlalchemy import Boolean, Column, Date, Integer, String, DateTime, func, Enum as SqlEnum

from backend.app.db.base import Base
from backend.app.models.enums import City


class User(Base):
	__tablename__='users'

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True, nullable=False)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	password_hash = Column(String, nullable=False)
	phone_number = Column(String, unique=True, index=True, nullable=False)
	date_of_birth = Column(Date, nullable=False)
	city = Column(SqlEnum(City), nullable=False)
	created_at =Column(DateTime, server_default = func.now())
	updated_at = Column(DateTime, server_default = func.now(), onupdate=func.now())
	is_active = Column(Boolean, default=True)
	is_verified = Column(Boolean, default=False)









