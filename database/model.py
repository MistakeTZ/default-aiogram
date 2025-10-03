from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    telegram_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    username = Column(String)
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
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
