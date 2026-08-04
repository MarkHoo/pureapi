Contributing
============

PureAPI aims to stay lightweight, clear, and dependency-conscious.

Development setup:

.. code-block:: bash

   git clone https://github.com/MarkHoo/pureapi.git
   cd pureapi
   python -m pip install -e ".[dev]"

Run tests:

.. code-block:: bash

   python -m pytest

Build documentation:

.. code-block:: bash

   python -m pip install -e ".[docs]"
   python -m sphinx -b html docs docs/_build/html

Contribution guidelines:

* Keep the core framework free of runtime dependencies.
* Prefer simple, readable APIs over heavy abstractions.
* Update documentation when changing user-facing behavior.
* Add or update tests for route, request, response, exception, and OpenAPI behavior.
* Avoid unrelated formatting-only changes.
