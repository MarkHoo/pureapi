请求对象
========

处理函数中声明 ``request`` 参数即可获取请求对象：

.. code-block:: python

   from pureapi import Request


   @app.post("/messages")
   def create_message(request: Request):
       data = request.json
       return {"received": data}

常用属性
--------

.. list-table::
   :header-rows: 1

   * - 属性
     - 说明
   * - ``request.method``
     - HTTP 方法
   * - ``request.path``
     - 请求路径
   * - ``request.query_string``
     - 原始查询字符串
   * - ``request.query_params``
     - 查询参数
   * - ``request.headers``
     - 请求头
   * - ``request.body``
     - 原始请求体 bytes
   * - ``request.json``
     - JSON 请求体
   * - ``request.form``
     - 表单请求体
   * - ``request.content_type``
     - Content-Type
   * - ``request.url``
     - 完整请求 URL

查询参数
--------

.. code-block:: python

   @app.get("/search")
   def search(request: Request):
       keyword = request.query_params.get("q", "")
       return {"keyword": keyword}

JSON 请求体
-----------

.. code-block:: python

   @app.post("/users")
   def create_user(request: Request):
       data = request.json or {}
       return {"name": data.get("name")}
