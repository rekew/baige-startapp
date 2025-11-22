from typing import List

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse, UserUpdate, UserUpdatePassword

router = APIRouter(prefix="/user")


# GET Routers
@router.get("/all", response_model=List[UserResponse])
def get_all_users_endpoint(db: AsyncSession   = Depends(get_db)):
    user_repo = UserRepository(db)
    users = user_repo.get_all()
    return users


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(user_id: int, db: AsyncSession  = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_http_status.HTTP_404_NOT_FOUND_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email_endpoint(email: str, db: AsyncSession  = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/phone/{phone}", response_model=UserResponse)
def get_user_by_phone_endpoint(phone: str, db: AsyncSession  = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_phone_number(phone)
    if user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# PUT & PATCH Routers
@router.patch("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession  = Depends(get_db),
    _: User = Depends(get_current_user),
):
    user_repo = UserRepository(db)
    existing_user = user_repo.get_by_id(user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.phone_number:
        existing_phone = user_repo.get_by_phone_number(user.phone_number)
        if existing_phone and existing_phone.id != user_id:
            raise HTTPException(
                status_code=http_status.HTTP_http_status.HTTP_400_BAD_REQUEST_BAD_REQUEST,
                detail="Phone already registered",
            )

    updated_user = user_repo.update(user_id, user)
    return updated_user


@router.patch("/{user_id}/password", response_model=UserResponse)
def update_user_password_endpoint(
    user_id: int,
    password: UserUpdatePassword,
    db: AsyncSession  = Depends(get_db),
    _: User = Depends(get_current_user),
):
    user_repo = UserRepository(db)
    existing_user = user_repo.get_by_id(user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    updated_user = user_repo.update_password(user_id, password)
    if updated_user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif updated_user == "wrong_old_password":
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password",
        )
    elif updated_user == "passwords_dont_match":
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match",
        )
    return updated_user


# DELETE Routers
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_endpoint(user_id: int, db: AsyncSession  = Depends(get_db)):
    user_repo = UserRepository(db)
    existing_user = user_repo.get_by_id(user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_repo.delete(existing_user.id)
    return existing_user
