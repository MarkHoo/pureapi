"""Response handling for PureAPI."""

import json
from typing import Any, Dict, List, Optional, Tuple, Union

HTTP_STATUS = {
    200: "OK", 201: "Created", 204: "No Content",
    301: "Moved Permanently", 302: "Found", 304: "Not Modified",
    400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
    404: "Not Found", 405: "Method Not Allowed", 422: "Unprocessable Entity",
    500: "Internal Server Error", 502: "Bad Gateway", 503: "Service Unavailable"
}


class Response:
    """HTTP Response object."""
    
    def __init__(
        self,
        content: Union[str, bytes] = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        content_type: str = "text/plain; charset=utf-8"
    ):
        self.status_code = status_code
        self._headers: Dict[str, str] = headers or {}
        self._headers.setdefault("Content-Type", content_type)
        
        if isinstance(content, str):
            self.body = content.encode("utf-8")
        else:
            self.body = content
    
    @property
    def status(self) -> str:
        phrase = HTTP_STATUS.get(self.status_code, "Unknown")
        return f"{self.status_code} {phrase}"
    
    @property
    def headers(self) -> List[Tuple[str, str]]:
        return list(self._headers.items())
    
    def set_header(self, name: str, value: str) -> None:
        self._headers[name] = value
    
    def set_cookie(
        self,
        name: str,
        value: str,
        max_age: Optional[int] = None,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Optional[str] = None
    ) -> None:
        cookie = f"{name}={value}; Path={path}"
        if max_age is not None:
            cookie += f"; Max-Age={max_age}"
        if domain:
            cookie += f"; Domain={domain}"
        if secure:
            cookie += "; Secure"
        if httponly:
            cookie += "; HttpOnly"
        if samesite:
            cookie += f"; SameSite={samesite}"
        self._headers["Set-Cookie"] = cookie


class JSONResponse(Response):
    """JSON response with automatic serialization."""
    
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        body = json.dumps(content, ensure_ascii=False) if content is not None else "{}"
        super().__init__(
            content=body,
            status_code=status_code,
            headers=headers,
            content_type="application/json; charset=utf-8"
        )


class HTMLResponse(Response):
    """HTML response."""
    
    def __init__(
        self,
        content: str = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            content_type="text/html; charset=utf-8"
        )


class RedirectResponse(Response):
    """HTTP redirect response."""
    
    def __init__(self, url: str, status_code: int = 302):
        super().__init__(content="", status_code=status_code)
        self.set_header("Location", url)
