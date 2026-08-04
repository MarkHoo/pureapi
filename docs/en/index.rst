English Documentation
=====================

PureAPI is a lightweight, intuitive, zero-runtime-dependency Python web API framework. It is built on WSGI and is suitable for small services, internal tools, teaching examples, prototype APIs, and REST API projects that value a small dependency footprint.

Project Links
-------------

* PyPI: https://pypi.org/project/pureapi/
* GitHub: https://github.com/MarkHoo/pureapi
* Issues: https://github.com/MarkHoo/pureapi/issues

Features
--------

* Typed routing with automatic conversion, such as ``/users/{user_id:int}``.
* Standard WSGI application interface.
* Automatic JSON responses for ``dict`` and ``list`` return values.
* Request object with query parameters, headers, body, JSON, form data, and URL helpers.
* Built-in OpenAPI generation at ``/openapi.json``.
* Built-in API documentation with Scalar API Reference by default, plus Swagger UI and ReDoc.
* Zero runtime dependencies in the core framework.

Supported Python Versions
-------------------------

PureAPI supports Python 3.11 and newer:

* Python 3.11
* Python 3.12
* Python 3.13
* Python 3.14

Sections
--------

* :doc:`installation`
* :doc:`quickstart`
* :doc:`routing`
* :doc:`requests-responses`
* :doc:`openapi`
* :doc:`deployment`
* :doc:`contributing`
