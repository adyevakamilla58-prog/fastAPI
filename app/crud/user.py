from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.password import hash_password

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_pw = hash_password(user_in.password)

    db_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        surname=user_in.surname,
        login=user_in.login,
        hashed_password=hashed_pw,
        birthday=user_in.birthday,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(select(User).where(User.login == login))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_in: UserUpdate):
    user = await get_user(db, user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_none=True)

    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False