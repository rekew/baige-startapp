from typing import Optional

from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, create_refresh_token, verify_password
from backend.app.models.user import User
from backend.app.schemas.token import Token


class AuthService:
	def __init__(self, db: Session):
		self.db = db


	def authenticate_user(self, email: str, password: str) -> Optional[User]:
		user = self.db.query(User).filter(User.email == email).first()

		if not user:
			return None
		if not verify_password(password, user.password_hash):
			return None
		return user

	@staticmethod
	def create_tokens(user: User) -> Token:
		access_token = create_access_token(data={"sub": user.email})
		refresh_token = create_refresh_token(data={"sub": user.email})
		return Token(access_token=access_token, refresh_token=refresh_token)



