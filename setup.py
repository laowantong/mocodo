#!/usr/bin/env python
# encoding: utf-8

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path
from mocodo.version_number import version

long_description = """
Mocodo is an open-source tool for designing and teaching relational databases. It takes as an input a textual description of both entities and associations of an entity-relationship diagram (ERD). It outputs a vectorial drawing in SVG and a relational schema in various formats (SQL, LaTeX, Markdown, etc.).

Installation
------------

The recommended way to install Mocodo is to use pip:

::

    pip install mocodo

If this fails, ensure first you have a working Python installation (tested under 2.7 and 3.5).

Usage
-------

Generate the conceptual diagram of a default ERD:

::

    mocodo

Show the argument list:

::

    mocodo --help

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
    name='mocodo',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description=u'Modélisation Conceptuelle de Données. Nickel. Ni souris.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/laowantong/mocodo',

    # Author details
    author='Aristide Grange',
    author_email='mocodo@wingi.net',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Topic :: Database',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='relational database drawing ERD SVG',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["mocodo"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['peppercorn'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'mocodo': [
            'colors/*.json',
            'lorem/*.txt',
            'relation_templates/*.json',
            'res/*.mo',
            'shapes/*.json',
            'pristine_sandbox.mcd',
            'font_metrics.json'
        ],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': ['mocodo=mocodo.__main__:main'],
    },
    
    # Not all packages, however, are capable of running in compressed form,
    # because they may expect to be able to access either source code or data files
    # as normal operating system files. 
    zip_safe=False,
)
