====
XSON
====
*XML Encoding for JSON*

.. image:: https://badge.fury.io/py/xson.svg
   :target: https://badge.fury.io/py/xson
.. image:: https://travis-ci.org/renatahodovan/xson.svg?branch=master
   :target: https://travis-ci.org/renatahodovan/xson
.. image:: https://coveralls.io/repos/github/renatahodovan/xson/badge.svg?branch=master
   :target: https://coveralls.io/github/renatahodovan/xson?branch=master

*XSON* is a Python package that supports the serialization of Python objects to
XML documents according to the JSONx_ specification (draft), as well as the
deserialization of JSONx documents to Python objects. The implementation aims at
being API-compatible with Python's standard JSON_ package.

.. _JSONx: https://tools.ietf.org/html/draft-rsalz-jsonx-00
.. _JSON: https://docs.python.org/3/library/json.html


Requirements
============

* Python_ >= 3.5
* pip_ and setuptools Python packages (the latter is automatically installed by
  pip)

.. _Python: https://www.python.org
.. _pip: https://pip.pypa.io


Install
=======

The quick way::

    pip install xson

Alternatively, by cloning the project and running setuptools::

    python setup.py install


Usage
=====

Example::

    >>> import xson
    >>> out = xson.dumps({'foo': 42, 'bar': [3.14, 'baz', True, None]}, indent=4)
    >>> print(out)
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


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
