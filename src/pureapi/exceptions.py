"""HTTP exceptions for PureAPI."""

from typing import Any, Dict, Optional


class HTTPException(Exception):
    """Base HTTP exception with status code and detail."""
    
    def __init__(
        self,
        status_code: int = 500,
        detail: str = "Internal Server Error",
        headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers or {}
        super().__init__(detail)


class BadRequest(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(400, detail)


class Unauthorized(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(401, detail)


class Forbidden(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(403, detail)


class NotFound(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(404, detail)


class MethodNotAllowed(HTTPException):
    def __init__(self, detail: str = "Method Not Allowed", allowed: str = ""):
        super().__init__(405, detail, {"Allow": allowed} if allowed else None)


class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(500, detail)
