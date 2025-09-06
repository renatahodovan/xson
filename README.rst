====
XSON
====
*XML Encoding for JSON*

.. image:: https://img.shields.io/pypi/v/xson?logo=python&logoColor=white
   :target: https://pypi.org/project/xson/
.. image:: https://img.shields.io/pypi/l/xson?logo=open-source-initiative&logoColor=white
   :target: https://pypi.org/project/xson/
.. image:: https://img.shields.io/github/actions/workflow/status/renatahodovan/xson/main.yml?branch=master&logo=github&logoColor=white
   :target: https://github.com/renatahodovan/xson/actions
.. image:: https://img.shields.io/coveralls/github/renatahodovan/xson/master?logo=coveralls&logoColor=white
   :target: https://coveralls.io/github/renatahodovan/xson

.. start included documentation

*XSON* is a Python package that supports the serialization of Python objects to
XML documents according to the JSONx_ specification (draft), as well as the
deserialization of JSONx documents to Python objects. The implementation aims at
being API and CLI-compatible with Python's standard JSON_ package.

.. _JSONx: https://tools.ietf.org/html/draft-rsalz-jsonx-00
.. _JSON: https://docs.python.org/3/library/json.html


Requirements
============

* Python_ >= 3.9

.. _Python: https://www.python.org


Install
=======

To use *XSON* in another project, it can be added to ``setup.cfg`` as an install
requirement (if using setuptools_ with declarative config):

.. code-block:: ini

    [options]
    install_requires =
        xson

To install *XSON* manually, e.g., into a virtual environment, use pip_::

    pip install xson

The above approaches install the latest release of *XSON* from PyPI_.
Alternatively, for the development version, clone the project and perform a
local install::

    pip install .

.. _setuptools: https://github.com/pypa/setuptools
.. _pip: https://pip.pypa.io
.. _PyPI: https://pypi.org/


Usage
=====

API
---

Example:

>>> import xson
>>> out = xson.dumps({'foo': 42, 'bar': [3.14, 'baz', True, None]}, indent=4)
>>> print(out)  #doctest: +NORMALIZE_WHITESPACE
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:number name="foo">42</json:number>
    <json:array name="bar">
        <json:number>3.14</json:number>
        <json:string>baz</json:string>
        <json:boolean>true</json:boolean>
        <json:null/>
    </json:array>
</json:object>
>>> dct = xson.loads(out)
>>> print(dct)
{'foo': 42, 'bar': [3.14, 'baz', True, None]}

CLI
---

A command line tool is available to validate, pretty-print, or convert between
JSONx and JSON objects::

    xson-tool --help

or::

    python -m xson.tool --help

.. end included documentation


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
