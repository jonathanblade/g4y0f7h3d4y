from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class BadRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.method.capitalize() in ["Post"]:
            content_type_header = request.headers.get("content-type")
            if not content_type_header:
                return JSONResponse(
                    content={"detail": "Missing request content type."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            if content_type_header not in ["application/json"]:
                return JSONResponse(
                    content={"detail": "Unsupported request content type."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        return await call_next(request)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            print(exc)
            return JSONResponse(
                content={"detail": "Internal server error."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
