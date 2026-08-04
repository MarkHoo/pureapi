# PureAPI 使用文档

PureAPI 是一个轻量级 Python Web API 框架，目标是用尽可能少的概念完成常见 API 开发工作。它适合小型 REST API、内部系统、教学项目、原型服务和依赖敏感的工具型项目。

## 目录

- [安装](#安装)
- [创建应用](#创建应用)
- [路由](#路由)
- [请求对象](#请求对象)
- [响应对象](#响应对象)
- [错误处理](#错误处理)
- [子路由](#子路由)
- [OpenAPI 和 Scalar 文档](#openapi-和-scalar-文档)
- [完整 CRUD 示例](#完整-crud-示例)
- [生产部署](#生产部署)
- [开发者工作流](#开发者工作流)

## 安装

```bash
pip install pureapi
```

PureAPI 支持 Python 3.11 及以上版本：

- Python 3.11
- Python 3.12
- Python 3.13
- Python 3.14

## 创建应用

```python
from pureapi import PureAPI

app = PureAPI(
    title="Example API",
    version="1.0.0",
    description="An API built with PureAPI.",
)


@app.get("/")
def home():
    return {"message": "Hello PureAPI"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
```

启动：

```bash
python app.py
```

## 路由

PureAPI 使用装饰器注册路由。

```python
@app.get("/users")
def list_users():
    return []


@app.post("/users")
def create_user():
    return {"created": True}
```

支持的方法：

- `get`
- `post`
- `put`
- `patch`
- `delete`
- `route`

### 路径参数

```python
@app.get("/users/{user_id:int}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

参数类型：

| 路由写法 | 转换类型 | 示例 |
| --- | --- | --- |
| `{name}` | `str` | `/users/alice` |
| `{id:int}` | `int` | `/users/1` |
| `{price:float}` | `float` | `/prices/19.9` |
| `{file:path}` | `str` | `/files/a/b/c.txt` |

如果类型转换失败，路由不会匹配。

### 路由元数据

路由元数据会进入 OpenAPI，并显示在 Scalar、Swagger UI 和 ReDoc 中：

```python
@app.get(
    "/users",
    summary="List users",
    description="Return all users in the system.",
    tags=["users"],
)
def list_users():
    return []
```

## 请求对象

处理函数中声明 `request` 参数即可获取请求对象：

```python
from pureapi import Request


@app.post("/messages")
def create_message(request: Request):
    data = request.json
    return {"received": data}
```

常用属性：

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `request.method` | `str` | HTTP 方法 |
| `request.path` | `str` | 请求路径 |
| `request.query_string` | `str` | 原始查询字符串 |
| `request.query_params` | `dict[str, str]` | 查询参数 |
| `request.headers` | `dict[str, str]` | 请求头 |
| `request.body` | `bytes` | 原始请求体 |
| `request.json` | `Any` | JSON 请求体 |
| `request.form` | `dict[str, str]` | 表单请求体 |
| `request.content_type` | `str` | Content-Type |
| `request.url` | `str` | 完整 URL |

### 查询参数

```python
@app.get("/search")
def search(request: Request):
    keyword = request.query_params.get("q", "")
    return {"keyword": keyword}
```

请求：

```text
GET /search?q=pureapi
```

### JSON 请求体

```python
@app.post("/users")
def create_user(request: Request):
    data = request.json or {}
    return {"name": data.get("name")}
```

## 响应对象

### 自动 JSON 响应

```python
@app.get("/status")
def status():
    return {"status": "ok"}
```

### 显式响应

```python
from pureapi import Response, JSONResponse, HTMLResponse


@app.get("/plain")
def plain():
    return Response("plain text")


@app.get("/created")
def created():
    return JSONResponse({"created": True}, status_code=201)


@app.get("/page")
def page():
    return HTMLResponse("<h1>PureAPI</h1>")
```

## 错误处理

### 抛出 HTTPException

```python
from pureapi import HTTPException


@app.get("/users/{user_id:int}")
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="user_id must be positive")
    return {"user_id": user_id}
```

### 自定义错误响应

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

使用 `Router` 拆分模块：

```python
from pureapi import PureAPI, Router

app = PureAPI()
users = Router()


@users.get("/users")
def list_users():
    return []


app.include_router(users, prefix="/api/v1")
```

最终路径：

```text
/api/v1/users
```

## OpenAPI 和 Scalar 文档

PureAPI 默认提供以下文档入口：

| 地址 | 说明 |
| --- | --- |
| `/docs` | Scalar API Reference |
| `/swagger` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI JSON |

### 自定义文档入口

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

### 关闭文档入口

```python
app = PureAPI(
    docs_url=None,
    swagger_url=None,
    redoc_url=None,
)
```

`openapi_url=None` 可以关闭 OpenAPI JSON。

## 完整 CRUD 示例

```python
from pureapi import PureAPI, Request, HTTPException

app = PureAPI(title="Book API", version="1.0.0")

books = {
    1: {"id": 1, "title": "PureAPI Guide", "author": "MarkHoo"},
}


def get_book_or_404(book_id: int):
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books", summary="List books", tags=["books"])
def list_books():
    return {"items": list(books.values()), "count": len(books)}


@app.get("/books/{book_id:int}", summary="Get book", tags=["books"])
def get_book(book_id: int):
    return get_book_or_404(book_id)


@app.post("/books", summary="Create book", tags=["books"])
def create_book(request: Request):
    data = request.json or {}
    title = str(data.get("title", "")).strip()
    author = str(data.get("author", "")).strip()
    if not title or not author:
        raise HTTPException(status_code=400, detail="title and author are required")

    book_id = max(books.keys(), default=0) + 1
    book = {"id": book_id, "title": title, "author": author}
    books[book_id] = book
    return book


@app.patch("/books/{book_id:int}", summary="Update book", tags=["books"])
def update_book(book_id: int, request: Request):
    book = get_book_or_404(book_id)
    data = request.json or {}
    if "title" in data:
        book["title"] = str(data["title"]).strip()
    if "author" in data:
        book["author"] = str(data["author"]).strip()
    return book


@app.delete("/books/{book_id:int}", summary="Delete book", tags=["books"])
def delete_book(book_id: int):
    book = get_book_or_404(book_id)
    del books[book_id]
    return {"deleted": True, "book": book}
```

## 生产部署

### Gunicorn

```bash
gunicorn app:app -w 4 -b 0.0.0.0:8000
```

### uWSGI

```bash
uwsgi --http :8000 --wsgi-file app.py --callable app
```

## 开发者工作流

克隆项目：

```bash
git clone https://github.com/MarkHoo/pureapi.git
cd pureapi
```

安装开发依赖：

```bash
python -m pip install -e ".[dev]"
```

运行测试：

```bash
python -m pytest
```

构建分发包：

```bash
python -m build
```

发布版本时，更新版本号后创建 tag：

```bash
git tag v0.2.0
git push origin v0.2.0
```

仓库中的 GitHub Actions 会在 `v*` 标签推送后执行测试、构建并发布到 PyPI。发布前需要在 PyPI 配置 Trusted Publisher。
