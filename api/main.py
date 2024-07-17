from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi_cli.cli import main
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from typing import AsyncIterator, Iterable
from db import init_db, get_session, Todo


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/todos")
def create_todo(newTodo: Todo, session: Session = Depends(get_session)) -> Todo:
    todo = Todo()
    todo.name = newTodo.name
    if isinstance(newTodo.done, bool):
        todo.done = newTodo.done
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todos")
def get_todos(session: Session = Depends(get_session)) -> Iterable[Todo]:
    statement = select(Todo)
    return session.exec(statement).all()


@app.get("/todos/{todo_id}")
def get_todo_by_todo_id(todo_id: int, session: Session = Depends(get_session)) -> Todo:
    todo = session.get_one(Todo, todo_id)
    return todo


@app.put("/todos/{todo_id}")
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


@app.delete("/todos/{todo_id}")
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


@app.exception_handler(NoResultFound)
async def no_result_found_exception_handler(request: Request, exception: NoResultFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Resource not found: {exception}",
            "path": request.url.path,
        },
    )


if __name__ == "__main__":
    main()
