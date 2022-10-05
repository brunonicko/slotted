# type: ignore

import os
import sys

# Path setup.
root_path = os.path.abspath(os.path.join("..", ".."))
sys.path.insert(0, root_path)

# Project information.
project = "Slotted"
copyright = "2022, Bruno Nicko"  # noqa
author = "Bruno Nicko"

# Sphinx extensions.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
]

# Intersphinx configuration.
intersphinx_mapping = {
    "six": ("https://six.readthedocs.io/", None),
    "tippo": ("https://tippo.readthedocs.io/en/stable/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "python": ("https://docs.python.org/3.10", None),
}

# Autodoc configuration.
autoclass_content = "class"
autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

# Templates' paths.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = [".rst"]

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx.
language = "en"

# List of patterns to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "monokai"

# HTML options.
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "style_external_links": False,
    "style_nav_header_background": "#CC6766",
}
html_static_path = ["_static"]
