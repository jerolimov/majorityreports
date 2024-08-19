import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException
from sqlalchemy.exc import NoResultFound, ArgumentError, IntegrityError
from pydantic import ValidationError


def add_exception_handler(app: FastAPI) -> None:
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

    @app.exception_handler(ArgumentError)
    async def argument_error_exception_handler(
        request: Request, exception: ArgumentError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Argument error: {exception}",
                "path": request.url.path,
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_exception_handler(
        request: Request, exception: IntegrityError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Integrity error: {exception}",
                "path": request.url.path,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_error_exception_handler(
        request: Request, exception: ValidationError
    ) -> JSONResponse:
        errors = json.loads(exception.json())
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Validation error: {exception}",
                "path": request.url.path,
                "validationErrorTitle": exception.title,
                "errors": errors,
            },
        )

    @app.exception_handler(ValidationException)
    async def fastapi_validation_exception_handler(
        request: Request, exception: ValidationException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Validation error: {exception}",
                "path": request.url.path,
                # "errors": exception.errors,
            },
        )
