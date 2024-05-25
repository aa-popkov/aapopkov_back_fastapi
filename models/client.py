from sqlalchemy.orm import Mapped

from models.base import Base, created_at, updated_at


class Client(Base):
    frontend_id: Mapped[str]
    client_last_ip: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
