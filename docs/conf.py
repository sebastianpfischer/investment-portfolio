import os
import sys

sys.path.insert(0, os.path.abspath("../src/investporto"))


# -- Project information -----------------------------------------------------
import investporto

project = "investporto"
copyright = "2020, Sebastian Fischer"
author = "Sebastian Fischer"

version = investporto.__version__.split(".")[0]
release = investporto.__version__


# -- General configuration ---------------------------------------------------

primary_domain = "py"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinxcontrib.programoutput",
    "sphinx_autodoc_typehints",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "restructuredtext",
}
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Include documentation from both the class level and __init__
autoclass_content = "both"

# The default autodoc directive flags
autodoc_default_flags = ["members", "show-inheritance"]
