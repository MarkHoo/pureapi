OpenAPI and Documentation UI
============================

PureAPI registers documentation routes automatically:

.. list-table::
   :header-rows: 1

   * - Path
     - Description
   * - ``/docs``
     - Scalar API Reference, the default documentation UI
   * - ``/swagger``
     - Swagger UI
   * - ``/redoc``
     - ReDoc
   * - ``/openapi.json``
     - OpenAPI 3.0 JSON

Improve Documentation Output
----------------------------

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

Customize Documentation Routes
------------------------------

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

Disable Documentation Routes
----------------------------

.. code-block:: python

   app = PureAPI(
       docs_url=None,
       swagger_url=None,
       redoc_url=None,
   )

Set ``openapi_url=None`` to disable the OpenAPI JSON route.
