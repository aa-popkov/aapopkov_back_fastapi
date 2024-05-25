from typing import Optional, List

from sqlalchemy import String, select, delete, update
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base
from utils.database import async_session_factory


class User(Base):
    username: Mapped[str] = mapped_column(String(50), index=True)
    hashed_password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    @staticmethod
    async def create(user: "User"):
        async with async_session_factory() as session:
            session.add(user)
            await session.flush()
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_by_username(username: str) -> Optional["User"]:
        async with async_session_factory() as session:
            q = select(User).where(User.username == username)
            result = await session.execute(q)
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_by_username(username: str) -> bool:
        async with async_session_factory() as session:
            q = delete(User).where(User.username == username)
            await session.execute(q)
            await session.flush()
            await session.commit()
            return True

    @staticmethod
    async def change_password(user: "User", new_password: bytes):
        async with async_session_factory() as session:
            q = update(User).where(User.username == user.username).values(hashed_password=new_password)
            await session.execute(q)
            await session.flush()
            await session.commit()
            return True

    @staticmethod
    async def get_all_users(page_number: int = 0, page_size: int = 10) -> List["User"]:
        async with async_session_factory() as session:
            q = select(User).order_by(User.username).limit(page_size).offset(page_number)
            result = await session.execute(q)
            return result.scalars().all()
