# IPython magic extension to use Mocodo in a Jupyter Notebook.
# Author: Aristide Grange <mocodo@wingi.net>
# License: MIT

from setuptools import setup, find_packages
from codecs import open
import mocodo_magic

long_description = """
IPython magic extension to use Mocodo in a Jupyter Notebook.

Mocodo is an open-source tool for designing and teaching relational databases. It takes as an input a textual description of both entities and associations of an entity-relationship diagram (ERD). It outputs a vectorial drawing in SVG and a relational schema in various formats (SQL, LaTeX, Markdown, etc.).

Installation
------------

The recommended way to install the Mocodo magic extension is to use pip:

::

    pip install mocodo_magic

If this fails, ensure first you have a working Python installation (tested under 2.7 and 3.5).

Usage
-------

Load the magic extension:

::

    %load_ext mocodo_magic

Show the argument list:

::

    %mocodo --help

More
------

`Mocodo online
<http://mocodo.net/>`_

`Documentation
<https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html>`_

`Source code on GitHub
<https://github.com/laowantong/mocodo/>`_"""

with open("README.rst", "w", "utf8") as f:
    f.write(long_description)

setup(
    name="mocodo_magic",
    version=mocodo_magic.__version__,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: IPython'
    ],
    keywords='relational database drawing ERD SVG',
    zip_safe=False,
    description=("Ipython magic extension to use Mocodo in a Jupyter Notebook."),
    url='https://github.com/laowantong/mocodo',
    author='Aristide Grange',
    author_email='mocodo@wingi.net',
    packages=find_packages(exclude=[]),
    install_requires=["ipython", "mocodo"],
    long_description=long_description
)
