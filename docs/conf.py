# coding: utf-8

import os

html_theme = "sphinx_rtd_theme"  # "sphinx_rtd_theme" | "bootstrap" | "default"

if html_theme == 'bootstrap':
    from sphinx_bootstrap_theme import get_html_theme_path
    html_theme_path = get_html_theme_path()
    html_theme_options = {
        'globaltoc_depth': -1,
        'navbar_site_name': 'Index',  # Tab name for entire site
        'navbar_pagenav': False,
        # 'navbar_title': None,
    }
    html_sidebars = {'**': ['localtoc.html']}
elif html_theme == "sphinx_rtd_theme":
    from sphinx_rtd_theme import get_html_theme_path
    html_theme_path = [get_html_theme_path()]
    html_theme_options = {}
    html_sidebars = {}
else:  # default
    html_theme_options = {}


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',     # dot must be in PATH
    'sphinxcontrib.napoleon',  # requires sphinxcontrib-napoleon
    'sphinxarg.ext',           # requires sphinx-argparse
    # 'rst2pdf.pdfbuilder'       # requires rst2pdf, reportlab
]

html_logo = '_static/logo.png' if os.path.exists('_static/logo.png') else None
html_favicon = '_static/favicon.ico' if os.path.exists('_static/favicon.ico') else None

html_title = None
htmlhelp_basename = None
project = None
copyright = None
version = None
release = None

templates_path = ['_templates']
html_static_path = ['_static']

pygments_style = 'sphinx'
master_doc = 'index'
source_suffix = '.md'
source_encoding = 'utf-8'
add_function_parentheses = True
add_module_names = True
show_authors = False
nitpicky = True
html_use_smartypants = True
html_use_index = False
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
html_domain_indices = False
graphviz_output_format = 'svg'
