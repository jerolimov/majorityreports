from sqlmodel import Field, SQLModel, create_engine, Session, select, func
from typing import Optional, Iterable


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    done: Optional[bool] = Field(default=False)


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///test.db", connect_args=connect_args, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        countStatement = select(func.count()).select_from(Todo)
        count = session.scalar(countStatement)
        if count == 0:
            session.add(Todo(name="todo a", done=False))
            session.add(Todo(name="todo b", done=False))
            session.add(Todo(name="todo c", done=False))
            session.add(Todo(name="done", done=True))
            session.commit()


def get_session() -> Iterable[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
