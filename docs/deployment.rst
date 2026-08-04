生产部署
========

PureAPI 是 WSGI 应用，可以使用常见 WSGI 服务器部署。

Gunicorn
--------

.. code-block:: bash

   gunicorn app:app -w 4 -b 0.0.0.0:8000

uWSGI
-----

.. code-block:: bash

   uwsgi --http :8000 --wsgi-file app.py --callable app

建议
----

* 生产环境不要开启 ``debug=True``。
* 使用反向代理处理 HTTPS、压缩、静态资源和访问日志。
* 将业务数据保存在数据库或外部存储中，不要依赖进程内内存。
