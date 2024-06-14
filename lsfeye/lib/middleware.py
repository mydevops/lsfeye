import time
from typing import Any

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from lsfeye.lib import exceptions
from lsfeye.lib import util


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Any:
        start_time = time.time()
        response = await call_next(request)
        if (
            request.url.path != "/healthcheck"
            and "form-data" not in request.headers.get("content-type", "")
        ):
            logger.info(
                f"response: Method {request.method} - {request.url.path} - "
                f"code: {response.status_code} "
                f"{(time.time() - start_time) * 1000:.2f}ms"
            )
        return response


class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            if not isinstance(e, exceptions.IgnoreException):
                logger.exception(e)
            return ORJSONResponse(util.make_response_not_ok(str(e)))


def register(app: FastAPI) -> Any:
    app.add_middleware(ResponseTimeMiddleware)
    app.add_middleware(CatchExceptionsMiddleware)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Any, exc: Any) -> ORJSONResponse:
        return ORJSONResponse(util.make_response_not_ok(str(exc.errors())))

    @app.exception_handler(404)
    async def custom_404_handler(request: Request, _: Any) -> ORJSONResponse:
        return ORJSONResponse(
            util.make_response_not_ok(f"[{request.url.path}] Not Found"),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @app.exception_handler(405)
    async def custom_405_handler(request: Request, _: Any) -> ORJSONResponse:
        return ORJSONResponse(
            util.make_response_not_ok(
                f"{request.method} [{request.url.path}] Method Not Allowed"
            ),
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
