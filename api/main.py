import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_cli.cli import main
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any
from sqlalchemy.exc import NoResultFound

from src.db import init_db
from src.testdata import init_testdata
from src.api import router as apiRouter


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
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