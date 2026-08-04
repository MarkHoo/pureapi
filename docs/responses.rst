响应对象
========

自动 JSON 响应
--------------

返回 ``dict`` 或 ``list`` 会自动生成 JSON 响应：

.. code-block:: python

   @app.get("/status")
   def status():
       return {"status": "ok"}

显式响应
--------

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

设置响应头
----------

.. code-block:: python

   from pureapi import Response


   @app.get("/download")
   def download():
       return Response(
           "content",
           headers={"Content-Disposition": "attachment; filename=example.txt"},
       )
