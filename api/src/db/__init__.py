from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session
from typing import Iterable

from ..config import read_config


engine: Engine


def init_db() -> None:
    config = read_config()

    connect_args = {"check_same_thread": False}

    global engine
    engine = create_engine(
        url=config.db.url,
        connect_args=connect_args,
        echo=config.db.log_sql,
    )
    if config.db.create_schema:
        SQLModel.metadata.create_all(engine)


def get_engine() -> Engine:
    global engine
    return engine


def get_session() -> Iterable[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
