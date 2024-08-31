import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_cli.cli import main
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any

from src.config import read_config
from src.db import init_db
from src.testdata import init_testdata
from src.router import router as apiRouter
from src.shared.exceptions import add_exception_handler


config = read_config()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    if config.db.create_testdata:
        init_testdata()
    yield


class CustomJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
        ).encode("utf-8")


app = FastAPI(
    docs_url="/",
    lifespan=lifespan,
    default_response_class=CustomJSONResponse,
)

app.include_router(apiRouter, prefix="/api")

add_exception_handler(app)

if __name__ == "__main__":
    main()
