"""Example PureAPI application."""

import sys
sys.path.insert(0, 'src')

from pureapi import PureAPI, Request, HTTPException

# Create application
app = PureAPI(
    title="PureAPI Example",
    version="1.0.0",
    description="A simple example API built with PureAPI"
)

# Sample data
users = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}


@app.get("/", summary="Root endpoint", tags=["general"])
def root():
    """Welcome to PureAPI!"""
    return {"message": "Welcome to PureAPI!", "docs": "/docs"}


@app.get("/users", summary="List all users", tags=["users"])
def list_users():
    """Get a list of all users."""
    return list(users.values())


@app.get("/users/{user_id:int}", summary="Get user by ID", tags=["users"])
def get_user(user_id: int):
    """Get a specific user by their ID."""
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return users[user_id]


@app.post("/users", summary="Create a new user", tags=["users"])
def create_user(request: Request):
    """Create a new user with the provided data."""
    data = request.json
    if not data:
        raise HTTPException(status_code=400, detail="Request body required")
    
    new_id = max(users.keys()) + 1 if users else 1
    user = {"id": new_id, **data}
    users[new_id] = user
    return user


@app.put("/users/{user_id:int}", summary="Update user", tags=["users"])
def update_user(user_id: int, request: Request):
    """Update an existing user."""
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    data = request.json
    users[user_id].update(data)
    return users[user_id]


@app.delete("/users/{user_id:int}", summary="Delete user", tags=["users"])
def delete_user(user_id: int):
    """Delete a user by ID."""
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    deleted = users.pop(user_id)
    return {"deleted": True, "user": deleted}


@app.get("/health", summary="Health check", tags=["general"])
def health_check():
    """Check if the API is running."""
    return {"status": "healthy"}


# Custom 404 handler
@app.exception_handler(404)
def custom_not_found(request: Request, exc: HTTPException):
    return {
        "error": "Not Found",
        "detail": exc.detail,
        "path": request.path
    }


if __name__ == "__main__":
    print("Starting PureAPI Example...")
    print("Visit http://127.0.0.1:8000/docs for Scalar API Reference")
    print("Visit http://127.0.0.1:8000/swagger for Swagger UI")
    print("Visit http://127.0.0.1:8000/redoc for ReDoc")
    app.run(debug=True)
