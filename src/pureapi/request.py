"""Request handling for PureAPI."""

import json
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, unquote


class Request:
    """HTTP Request wrapper for WSGI environ."""
    
    def __init__(self, environ: Dict[str, Any]):
        self.environ = environ
        self._body: Optional[bytes] = None
        self._json: Optional[Any] = None
        
    @property
    def method(self) -> str:
        return self.environ.get("REQUEST_METHOD", "GET").upper()
    
    @property
    def path(self) -> str:
        return "/" + self.environ.get("PATH_INFO", "").lstrip("/")
    
    @property
    def query_string(self) -> str:
        return self.environ.get("QUERY_STRING", "")
    
    @property
    def query_params(self) -> Dict[str, str]:
        """Parse query string into dict (single values only)."""
        params = parse_qs(self.query_string)
        return {k: v[0] for k, v in params.items()}
    
    @property
    def headers(self) -> Dict[str, str]:
        """Extract HTTP headers from environ."""
        headers = {}
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                header_name = key[5:].replace("_", "-").title()
                headers[header_name] = value
            elif key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                header_name = key.replace("_", "-").title()
                headers[header_name] = value
        return headers
    
    @property
    def content_type(self) -> str:
        return self.environ.get("CONTENT_TYPE", "")
    
    @property
    def content_length(self) -> int:
        try:
            return int(self.environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            return 0
    
    @property
    def body(self) -> bytes:
        """Read request body."""
        if self._body is None:
            try:
                length = self.content_length
                self._body = self.environ["wsgi.input"].read(length) if length > 0 else b""
            except Exception:
                self._body = b""
        return self._body
    
    @property
    def json(self) -> Any:
        """Parse JSON body."""
        if self._json is None:
            if "application/json" in self.content_type:
                try:
                    self._json = json.loads(self.body.decode("utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    self._json = None
        return self._json
    
    @property
    def form(self) -> Dict[str, str]:
        """Parse form data."""
        if "application/x-www-form-urlencoded" in self.content_type:
            params = parse_qs(self.body.decode("utf-8"))
            return {k: v[0] for k, v in params.items()}
        return {}
    
    @property
    def host(self) -> str:
        return self.environ.get("HTTP_HOST", "")
    
    @property
    def scheme(self) -> str:
        return self.environ.get("wsgi.url_scheme", "http")
    
    @property
    def url(self) -> str:
        """Full request URL."""
        url = f"{self.scheme}://{self.host}{self.path}"
        if self.query_string:
            url += f"?{self.query_string}"
        return url
