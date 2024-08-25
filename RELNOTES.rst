====================
*XSON* Release Notes
====================

.. start included documentation

1.1.1
=====

Summary of changes:

* Moved project from flat layout to src layout.
* Improved code internals.
* Improved testing (on Python 3.10, 3.11, 3.12, 3.13, and on PyPy 3.11; also
  linting tests).
* Improved package metadata.
* Improved documentation (switched to furo theme).
* Dropped support for Python 3.5, 3.6, 3.7, and 3.8.


1.1.0
=====

Summary of changes:

* Added command line tool (or module) xson-tool (or xson.tool) to validate,
  pretty-print, or convert between JSONx and JSON objects (highly CLI-compatible
  with the standard json.tool module).
* Improved documentation.
* Improved testing (on PyPy).


1.0.4
=====

Summary of changes:

* Moved to pyproject.toml & setup.cfg-based packaging.
* Improved testing (on Python 3.9).


1.0.3
=====

Summary of changes:

* Fixed doctest embedded in readme to meet the requirements of packaging.
* Improved testing to check the validity of package metadata.


1.0.2
=====

Summary of changes:

* Improved testing (on Python 3.8, on Windows, on macOS).
* Improved package metadata.
* Sphinx can be used to generate documentation.
* CI migrated from Travis CI to GitHub Actions.


1.0.1
=====

Summary of changes:

* Install instructions include pip.
* Automatic SemVer with the help of setuptools_scm.


1.0.0
=====

First release of *XSON*.

Summary of main features:

* Object serialization to and deserialization from JSONx XML documents.
* API-compatibility with the standard JSON package.
* Python 3 implementation.
