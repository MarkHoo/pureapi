PureAPI 文档
============

PureAPI 是一个轻量、直观、零运行时依赖的 Python Web API 框架。它基于 WSGI，适合构建小型服务、内部工具、教学示例、原型 API，以及希望保持依赖简单的 REST API 项目。

项目链接
--------

* PyPI: https://pypi.org/project/pureapi/
* GitHub: https://github.com/MarkHoo/pureapi
* Issues: https://github.com/MarkHoo/pureapi/issues

特性
----

* 类型化路由：支持 ``/users/{user_id:int}`` 这类路径参数，并自动完成类型转换。
* 标准 WSGI：可直接作为 WSGI 应用运行，也可配合 Gunicorn、uWSGI 等服务器部署。
* 自动 JSON 响应：返回 ``dict``、``list`` 等对象时自动序列化为 JSON。
* 请求对象：提供 query、headers、body、json、form 等常用请求数据。
* 内置 OpenAPI：自动生成 ``/openapi.json``。
* 内置接口文档：默认使用 Scalar API Reference，同时保留 Swagger UI 和 ReDoc。
* 零运行时依赖：核心框架只使用 Python 标准库。

支持版本
--------

PureAPI 支持 Python 3.11 及以上版本：

* Python 3.11
* Python 3.12
* Python 3.13
* Python 3.14

.. toctree::
   :maxdepth: 2
   :caption: 使用指南

   installation
   quickstart
   routing
   requests
   responses
   errors
   openapi
   deployment

.. toctree::
   :maxdepth: 2
   :caption: 项目

   api
   changelog
   contributing

.. toctree::
   :maxdepth: 2
   :caption: English Documentation

   en/index
   en/installation
   en/quickstart
   en/routing
   en/requests-responses
   en/openapi
   en/deployment
   en/contributing
