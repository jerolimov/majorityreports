from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel import Field, SQLModel, Session, select
from typing import Optional, Iterable
from .db import get_session


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    done: Optional[bool] = Field(default=False)


router = APIRouter()


@router.post("")
def create_todo(newTodo: Todo, session: Session = Depends(get_session)) -> Todo:
    todo = Todo()
    todo.name = newTodo.name
    if isinstance(newTodo.done, bool):
        todo.done = newTodo.done
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.get("")
def get_todos(session: Session = Depends(get_session)) -> Iterable[Todo]:
    statement = select(Todo)
    return session.exec(statement).all()


@router.get("{todo_id}")
def get_todo_by_todo_id(todo_id: int, session: Session = Depends(get_session)) -> Todo:
    todo = session.get_one(Todo, todo_id)
    return todo


@router.put("{todo_id}")
def update_todo_by_todo_id(
    todo_id: int, updateTodo: Todo, session: Session = Depends(get_session)
) -> Todo:
    todo = session.get_one(Todo, todo_id)
    if name := updateTodo.name:
        todo.name = name
    if done := updateTodo.done:
        todo.done = done
    session.commit()
    session.refresh(todo)
    return todo


@router.delete("{todo_id}")
def delete_todo_by_todo_id(
    todo_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    # or how can we run a delete query directly?
    todo = session.get_one(Todo, todo_id)
    session.delete(todo)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, content={"message": "Todo deleted"}
    )
