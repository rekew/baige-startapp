from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import verify_token
from app.db import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.repositories.user import UserRepository

router = APIRouter(prefix="/auth")


@router.post(
    "/register", response_model=UserResponse, status_code=http_status.HTTP_201_CREATED
)
async def register_endpoint(user_create: UserCreate, db: AsyncSession  = Depends(get_db)):
    user_repository = UserRepository(db)
    print(user_create.email)
    existing_user = await user_repository.get_by_email(user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user = await user_repository.create(user_create)
    return user


@router.post("/login", response_model=Token)
async def login_endpoint(login_data: UserLogin, db: AsyncSession  = Depends(get_db)):
    auth_service = AuthService(db)

    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_service.create_tokens(user)


@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(refresh_token: str, db: AsyncSession  = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(db)
    email = verify_token(refresh_token, token_type="refresh")
    if email is None:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_repository.get_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_service.create_tokens(user)


@router.get("/me", response_model=UserResponse)
def get_me_endpoint(current_user: UserResponse = Depends(get_current_user)):
    return current_user
