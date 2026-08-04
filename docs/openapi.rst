OpenAPI 和 Scalar 文档
======================

PureAPI 默认提供以下文档入口：

.. list-table::
   :header-rows: 1

   * - 地址
     - 说明
   * - ``/docs``
     - Scalar API Reference，默认文档页
   * - ``/swagger``
     - Swagger UI
   * - ``/redoc``
     - ReDoc
   * - ``/openapi.json``
     - OpenAPI 3.0 JSON

增强文档展示
------------

.. code-block:: python

   @app.get(
       "/reports",
       summary="List reports",
       description="Return all reports visible to the current user.",
       tags=["reports"],
       deprecated=False,
   )
   def list_reports():
       return []

自定义文档地址
--------------

.. code-block:: python

   app = PureAPI(
       title="My API",
       version="1.0.0",
       docs_url="/docs",
       scalar_url="/reference",
       swagger_url="/swagger",
       redoc_url="/redoc",
       openapi_url="/openapi.json",
   )

关闭文档入口
------------

.. code-block:: python

   app = PureAPI(
       docs_url=None,
       swagger_url=None,
       redoc_url=None,
   )

``openapi_url=None`` 可以关闭 OpenAPI JSON。
