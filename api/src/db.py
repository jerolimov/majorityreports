from sqlmodel import SQLModel, create_engine, Session
from typing import Iterable


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///test.db", connect_args=connect_args, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterable[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
