"""Sphinx configuration for PureAPI documentation."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

project = "PureAPI"
author = "MarkHoo"
copyright = f"{datetime.now().year}, {author}"

try:
    from pureapi import __version__
except Exception:
    __version__ = "0.0.0"

version = __version__
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "README.md", "Thumbs.db", ".DS_Store"]

language = "zh_CN"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["language-switcher.js"]
html_title = f"{project} {release} 文档"

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = True

master_doc = "index"
