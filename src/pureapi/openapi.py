"""OpenAPI documentation support for PureAPI."""

import json
import inspect
from typing import Any, Dict, List, Optional, Type, get_type_hints, get_origin, get_args

SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{title} - Swagger UI</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({{
            url: "{openapi_url}",
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
            layout: "BaseLayout"
        }});
    </script>
</body>
</html>
"""

REDOC_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{title} - ReDoc</title>
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>body {{ margin: 0; padding: 0; }}</style>
</head>
<body>
    <redoc spec-url="{openapi_url}"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
</body>
</html>
"""

SCALAR_UI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{title} - API Reference</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            margin: 0;
        }}
    </style>
</head>
<body>
    <script
        id="api-reference"
        data-url="{openapi_url}"
        data-layout="{layout}"
        data-theme="{theme}"
    ></script>
    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
</body>
</html>
"""


def python_type_to_openapi(py_type: Type) -> Dict[str, Any]:
    """Convert Python type to OpenAPI schema."""
    if py_type is None or py_type is type(None):
        return {"type": "null"}
    
    origin = get_origin(py_type)
    args = get_args(py_type)
    
    if origin is list or py_type is list:
        item_type = args[0] if args else Any
        return {"type": "array", "items": python_type_to_openapi(item_type)}
    
    if origin is dict or py_type is dict:
        return {"type": "object"}
    
    type_map = {
        str: {"type": "string"},
        int: {"type": "integer"},
        float: {"type": "number"},
        bool: {"type": "boolean"},
        bytes: {"type": "string", "format": "binary"},
    }
    
    return type_map.get(py_type, {"type": "string"})


class OpenAPIGenerator:
    """Generate OpenAPI 3.0 specification."""
    
    def __init__(
        self,
        title: str = "PureAPI",
        version: str = "1.0.0",
        description: str = "",
        servers: Optional[List[Dict[str, str]]] = None
    ):
        self.title = title
        self.version = version
        self.description = description
        self.servers = servers or []
    
    def generate(self, routes: List) -> Dict[str, Any]:
        """Generate OpenAPI spec from routes."""
        spec = {
            "openapi": "3.0.3",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": self.description
            },
            "paths": {}
        }
        
        if self.servers:
            spec["servers"] = self.servers
        
        for route in routes:
            path = self._convert_path(route.path)
            if path not in spec["paths"]:
                spec["paths"][path] = {}
            
            for method in route.methods:
                if method == "ANY":
                    continue
                spec["paths"][path][method.lower()] = self._generate_operation(route)
        
        return spec
    
    def _convert_path(self, path: str) -> str:
        """Convert {param:type} to {param} for OpenAPI."""
        import re
        return re.sub(r"\{(\w+)(?::\w+)?\}", r"{\1}", path)
    
    def _generate_operation(self, route) -> Dict[str, Any]:
        """Generate operation object for a route."""
        operation: Dict[str, Any] = {
            "responses": {
                "200": {"description": "Successful response"}
            }
        }
        
        if route.summary:
            operation["summary"] = route.summary
        elif route.description:
            # Use first line of description as summary
            operation["summary"] = route.description.strip().split("\n")[0]
        
        if route.description:
            operation["description"] = route.description.strip()
        
        if route.tags:
            operation["tags"] = route.tags
        
        if route.deprecated:
            operation["deprecated"] = True
        
        operation["operationId"] = route.name
        
        # Path parameters
        if route.param_names:
            operation["parameters"] = []
            for param_name in route.param_names:
                param_type = route.path_params.get(param_name, str)
                operation["parameters"].append({
                    "name": param_name,
                    "in": "path",
                    "required": True,
                    "schema": python_type_to_openapi(param_type)
                })
        
        # Request body for POST/PUT/PATCH
        if any(m in route.methods for m in ["POST", "PUT", "PATCH"]):
            operation["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": {"type": "object"}
                    }
                }
            }
        
        return operation
    
    def get_swagger_ui_html(self, openapi_url: str) -> str:
        """Generate Swagger UI HTML page."""
        return SWAGGER_UI_HTML.format(title=self.title, openapi_url=openapi_url)
    
    def get_redoc_html(self, openapi_url: str) -> str:
        """Generate ReDoc HTML page."""
        return REDOC_HTML.format(title=self.title, openapi_url=openapi_url)

    def get_scalar_ui_html(
        self,
        openapi_url: str,
        layout: str = "modern",
        theme: str = "default"
    ) -> str:
        """Generate Scalar API Reference HTML page."""
        return SCALAR_UI_HTML.format(
            title=self.title,
            openapi_url=openapi_url,
            layout=layout,
            theme=theme
        )
