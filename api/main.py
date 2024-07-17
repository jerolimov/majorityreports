from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_cli.cli import main
from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlmodel import Session, select, func
from sqlalchemy.exc import NoResultFound
from src.db import init_db, engine
from src.todos import Todo
from src.todos import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    with Session(engine) as session:
        countStatement = select(func.count()).select_from(Todo)
        count = session.scalar(countStatement)
        if count == 0:
            session.add(Todo(name="todo a", done=False))
            session.add(Todo(name="todo b", done=False))
            session.add(Todo(name="todo c", done=False))
            session.add(Todo(name="done", done=True))
            session.commit()
    yield


app = FastAPI(
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(router, prefix="/todos")


@app.exception_handler(NoResultFound)
async def no_result_found_exception_handler(
    request: Request, exception: NoResultFound
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Resource not found: {exception}",
            "path": request.url.path,
        },
    )


if __name__ == "__main__":
    main()
