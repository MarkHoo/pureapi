"""Routing system for PureAPI with type annotations support."""

import re
import inspect
from typing import Any, Callable, Dict, List, Optional, Pattern, Tuple, Type, get_type_hints
from .exceptions import NotFound, MethodNotAllowed


class Route:
    """A single route definition."""
    
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str],
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        response_model: Optional[Type] = None,
        deprecated: bool = False
    ):
        self.path = path
        self.endpoint = endpoint
        self.methods = [m.upper() for m in methods]
        self.name = name or endpoint.__name__
        self.summary = summary
        self.description = description or endpoint.__doc__
        self.tags = tags or []
        self.response_model = response_model
        self.deprecated = deprecated
        
        # Parse path parameters
        self.path_params: Dict[str, Type] = {}
        self.pattern, self.param_names = self._compile_path(path)
        
        # Extract type hints from endpoint
        try:
            self.type_hints = get_type_hints(endpoint)
        except Exception:
            self.type_hints = {}
    
    def _compile_path(self, path: str) -> Tuple[Pattern, List[str]]:
        """Convert path with {param} or {param:type} to regex pattern."""
        param_names = []
        pattern = "^"
        last_end = 0
        
        # Match {name} or {name:type}
        for match in re.finditer(r"\{(\w+)(?::(\w+))?\}", path):
            param_name = match.group(1)
            param_type = match.group(2) or "str"
            param_names.append(param_name)
            
            # Add literal part before this param
            pattern += re.escape(path[last_end:match.start()])
            
            # Add param pattern based on type
            if param_type == "int":
                pattern += r"(?P<" + param_name + r">\d+)"
                self.path_params[param_name] = int
            elif param_type == "float":
                pattern += r"(?P<" + param_name + r">[\d.]+)"
                self.path_params[param_name] = float
            elif param_type == "path":
                pattern += r"(?P<" + param_name + r">.+)"
                self.path_params[param_name] = str
            else:
                pattern += r"(?P<" + param_name + r">[^/]+)"
                self.path_params[param_name] = str
            
            last_end = match.end()
        
        pattern += re.escape(path[last_end:]) + "$"
        return re.compile(pattern), param_names
    
    def match(self, path: str) -> Optional[Dict[str, Any]]:
        """Match path and extract parameters."""
        m = self.pattern.match(path)
        if not m:
            return None
        
        params = m.groupdict()
        # Convert types
        for name, value in params.items():
            converter = self.path_params.get(name, str)
            try:
                params[name] = converter(value)
            except (ValueError, TypeError):
                return None
        return params


class Router:
    """Route collection and matching."""
    
    def __init__(self, prefix: str = ""):
        self.prefix = prefix.rstrip("/")
        self.routes: List[Route] = []
    
    def add_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str],
        **kwargs
    ) -> Route:
        """Add a route to the router."""
        full_path = self.prefix + path
        route = Route(full_path, endpoint, methods, **kwargs)
        self.routes.append(route)
        return route
    
    def route(
        self,
        path: str,
        methods: List[str] = None,
        **kwargs
    ) -> Callable:
        """Decorator to register a route."""
        methods = methods or ["GET"]
        
        def decorator(func: Callable) -> Callable:
            self.add_route(path, func, methods, **kwargs)
            return func
        return decorator
    
    def get(self, path: str, **kwargs) -> Callable:
        """Register GET route."""
        return self.route(path, methods=["GET"], **kwargs)
    
    def post(self, path: str, **kwargs) -> Callable:
        """Register POST route."""
        return self.route(path, methods=["POST"], **kwargs)
    
    def put(self, path: str, **kwargs) -> Callable:
        """Register PUT route."""
        return self.route(path, methods=["PUT"], **kwargs)
    
    def delete(self, path: str, **kwargs) -> Callable:
        """Register DELETE route."""
        return self.route(path, methods=["DELETE"], **kwargs)
    
    def patch(self, path: str, **kwargs) -> Callable:
        """Register PATCH route."""
        return self.route(path, methods=["PATCH"], **kwargs)
    
    def match(self, path: str, method: str) -> Tuple[Route, Dict[str, Any]]:
        """Find matching route for path and method."""
        method = method.upper()
        matched_routes = []
        
        for route in self.routes:
            params = route.match(path)
            if params is not None:
                matched_routes.append((route, params))
        
        if not matched_routes:
            raise NotFound(f"Path not found: {path}")
        
        # Check method
        for route, params in matched_routes:
            if method in route.methods or "ANY" in route.methods:
                return route, params
        
        # Method not allowed
        allowed = set()
        for route, _ in matched_routes:
            allowed.update(route.methods)
        raise MethodNotAllowed(allowed=", ".join(sorted(allowed)))
    
    def include_router(self, router: "Router", prefix: str = "") -> None:
        """Include routes from another router."""
        for route in router.routes:
            new_path = prefix + route.path
            self.add_route(
                new_path,
                route.endpoint,
                route.methods,
                name=route.name,
                summary=route.summary,
                description=route.description,
                tags=route.tags,
                response_model=route.response_model,
                deprecated=route.deprecated
            )
