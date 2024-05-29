from datetime import datetime

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, created_at, updated_at
from models.client import Client
from utils.database import async_session_factory


class Message(Base):
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(2000))
    contact: Mapped[str] = mapped_column(String(255))
    client_id: Mapped[int] = mapped_column(ForeignKey(Client.id))
    client_msg_ip: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    async def create(message: "Message") -> "Message":
        async with async_session_factory() as session:
            session.add(message)
            await session.flush()
            await session.commit()
            await session.refresh(message)
            return message

    @staticmethod
    async def get_last_date_client_msg(client_id: int) -> datetime | None:
        async with async_session_factory() as session:
            q = select(Message).where(Message.client_id == client_id).order_by(Message.created_at.desc())
            result = await session.execute(q)
            result = result.scalars().first()
            if result:
                return result.created_at
            return None
