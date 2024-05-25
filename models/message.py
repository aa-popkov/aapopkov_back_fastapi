from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, created_at, updated_at
from models.client import Client


class Message(Base):
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(2000))
    client_id: Mapped[int] = mapped_column(ForeignKey(Client.id))
    client_msg_ip: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
