"""Tests for PureAPI routing system."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pureapi.routing import Router, Route
from pureapi.exceptions import NotFound, MethodNotAllowed


class TestRoute(unittest.TestCase):
    """Test Route class."""
    
    def test_simple_path(self):
        """Test simple path matching."""
        def handler(): pass
        route = Route("/users", handler, ["GET"])
        
        self.assertEqual(route.match("/users"), {})
        self.assertIsNone(route.match("/other"))
    
    def test_path_with_param(self):
        """Test path with parameter."""
        def handler(user_id): pass
        route = Route("/users/{user_id}", handler, ["GET"])
        
        result = route.match("/users/123")
        self.assertEqual(result, {"user_id": "123"})
        self.assertIsNone(route.match("/users"))
    
    def test_path_with_int_param(self):
        """Test path with typed int parameter."""
        def handler(id): pass
        route = Route("/items/{id:int}", handler, ["GET"])
        
        result = route.match("/items/42")
        self.assertEqual(result, {"id": 42})
        self.assertIsNone(route.match("/items/abc"))
    
    def test_path_with_multiple_params(self):
        """Test path with multiple parameters."""
        def handler(org, repo): pass
        route = Route("/orgs/{org}/repos/{repo}", handler, ["GET"])
        
        result = route.match("/orgs/acme/repos/api")
        self.assertEqual(result, {"org": "acme", "repo": "api"})


class TestRouter(unittest.TestCase):
    """Test Router class."""
    
    def test_add_route(self):
        """Test adding routes."""
        router = Router()
        
        def handler(): pass
        router.add_route("/test", handler, ["GET"])
        
        self.assertEqual(len(router.routes), 1)
    
    def test_route_decorator(self):
        """Test route decorator."""
        router = Router()
        
        @router.get("/hello")
        def hello():
            return "Hello"
        
        self.assertEqual(len(router.routes), 1)
        self.assertEqual(router.routes[0].path, "/hello")
    
    def test_match_route(self):
        """Test route matching."""
        router = Router()
        
        @router.get("/users/{id:int}")
        def get_user(id: int):
            return {"id": id}
        
        route, params = router.match("/users/123", "GET")
        self.assertEqual(params, {"id": 123})
    
    def test_match_not_found(self):
        """Test 404 for non-existent path."""
        router = Router()
        
        @router.get("/exists")
        def handler(): pass
        
        with self.assertRaises(NotFound):
            router.match("/not-exists", "GET")
    
    def test_match_method_not_allowed(self):
        """Test 405 for wrong method."""
        router = Router()
        
        @router.get("/resource")
        def handler(): pass
        
        with self.assertRaises(MethodNotAllowed):
            router.match("/resource", "POST")
    
    def test_http_methods(self):
        """Test different HTTP method decorators."""
        router = Router()
        
        @router.get("/resource")
        def get_resource(): pass
        
        @router.post("/resource")
        def create_resource(): pass
        
        @router.put("/resource/{id}")
        def update_resource(id): pass
        
        @router.delete("/resource/{id}")
        def delete_resource(id): pass
        
        self.assertEqual(len(router.routes), 4)
    
    def test_include_router(self):
        """Test including sub-router."""
        main_router = Router()
        sub_router = Router()
        
        @sub_router.get("/items")
        def list_items(): pass
        
        main_router.include_router(sub_router, prefix="/api/v1")
        
        route, _ = main_router.match("/api/v1/items", "GET")
        self.assertIsNotNone(route)


if __name__ == "__main__":
    unittest.main()
