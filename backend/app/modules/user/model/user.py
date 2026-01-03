from datetime import date
from sqlalchemy import String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_models import TimestampMixin
from app.db.base import Base
from app.modules.basic.enums import City


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    date_of_birth: Mapped[date] = mapped_column()
    city: Mapped[City] = mapped_column(SqlEnum(City))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)