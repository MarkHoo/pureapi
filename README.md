# PureAPI

[![PyPI version](https://img.shields.io/pypi/v/pureapi.svg)](https://pypi.org/project/pureapi/)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/pureapi.svg)](https://pypi.org/project/pureapi/)
[![Documentation Status](https://readthedocs.org/projects/pureapi/badge/?version=latest)](https://pureapi.readthedocs.io/)
[![License](https://img.shields.io/pypi/l/pureapi.svg)](LICENSE)
[![Package status](https://img.shields.io/pypi/status/pureapi.svg)](https://pypi.org/project/pureapi/)
<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">简体中文</a>
</p>

PureAPI is a lightweight, intuitive, zero-runtime-dependency Python web API framework.

## Features

- Typed routing with automatic conversion, such as `/users/{user_id:int}`.
- Standard WSGI application interface.
- Automatic JSON responses for `dict` and `list` return values.
- Request object with query parameters, headers, body, JSON, form data, and URL helpers.
- Built-in OpenAPI generation at `/openapi.json`.
- Built-in API documentation with Scalar API Reference by default, plus Swagger UI and ReDoc.
- Zero runtime dependencies in the core framework.

## Requirements

PureAPI supports Python 3.11 and newer.

## Installation

Install from PyPI:

```bash
pip install pureapi
```

Install for local development:

```bash
git clone https://github.com/MarkHoo/pureapi.git
cd pureapi
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
python -m pytest
```

## Quick Start

Create `app.py`:

```python
from pureapi import PureAPI, Request, HTTPException

app = PureAPI(
    title="Task API",
    version="1.0.0",
    description="A small task management API built with PureAPI.",
)

tasks = {
    1: {"id": 1, "title": "Write documentation", "done": False},
}


@app.get("/", summary="API home", tags=["system"])
def home():
    """Return basic service information."""
    return {
        "name": "Task API",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/tasks", summary="List tasks", tags=["tasks"])
def list_tasks():
    """Return all tasks."""
    return {"items": list(tasks.values()), "count": len(tasks)}


@app.get("/tasks/{task_id:int}", summary="Get task", tags=["tasks"])
def get_task(task_id: int):
    """Return one task by ID."""
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", summary="Create task", tags=["tasks"])
def create_task(request: Request):
    """Create a task from a JSON request body."""
    data = request.json or {}
    title = str(data.get("title", "")).strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    task_id = max(tasks.keys(), default=0) + 1
    task = {"id": task_id, "title": title, "done": False}
    tasks[task_id] = task
    return task


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
```

Start the application:

```bash
python app.py
```

Open:

- API home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Scalar docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Swagger UI: [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## Documentation Routes

PureAPI registers documentation routes automatically:

| Path | Description |
| --- | --- |
| `/docs` | Scalar API Reference, the default documentation UI |
| `/swagger` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI 3.0 JSON |

Customize them when creating the app:

```python
app = PureAPI(
    title="My API",
    version="1.0.0",
    docs_url="/docs",
    scalar_url="/reference",
    swagger_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)
```

## Production

Run with Gunicorn:

```bash
gunicorn myapp:app -w 4 -b 0.0.0.0:8000
```

Run with uWSGI:

```bash
uwsgi --http :8000 --wsgi-file myapp.py --callable app
```

## License

PureAPI is released under the MIT License. See [LICENSE](LICENSE).
