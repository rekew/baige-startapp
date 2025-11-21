import hashlib
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from backend.app.core.security import get_password_hash, pwd_context
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate, UserUpdatePassword


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # GET all Users
    async def get_all(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    # GET User by ID
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    # GET User by Email
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    # GET User by phone number
    async def get_by_phone_number(self, phone: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.phone_number == phone)
        )
        return result.scalar_one_or_none()

    # POST Create User
    async def create(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)

        phone_normalized = (
            str(user.phone_number)
            .replace("tel:", "")
            .replace("-", "")
            .replace(" ", "")
        )

        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=phone_normalized,
            password_hash=hashed_password,
            date_of_birth=user.date_of_birth,
            city=user.city,
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    # PUT the User
    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        # Получаем пользователя
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        db_user = result.scalar_one_or_none()

        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    # PATCH User password
    async def update_password(
        self, user_id: int, password: UserUpdatePassword
    ) -> Optional[User] | str:

        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        db_user = result.scalar_one_or_none()

        if not db_user:
            return None

        password_hashed = hashlib.sha256(
            password.old_password.encode("utf-8")
        ).hexdigest()

        if not pwd_context.verify(password_hashed, db_user.password_hash):
            return "wrong_old_password"

        if password.new_password != password.confirm_password:
            return "passwords_dont_match"

        db_user.password_hash = get_password_hash(password.new_password)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    # DELETE User
    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        db_user = result.scalar_one_or_none()

        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.commit()

        return True
