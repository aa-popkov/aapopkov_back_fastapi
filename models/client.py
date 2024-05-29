from sqlalchemy import select, update
from sqlalchemy.orm import Mapped

from models.base import Base, created_at, updated_at
from utils.database import async_session_factory


class Client(Base):
    frontend_id: Mapped[str]
    client_last_ip: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    async def create(client: "Client") -> "Client":
        async with async_session_factory() as session:
            session.add(client)
            await session.flush()
            await session.commit()
            await session.refresh(client)
            return client

    @staticmethod
    async def get_by_token_id(token_id: str) -> "Client":
        async with async_session_factory() as session:
            q = select(Client).where(Client.frontend_id == token_id)
            result = await session.execute(q)
            return result.scalar_one_or_none()

    @staticmethod
    async def update_ip(token_id: str, ip_address: str) -> int:
        async with async_session_factory() as session:
            q = update(Client).where(Client.frontend_id == token_id).values(client_last_ip=ip_address)
            result = await session.execute(q)
            return result.rowcount
