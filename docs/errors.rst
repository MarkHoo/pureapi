错误处理
========

抛出 HTTPException
------------------

.. code-block:: python

   from pureapi import HTTPException


   @app.get("/users/{user_id:int}")
   def get_user(user_id: int):
       if user_id <= 0:
           raise HTTPException(status_code=400, detail="user_id must be positive")
       return {"user_id": user_id}

自定义错误响应
--------------

.. code-block:: python

   @app.exception_handler(404)
   def not_found(request, exc):
       return {
           "error": "not_found",
           "detail": exc.detail,
           "path": request.path,
       }

调试模式
--------

开发时可以开启 ``debug=True``：

.. code-block:: python

   app.run(debug=True)

开启调试后，未捕获异常会返回堆栈信息。生产环境不应开启调试模式。
