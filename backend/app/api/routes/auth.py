from asyncio.sslproto import SSLAgainErrors

from fastapi import APIRouter, Depends, HTTPException, status as http_status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_user
from backend.app.core.security import verify_token
from backend.app.db.session import get_db
from backend.app.schemas.token import Token
from backend.app.schemas.user import UserCreate, UserLogin, UserResponse
from backend.app.services.auth_service import AuthService
from backend.app.repositories.user import UserRepository

router = APIRouter(prefix="/auth")


@router.post(
    "/register", response_model=UserResponse, status_code=http_status.HTTP_201_CREATED
)
async def register_endpoint(user_create: UserCreate, db: AsyncSession  = Depends(   get_db)):
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


@router.post("/login")
async def login_endpoint(response: Response, login_data: UserLogin, db: AsyncSession  = Depends(get_db)):
    auth_service = AuthService(db)

    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = auth_service.create_tokens(user)

    response.set_cookie(
        key = "access_token",
        value = tokens.access_token,
        httponly = True,
        samesite = "lax",
        max_age = 1800
    )

    response.set_cookie(
        key = "refresh_token",
        value = tokens.refresh_token,
        httponly = True,
        samesite = "lax",
        max_age = 604800
    )

    return {"message": "Login successful"}


@router.post("/refresh")
async def refresh_token_endpoint(response: Response, refresh_token: str, db: AsyncSession  = Depends(get_db)):
    user_repository = UserRepository(db)
    auth_service = AuthService(db)
    email = verify_token(refresh_token, token_type="refresh")
    if email is None:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_repository.get_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tokens = auth_service.create_tokens (user)

    response.set_cookie (
        key = "access_token",
        value = tokens.access_token,
        httponly = True,
        samesite = "lax",
        max_age = 1800
    )

    return {"message": "Token refreshed"}

@router.post("/logout")
async def logout_endpoint(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logout successful"}

@router.get("/me", response_model=UserResponse)
async def get_me_endpoint(current_user: UserResponse = Depends(get_current_user)):
    return current_user
