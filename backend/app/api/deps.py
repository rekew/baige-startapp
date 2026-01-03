from fastapi import Depends, HTTPException, status as http_status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import verify_token
from app.db.session import get_db
from app.modules.user.model.user import User

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    email = verify_token(token, token_type="access")
    if email is None:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="There is no user with such credentials",
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user