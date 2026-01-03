from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.modules.user.model.user import User
from app.modules.user.schemas.token import Token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

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
