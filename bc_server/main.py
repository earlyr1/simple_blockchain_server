import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from bc_server.models import ErrorResponse
from bc_server.routers import main_router
from bc_server.settings import settings


def get_app() -> FastAPI:
    def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error=f"Wasn't able to validate your message: {exc}"
            ).dict(),
        )

    _app = FastAPI(
        title="Blockchain API",
        version="0.0.1",
        description="A service fetching some info from blockchains",
        docs_url=f"/docs",
        exception_handlers={
            RequestValidationError: validation_exception_handler,
            ValidationError: validation_exception_handler,
        },
    )

    _app.include_router(main_router)
    return _app


app = get_app()


def main() -> None:
    uvicorn.run(app=app, host=settings.HOST, port=settings.PORT, log_level="info")


if __name__ == "__main__":
    main()
