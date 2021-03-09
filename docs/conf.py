# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'eemont'
copyright = '2021, David Montero Loaiza'
author = 'David Montero Loaiza'

# The full version, including alpha/beta/rc tags
release = '0.1.8'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    'sphinx.ext.napoleon',
    "sphinx_rtd_theme",
    'sphinx.ext.autosummary',
    'sphinx.ext.autosectionlabel'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
#html_theme = "insegel"
#html_theme = "divio_docs_theme"
#html_theme = "karma_sphinx_theme"
#html_theme = "sphinx_materialdesign_theme"

#html_theme_options = {
    # Specify a list of menu in Header.
    # Tuples forms:
    #  ('Name', 'external url or path of pages in the document', boolean, 'icon name')
    #
    # Third argument:
    # True indicates an external link.
    # False indicates path of pages in the document.
    #
    # Fourth argument:
    # Specify the icon name.
    # For details see link.
    # https://material.io/icons/
#    'header_links' : [
#        ('Home', 'index', False, 'home'),
#        ("GitHub", "https://github.com/davemlz/eemont", True, 'link')
#    ],

    # Customize css colors.
    # For details see link.
    # https://getmdl.io/customize/index.html
    #
    # Values: amber, blue, brown, cyan deep_orange, deep_purple, green, grey, indigo, light_blue,
    #         light_green, lime, orange, pink, purple, red, teal, yellow(Default: indigo)
#    'primary_color': 'blue',
    # Values: Same as primary_color. (Default: pink)
#    'accent_color': 'pink',

    # Customize layout.
    # For details see link.
    # https://getmdl.io/components/index.html#layout-section
#    'fixed_drawer': False,
#    'fixed_header': True,
#    'header_waterfall': False,
#    'header_scroll': False,

    # Render title in header.
    # Values: True, False (Default: False)
#    'show_header_title': False,
    # Render title in drawer.
    # Values: True, False (Default: True)
#    'show_drawer_title': True,
    # Render footer.
    # Values: True, False (Default: True)
#    'show_footer': True
#}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_sidebars = { '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'] }