import hashlib
from typing import Optional, List

from sqlalchemy.orm import Session

from backend.app.core.security import get_password_hash, pwd_context
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate, UserUpdatePassword


class UserRepository:
	def __init__ (self, db: Session):
		self.db = db

	# GET all Users
	def get_all (self) -> List[User]:
		return self.db.query (User).all ()

	# GET User by ID
	def get_by_id (self, user_id: int) -> Optional[User]:
		return self.db.query (User).filter (User.id == user_id).first ()

	# GET User by Email
	def get_by_email (self, email: str) -> Optional[User]:
		return self.db.query (User).filter (User.email == email).first ()

	# GET User by phone number
	def get_by_phone_number (self, phone: str) -> Optional[User]:
		return self.db.query (User).filter (User.phone_number == phone).first ()

	# POST Create User
	def create (self, user: UserCreate) -> User:
		hashed_password = get_password_hash (user.password)
		phone_normalized = str (user.phone_number).replace ('tel:', '').replace ('-', '').replace (' ', '')
		db_user = User (
			first_name = user.first_name,
			last_name = user.last_name,
			email = user.email,
			phone_number = phone_normalized,
			password_hash = hashed_password,
			date_of_birth = user.date_of_birth,
			city = user.city,
		)
		self.db.add (db_user)
		self.db.commit ()
		self.db.refresh (db_user)
		return db_user

	# PUT the User
	def update (self, user_id: int, user_update: UserUpdate) -> Optional[User]:
		db_user = self.db.query (User).filter (User.id == user_id).first ()

		if not db_user:
			return None

		update_data = user_update.model_dump (exclude_unset = True)

		for field, value in update_data.items ():
			setattr (db_user, field, value)

		self.db.commit ()
		self.db.refresh (db_user)
		return db_user

	# PATCH User password
	def update_password (self, user_id: int, password: UserUpdatePassword) -> Optional[User] | str:
		db_user = self.db.query (User).filter (User.id == user_id).first()
		password_hashed = hashlib.sha256 (password.old_password.encode ('utf-8')).hexdigest ()
		if not db_user:
			return None

		if not pwd_context.verify (password_hashed, db_user.password_hash):
			return "wrong_old_password"

		if password.new_password != password.confirm_password:
			return "passwords_dont_match"

		db_user.password_hash = get_password_hash (password.new_password)

		self.db.commit ()
		self.db.refresh (db_user)
		return db_user

	# DELETE User
	def delete (self, user_id: int) -> bool:
		db_user = self.db.query (User).filter (User.id == user_id).first ()

		if not db_user:
			return False

		self.db.delete (db_user)
		self.db.commit ()
		return True