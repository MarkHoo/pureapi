Routing
=======

PureAPI registers routes with decorators.

Basic Routes
------------

.. code-block:: python

   @app.get("/users")
   def list_users():
       return []


   @app.post("/users")
   def create_user():
       return {"created": True}

HTTP Methods
------------

Supported methods:

* ``get``
* ``post``
* ``put``
* ``patch``
* ``delete``
* ``route``

Path Parameters
---------------

.. code-block:: python

   @app.get("/users/{user_id:int}")
   def get_user(user_id: int):
       return {"user_id": user_id}

Parameter types:

.. list-table::
   :header-rows: 1

   * - Route syntax
     - Converted type
     - Example
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

Route Metadata
--------------

Route metadata is included in the generated OpenAPI schema:

.. code-block:: python

   @app.get(
       "/users",
       summary="List users",
       description="Return all users in the system.",
       tags=["users"],
   )
   def list_users():
       return []

Sub-Routers
-----------

Use ``Router`` to split routes into modules:

.. code-block:: python

   from pureapi import PureAPI, Router

   app = PureAPI()
   users = Router()


   @users.get("/users")
   def list_users():
       return []


   app.include_router(users, prefix="/api/v1")

The final route is:

.. code-block:: text

   /api/v1/users
