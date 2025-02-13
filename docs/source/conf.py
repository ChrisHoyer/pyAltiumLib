# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os, sys
sys.path.insert(0, os.path.abspath('../../src'))
import pyaltiumlib

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = u'pyAltiumLib'
copyright = u'%s, %s <%s>' % (pyaltiumlib.CYEAR, pyaltiumlib.AUTHOR_NAME, pyaltiumlib.AUTHOR_EMAIL)

version = pyaltiumlib.__version__ 

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.coverage']

templates_path = []
exclude_patterns = []

autodoc_default_options = { "members": True,
                           "no-index": True,
                           "special-members": "__repr__",}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = []
