# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
from __future__ import annotations

import os
import sys

try:
    sys.path.insert(0, os.path.abspath(".."))
except Exception as e:
    print(f"Error adding path to sys.path: {e}")
    raise  # Re-raise the exception to notify the user

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "FaceRec"
copyright = "2024, Devansh Shah, Devasy Patel"
author = "Devansh Shah, Devasy Patel"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",  # Add this line
]

# Include markdown support
myst_enable_extensions = [
    "colon_fence",
    "html_image",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",  # Add this line to recognize markdown files
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Additional configuration that might raise exceptions can also be wrapped
try:
    # Example of additional configurations that could raise exceptions
    # html_theme_options = {...}
    pass  # Replace with actual configurations if needed
except Exception as e:
    print(f"Error in HTML configuration: {e}")
    raise  # Re-raise the exception to notify the user
