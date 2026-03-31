from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    create_engine,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Base model
Base = declarative_base()


# Users model
class User(Base):
    __tablename__ = "users"

    id = Column( # noqa VNE003
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    chat_id = Column(Integer, nullable=False, unique=True)
    user_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    username = Column(String)
    enabled_rep = Column(Boolean, nullable=False, default=True)
    role = Column(String, nullable=False, default="user")
    restricted = Column(Boolean, nullable=False, default=False)
    registered = Column(
        DateTime, nullable=False, server_default=func.current_timestamp(),
    )


# Repetitions model
class Repetition(Base):
    __tablename__ = "repetitions"

    id = Column( # noqa VNE003
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    chat_id = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    button_text = Column(String, nullable=False, default="")
    button_link = Column(String, nullable=False, default="")
    time_to_send = Column(DateTime, nullable=True, default=None)
    confirmed = Column(Boolean, nullable=False, default=False)
    is_send = Column(Boolean, nullable=False, default=False)


# Init DB
def init_db(db_path="database/db.sqlite3"):
    # Keep schema bootstrap synchronous to avoid async initialization at import time.
    sync_engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(sync_engine)
    sync_engine.dispose()

    async_engine = create_async_engine(
        f"sqlite+aiosqlite:///{db_path}",
        echo=False,
    )
    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
