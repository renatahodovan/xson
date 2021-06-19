====
XSON
====
*XML Encoding for JSON*

.. image:: https://img.shields.io/pypi/v/xson?logo=python&logoColor=white
   :target: https://pypi.org/project/xson/
.. image:: https://img.shields.io/pypi/l/xson?logo=open-source-initiative&logoColor=white
   :target: https://pypi.org/project/xson/
.. image:: https://img.shields.io/github/workflow/status/renatahodovan/xson/main/master?logo=github&logoColor=white
   :target: https://github.com/renatahodovan/xson/actions
.. image:: https://img.shields.io/coveralls/github/renatahodovan/xson/master?logo=coveralls&logoColor=white
   :target: https://coveralls.io/github/renatahodovan/xson

.. start included documentation

*XSON* is a Python package that supports the serialization of Python objects to
XML documents according to the JSONx_ specification (draft), as well as the
deserialization of JSONx documents to Python objects. The implementation aims at
being API-compatible with Python's standard JSON_ package.

.. _JSONx: https://tools.ietf.org/html/draft-rsalz-jsonx-00
.. _JSON: https://docs.python.org/3/library/json.html


Requirements
============

* Python_ >= 3.5
* pip_

.. _Python: https://www.python.org
.. _pip: https://pip.pypa.io


Install
=======

The quick way::

    pip install xson

Alternatively, by cloning the project and performing a local install::

    pip install .


Usage
=====

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

.. end included documentation


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
