Quick Start
===========

Create ``app.py``:

.. code-block:: python

   from pureapi import PureAPI, Request, HTTPException

   app = PureAPI(
       title="Task API",
       version="1.0.0",
       description="A small task management API built with PureAPI.",
   )

   tasks = {
       1: {"id": 1, "title": "Write documentation", "done": False},
   }


   @app.get("/", summary="API home", tags=["system"])
   def home():
       """Return basic service information."""
       return {
           "name": "Task API",
           "docs": "/docs",
           "openapi": "/openapi.json",
       }


   @app.get("/tasks", summary="List tasks", tags=["tasks"])
   def list_tasks():
       """Return all tasks."""
       return {"items": list(tasks.values()), "count": len(tasks)}


   @app.get("/tasks/{task_id:int}", summary="Get task", tags=["tasks"])
   def get_task(task_id: int):
       """Return one task by ID."""
       task = tasks.get(task_id)
       if task is None:
           raise HTTPException(status_code=404, detail="Task not found")
       return task


   @app.post("/tasks", summary="Create task", tags=["tasks"])
   def create_task(request: Request):
       """Create a task from a JSON request body."""
       data = request.json or {}
       title = str(data.get("title", "")).strip()
       if not title:
           raise HTTPException(status_code=400, detail="title is required")

       task_id = max(tasks.keys(), default=0) + 1
       task = {"id": task_id, "title": title, "done": False}
       tasks[task_id] = task
       return task


   if __name__ == "__main__":
       app.run(host="127.0.0.1", port=8000, debug=True)

Start the application:

.. code-block:: bash

   python app.py

Open:

* API home: http://127.0.0.1:8000/
* Scalar docs: http://127.0.0.1:8000/docs
* Swagger UI: http://127.0.0.1:8000/swagger
* ReDoc: http://127.0.0.1:8000/redoc
* OpenAPI JSON: http://127.0.0.1:8000/openapi.json
