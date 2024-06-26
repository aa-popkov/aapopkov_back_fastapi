from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from utils.config import config

async_engine = create_async_engine(
    url=config.connection_string_async,
    echo=False,
)

async_session_factory = async_sessionmaker(async_engine)
