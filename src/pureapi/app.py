"""Main PureAPI application class."""

import json
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union
from wsgiref.simple_server import make_server

from .request import Request
from .response import Response, JSONResponse, HTMLResponse
from .routing import Router, Route
from .exceptions import HTTPException, NotFound
from .openapi import OpenAPIGenerator


class PureAPI(Router):
    """PureAPI application - a lightweight Python web framework."""
    
    def __init__(
        self,
        title: str = "PureAPI",
        version: str = "1.0.0",
        description: str = "",
        docs_url: Optional[str] = "/docs",
        swagger_url: Optional[str] = "/swagger",
        redoc_url: Optional[str] = "/redoc",
        scalar_url: Optional[str] = None,
        scalar_layout: str = "modern",
        scalar_theme: str = "default",
        openapi_url: str = "/openapi.json",
        debug: bool = False
    ):
        super().__init__()
        self.title = title
        self.version = version
        self.description = description
        self.docs_url = docs_url
        self.swagger_url = swagger_url
        self.redoc_url = redoc_url
        self.scalar_url = scalar_url
        self.scalar_layout = scalar_layout
        self.scalar_theme = scalar_theme
        self.openapi_url = openapi_url
        self.debug = debug
        
        self._openapi_generator = OpenAPIGenerator(
            title=title,
            version=version,
            description=description
        )
        
        self._exception_handlers: Dict[int, Callable] = {}
        self._middleware: List[Callable] = []
        
        # Register OpenAPI routes
        self._setup_openapi_routes()
    
    def _setup_openapi_routes(self) -> None:
        """Setup OpenAPI documentation routes."""
        if self.openapi_url:
            @self.get(self.openapi_url, tags=["documentation"])
            def openapi_schema():
                """OpenAPI JSON schema."""
                return self._openapi_generator.generate(self.routes)
        
        if self.docs_url:
            @self.get(self.docs_url, tags=["documentation"])
            def scalar_docs():
                """Scalar API Reference documentation."""
                html = self._openapi_generator.get_scalar_ui_html(
                    self.openapi_url,
                    layout=self.scalar_layout,
                    theme=self.scalar_theme
                )
                return HTMLResponse(html)

        if self.swagger_url:
            @self.get(self.swagger_url, tags=["documentation"])
            def swagger_ui():
                """Swagger UI documentation."""
                html = self._openapi_generator.get_swagger_ui_html(self.openapi_url)
                return HTMLResponse(html)
        
        if self.redoc_url:
            @self.get(self.redoc_url, tags=["documentation"])
            def redoc():
                """ReDoc documentation."""
                html = self._openapi_generator.get_redoc_html(self.openapi_url)
                return HTMLResponse(html)

        if self.scalar_url and self.scalar_url != self.docs_url:
            @self.get(self.scalar_url, tags=["documentation"])
            def scalar_ui():
                """Scalar API Reference documentation."""
                html = self._openapi_generator.get_scalar_ui_html(
                    self.openapi_url,
                    layout=self.scalar_layout,
                    theme=self.scalar_theme
                )
                return HTMLResponse(html)
    
    def exception_handler(self, status_code: int) -> Callable:
        """Register an exception handler for a status code."""
        def decorator(func: Callable) -> Callable:
            self._exception_handlers[status_code] = func
            return func
        return decorator
    
    def add_middleware(self, middleware: Callable) -> None:
        """Add middleware to the application."""
        self._middleware.append(middleware)
    
    def _handle_exception(self, exc: HTTPException, request: Request) -> Response:
        """Handle HTTP exceptions."""
        handler = self._exception_handlers.get(exc.status_code)
        if handler:
            result = handler(request, exc)
            return self._make_response(result)
        
        return JSONResponse(
            {"detail": exc.detail},
            status_code=exc.status_code
        )
    
    def _make_response(self, result: Any) -> Response:
        """Convert handler result to Response object."""
        if isinstance(result, Response):
            return result
        if isinstance(result, dict):
            return JSONResponse(result)
        if isinstance(result, str):
            return Response(result)
        if result is None:
            return Response("")
        return JSONResponse(result)
    
    def _call_endpoint(self, route: Route, request: Request, path_params: Dict[str, Any]) -> Any:
        """Call route endpoint with appropriate arguments."""
        sig = inspect.signature(route.endpoint)
        kwargs = {}
        
        for param_name, param in sig.parameters.items():
            if param_name in path_params:
                kwargs[param_name] = path_params[param_name]
            elif param.annotation is Request or param_name == "request":
                kwargs[param_name] = request
        
        return route.endpoint(**kwargs)
    
    def __call__(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """WSGI application interface."""
        request = Request(environ)
        
        try:
            route, path_params = self.match(request.path, request.method)
            result = self._call_endpoint(route, request, path_params)
            response = self._make_response(result)
        except HTTPException as exc:
            response = self._handle_exception(exc, request)
        except Exception as exc:
            if self.debug:
                import traceback
                detail = traceback.format_exc()
            else:
                detail = "Internal Server Error"
            response = JSONResponse({"detail": detail}, status_code=500)
        
        start_response(response.status, response.headers)
        return [response.body]
    
    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        debug: Optional[bool] = None
    ) -> None:
        """Run the development server."""
        if debug is not None:
            self.debug = debug
        
        print(f"PureAPI v{self.version} running on http://{host}:{port}")
        if self.docs_url:
            print(f"Documentation: http://{host}:{port}{self.docs_url}")
        print("Press Ctrl+C to quit")
        
        server = make_server(host, port, self)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            server.shutdown()
