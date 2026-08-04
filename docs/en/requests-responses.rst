Requests and Responses
======================

Request Object
--------------

Add a ``request`` parameter to access the request object:

.. code-block:: python

   from pureapi import Request


   @app.post("/messages")
   def create_message(request: Request):
       data = request.json
       return {"received": data}

Common request properties:

.. list-table::
   :header-rows: 1

   * - Property
     - Description
   * - ``request.method``
     - HTTP method
   * - ``request.path``
     - Request path
   * - ``request.query_string``
     - Raw query string
   * - ``request.query_params``
     - Parsed query parameters
   * - ``request.headers``
     - Request headers
   * - ``request.body``
     - Raw request body as bytes
   * - ``request.json``
     - Parsed JSON body
   * - ``request.form``
     - Parsed form body
   * - ``request.content_type``
     - Content-Type header
   * - ``request.url``
     - Full request URL

Automatic JSON Responses
------------------------

Returning a ``dict`` or ``list`` creates a JSON response automatically:

.. code-block:: python

   @app.get("/status")
   def status():
       return {"status": "ok"}

Explicit Responses
------------------

.. code-block:: python

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

Errors
------

.. code-block:: python

   from pureapi import HTTPException


   @app.get("/users/{user_id:int}")
   def get_user(user_id: int):
       if user_id <= 0:
           raise HTTPException(status_code=400, detail="user_id must be positive")
       return {"user_id": user_id}

Custom error handler:

.. code-block:: python

   @app.exception_handler(404)
   def not_found(request, exc):
       return {
           "error": "not_found",
           "detail": exc.detail,
           "path": request.path,
       }
