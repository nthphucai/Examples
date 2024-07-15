import os
import sys
from pathlib import Path
from typing import Callable

import uvicorn
from loguru import logger
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from api.routes.router import router as api_router
from api.routes import limiter
from exceptions import (
    AuthenticationFailed,
    ServiceError,
    TypingError,
    ProjectApiError,
)

sys.path.append(Path(__file__).parent.absolute().as_posix())

PORT = os.getenv("PORT")


def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, ProjectApiError], JSONResponse]:
    detail = {"message": initial_detail}  # Using a dictionary to hold the detail

    async def exception_handler(_: Request, exc: ProjectApiError) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        logger.error(exc)
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler


def get_app() -> FastAPI:
    app = FastAPI(
        title="RestAPI Scaffold",
        description="Scaffold for APIs Testing",
        openapi_url="/openapi.json",
    )

    # This middleware enables allow all cross-domain requests to the API from a browser.
    # For production deployments, it could be made more restrictive.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_exception_handler(
        exc_class_or_status_code=TypingError,
        handler=create_exception_handler(
            status.HTTP_400_BAD_REQUEST, "Can't perform the operation."
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=AuthenticationFailed,
        handler=create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            "Authentication failed due to invalid credentials.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=ServiceError,
        handler=create_exception_handler(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "A service seems to be down, try again later.",
        ),
    )

    app.include_router(api_router)
    return app


app = get_app()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API")


if __name__ == "__main__":
    # In production, don't forget to change reload => False, debug => False
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True)
