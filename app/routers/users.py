from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import (
    create_user, get_user, get_users,
    update_user, delete_user, get_user_by_login
)
from app.utils.auth import create_access_token, get_current_user
from app.utils.password import verify_password
from app.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidCredentialsException
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user_by_login(db, user.login):
        raise UserAlreadyExistsException()
    return await create_user(db, user)


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_login(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsException()

    access_token = create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserRead])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return await get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    user = await get_user(db, user_id)
    if user is None:
        raise UserNotFoundException()
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_info(
        user_id: int,
        user: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    updated = await update_user(db, user_id, user)
    if updated is None:
        raise UserNotFoundException()
    return updated


@router.delete("/{user_id}")
async def delete_user_info(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)
):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise UserNotFoundException()
    return {"message": "Пользователь удален"}