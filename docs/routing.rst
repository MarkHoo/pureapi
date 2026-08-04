路由
====

PureAPI 使用装饰器注册路由。

基础路由
--------

.. code-block:: python

   @app.get("/users")
   def list_users():
       return []


   @app.post("/users")
   def create_user():
       return {"created": True}

HTTP 方法
---------

支持的方法：

* ``get``
* ``post``
* ``put``
* ``patch``
* ``delete``
* ``route``

路径参数
--------

.. code-block:: python

   @app.get("/users/{user_id:int}")
   def get_user(user_id: int):
       return {"user_id": user_id}

参数类型：

.. list-table::
   :header-rows: 1

   * - 路由写法
     - 转换类型
     - 示例
   * - ``{name}``
     - ``str``
     - ``/users/alice``
   * - ``{id:int}``
     - ``int``
     - ``/users/1``
   * - ``{price:float}``
     - ``float``
     - ``/prices/19.9``
   * - ``{file:path}``
     - ``str``
     - ``/files/a/b/c.txt``

如果类型转换失败，路由不会匹配。

路由元数据
----------

路由元数据会进入 OpenAPI，并显示在 Scalar、Swagger UI 和 ReDoc 中：

.. code-block:: python

   @app.get(
       "/users",
       summary="List users",
       description="Return all users in the system.",
       tags=["users"],
   )
   def list_users():
       return []

子路由
------

使用 ``Router`` 拆分模块：

.. code-block:: python

   from pureapi import PureAPI, Router

   app = PureAPI()
   users = Router()


   @users.get("/users")
   def list_users():
       return []


   app.include_router(users, prefix="/api/v1")

最终路径：

.. code-block:: text

   /api/v1/users
