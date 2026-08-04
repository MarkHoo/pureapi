"""Tests for PureAPI application."""

import unittest
import sys
import os
import json
from io import BytesIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pureapi import PureAPI, Request, Response, JSONResponse, HTTPException


def make_environ(method="GET", path="/", body=b"", content_type="", query_string=""):
    """Create a mock WSGI environ dict."""
    return {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "CONTENT_TYPE": content_type,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": BytesIO(body),
        "wsgi.url_scheme": "http",
        "HTTP_HOST": "localhost:8000",
    }


class TestPureAPI(unittest.TestCase):
    """Test PureAPI application."""
    
    def test_create_app(self):
        """Test creating application."""
        app = PureAPI(title="Test API", version="1.0.0")
        self.assertEqual(app.title, "Test API")
        self.assertEqual(app.version, "1.0.0")
    
    def test_simple_route(self):
        """Test simple route handling."""
        app = PureAPI()
        
        @app.get("/hello")
        def hello():
            return {"message": "Hello, World!"}
        
        environ = make_environ("GET", "/hello")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        body = b"".join(result)
        
        self.assertTrue(response_started[0][0].startswith("200"))
        data = json.loads(body)
        self.assertEqual(data["message"], "Hello, World!")
    
    def test_path_parameter(self):
        """Test route with path parameter."""
        app = PureAPI()
        
        @app.get("/users/{user_id:int}")
        def get_user(user_id: int):
            return {"user_id": user_id}
        
        environ = make_environ("GET", "/users/42")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        body = b"".join(result)
        
        data = json.loads(body)
        self.assertEqual(data["user_id"], 42)
    
    def test_not_found(self):
        """Test 404 response."""
        app = PureAPI()
        
        environ = make_environ("GET", "/nonexistent")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        
        self.assertTrue(response_started[0][0].startswith("404"))
    
    def test_method_not_allowed(self):
        """Test 405 response."""
        app = PureAPI()
        
        @app.get("/resource")
        def get_resource():
            return {}
        
        environ = make_environ("POST", "/resource")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        
        self.assertTrue(response_started[0][0].startswith("405"))
    
    def test_openapi_endpoint(self):
        """Test OpenAPI JSON endpoint."""
        app = PureAPI(title="Test API")
        
        @app.get("/items")
        def list_items():
            """List all items."""
            return []
        
        environ = make_environ("GET", "/openapi.json")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        body = b"".join(result)
        
        self.assertTrue(response_started[0][0].startswith("200"))
        spec = json.loads(body)
        self.assertEqual(spec["info"]["title"], "Test API")
        self.assertIn("/items", spec["paths"])
    
    def test_swagger_ui(self):
        """Test Swagger UI endpoint."""
        app = PureAPI()
        
        environ = make_environ("GET", "/swagger")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        body = b"".join(result)
        
        self.assertTrue(response_started[0][0].startswith("200"))
        self.assertIn(b"swagger-ui", body)

    def test_scalar_ui_default_docs(self):
        """Test Scalar UI default documentation endpoint."""
        app = PureAPI()

        environ = make_environ("GET", "/docs")
        response_started = []

        def start_response(status, headers):
            response_started.append((status, headers))

        result = app(environ, start_response)
        body = b"".join(result)

        self.assertTrue(response_started[0][0].startswith("200"))
        self.assertIn(b"@scalar/api-reference", body)
        self.assertIn(b'data-url="/openapi.json"', body)

    def test_scalar_ui_custom_url(self):
        """Test Scalar UI custom documentation endpoint."""
        app = PureAPI(docs_url=None, scalar_url="/reference")

        environ = make_environ("GET", "/reference")
        response_started = []

        def start_response(status, headers):
            response_started.append((status, headers))

        result = app(environ, start_response)
        body = b"".join(result)

        self.assertTrue(response_started[0][0].startswith("200"))
        self.assertIn(b"@scalar/api-reference", body)

    def test_docs_can_be_disabled(self):
        """Test default docs can be disabled without exposing Scalar."""
        app = PureAPI(docs_url=None, scalar_url=None, swagger_url=None, redoc_url=None)

        environ = make_environ("GET", "/docs")
        response_started = []

        def start_response(status, headers):
            response_started.append((status, headers))

        app(environ, start_response)

        self.assertTrue(response_started[0][0].startswith("404"))
    
    def test_redoc(self):
        """Test ReDoc endpoint."""
        app = PureAPI()
        
        environ = make_environ("GET", "/redoc")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        body = b"".join(result)
        
        self.assertTrue(response_started[0][0].startswith("200"))
        self.assertIn(b"redoc", body)
    
    def test_exception_handler(self):
        """Test custom exception handler."""
        app = PureAPI()
        
        @app.exception_handler(404)
        def custom_404(request, exc):
            return {"error": "Custom not found"}
        
        environ = make_environ("GET", "/nonexistent")
        response_started = []
        
        def start_response(status, headers):
            response_started.append((status, headers))
        
        result = app(environ, start_response)
        body = b"".join(result)
        
        data = json.loads(body)
        self.assertEqual(data["error"], "Custom not found")


class TestRequest(unittest.TestCase):
    """Test Request class."""
    
    def test_request_properties(self):
        """Test request properties."""
        environ = make_environ("POST", "/test", query_string="foo=bar")
        request = Request(environ)
        
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.path, "/test")
        self.assertEqual(request.query_params, {"foo": "bar"})
    
    def test_json_body(self):
        """Test JSON body parsing."""
        body = json.dumps({"key": "value"}).encode()
        environ = make_environ("POST", "/", body=body, content_type="application/json")
        request = Request(environ)
        
        self.assertEqual(request.json, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
