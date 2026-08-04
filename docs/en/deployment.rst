Deployment
==========

PureAPI is a WSGI application and can run behind common WSGI servers.

Gunicorn
--------

.. code-block:: bash

   gunicorn app:app -w 4 -b 0.0.0.0:8000

uWSGI
-----

.. code-block:: bash

   uwsgi --http :8000 --wsgi-file app.py --callable app

Recommendations
---------------

* Do not enable ``debug=True`` in production.
* Use a reverse proxy for HTTPS, compression, static files, and access logs.
* Store business data in a database or external storage instead of process memory.
