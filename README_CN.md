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

PureAPI 是一个轻量、直观、零运行时依赖的 Python Web API 框架。

## 特性

- 类型化路由：支持 `/users/{user_id:int}` 这类路径参数，并自动完成类型转换。
- 标准 WSGI：可直接作为 WSGI 应用运行，也可配合 Gunicorn、uWSGI 等服务器部署。
- 自动 JSON 响应：返回 `dict`、`list` 等对象时自动序列化为 JSON。
- 请求对象：提供 query、headers、body、json、form 等常用请求数据。
- 内置 OpenAPI：自动生成 `/openapi.json`。
- 内置接口文档：默认使用 Scalar API Reference，同时保留 Swagger UI 和 ReDoc。
- 零运行时依赖：核心框架只使用 Python 标准库。

## 环境要求

PureAPI 支持 Python 3.11 及以上版本。

## 安装

从 PyPI 安装：

```bash
pip install pureapi
```

开发环境安装：

```bash
git clone https://github.com/MarkHoo/pureapi.git
cd pureapi
python -m pip install -e ".[dev]"
```

运行测试：

```bash
python -m pytest
```

## 快速开始

创建 `app.py`：

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

启动服务：

```bash
python app.py
```

访问：

- API 首页: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Scalar 文档: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Swagger UI: [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## 路由

### 基础路由

```python
@app.get("/users")
def list_users():
    return []
```

### 路径参数

PureAPI 使用 `{name}` 定义路径参数：

```python
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}
```

支持的路径参数类型：

| 写法 | Python 类型 | 说明 |
| --- | --- | --- |
| `{name}` | `str` | 默认字符串参数 |
| `{id:int}` | `int` | 整数参数 |
| `{price:float}` | `float` | 浮点数参数 |
| `{filepath:path}` | `str` | 匹配多级路径 |

示例：

```python
@app.get("/users/{user_id:int}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### HTTP 方法

```python
@app.get("/items")
def list_items():
    return []


@app.post("/items")
def create_item():
    return {"created": True}


@app.put("/items/{item_id:int}")
def replace_item(item_id: int):
    return {"replaced": item_id}


@app.patch("/items/{item_id:int}")
def update_item(item_id: int):
    return {"updated": item_id}


@app.delete("/items/{item_id:int}")
def delete_item(item_id: int):
    return {"deleted": item_id}
```

## 请求处理

通过在处理函数中声明 `request` 参数获取请求对象：

```python
from pureapi import Request


@app.post("/orders")
def create_order(request: Request):
    payload = request.json
    query = request.query_params
    headers = request.headers
    return {
        "payload": payload,
        "query": query,
        "user_agent": headers.get("User-Agent"),
    }
```

常用属性：

| 属性 | 说明 |
| --- | --- |
| `request.method` | HTTP 方法 |
| `request.path` | 请求路径 |
| `request.query_string` | 原始查询字符串 |
| `request.query_params` | 解析后的查询参数 |
| `request.headers` | 请求头 |
| `request.body` | 原始请求体 bytes |
| `request.json` | JSON 请求体 |
| `request.form` | 表单请求体 |
| `request.content_type` | Content-Type |
| `request.url` | 完整请求 URL |

## 响应

返回 `dict` 或 `list` 会自动生成 JSON 响应：

```python
@app.get("/profile")
def profile():
    return {"name": "PureAPI"}
```

也可以显式返回响应对象：

```python
from pureapi import Response, JSONResponse, HTMLResponse


@app.get("/plain")
def plain_text():
    return Response("Hello PureAPI")


@app.get("/json")
def json_data():
    return JSONResponse({"ok": True}, status_code=201)


@app.get("/html")
def html_page():
    return HTMLResponse("<h1>Hello PureAPI</h1>")
```

## 错误处理

抛出 `HTTPException`：

```python
from pureapi import HTTPException


@app.get("/items/{item_id:int}")
def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="item_id must be positive")
    return {"item_id": item_id}
```

注册自定义错误处理器：

```python
@app.exception_handler(404)
def not_found(request, exc):
    return {
        "error": "not_found",
        "detail": exc.detail,
        "path": request.path,
    }
```

## 子路由

使用 `Router` 组织模块化接口：

```python
from pureapi import PureAPI, Router

app = PureAPI()
api_router = Router()


@api_router.get("/users")
def list_users():
    return []


app.include_router(api_router, prefix="/api/v1")
```

最终路由：

```text
/api/v1/users
```

## OpenAPI 和接口文档

PureAPI 会自动注册文档路由：

| 路径 | 说明 |
| --- | --- |
| `/docs` | Scalar API Reference，默认文档页 |
| `/swagger` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI 3.0 JSON |

可以通过路由元数据增强文档展示：

```python
@app.get(
    "/reports",
    summary="List reports",
    description="Return all reports visible to the current user.",
    tags=["reports"],
    deprecated=False,
)
def list_reports():
    return []
```

自定义文档地址：

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

关闭某个文档入口：

```python
app = PureAPI(
    docs_url=None,
    swagger_url=None,
    redoc_url=None,
)
```

## 生产部署

### Gunicorn

```bash
gunicorn myapp:app -w 4 -b 0.0.0.0:8000
```

### uWSGI

```bash
uwsgi --http :8000 --wsgi-file myapp.py --callable app
```

## 开发和发布

安装开发依赖：

```bash
python -m pip install -e ".[dev]"
```

运行测试：

```bash
python -m pytest
```

更多贡献约定请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。版本变化请查看 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

PureAPI 使用 MIT License。详见 [LICENSE](LICENSE)。
