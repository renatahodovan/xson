# Copyright (c) 2019-2022 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from io import StringIO
from math import isinf, isnan
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesNSImpl

from .pkgdata import JSONX_NS_URI, JSONX_PREFIX


def dump(obj, fp, *, skipkeys=False, check_circular=True, allow_nan=True, indent=None, default=None, sort_keys=False):
    """
    Serialize a value to a file in JSONx format.

    :param obj: Value to be serialized.
    :param fp: File-like object to write JSONx :class:`str` to.
    :param bool skipkeys: If true, then dictionary keys that are not of a basic
        type (:class:`str`, :class:`int`, :class:`float`, :class:`bool`,
        ``None``) will be skipped. Otherwise, a :exc:`TypeError` is raised.
        (Default: ``False``)
    :param bool check_circular: If false, then the circular reference check for
        container types will be skipped. Otherwise, a :exc:`ValueError` is
        raised. (Default: ``True``)
    :param bool allow_nan: If false, then it will be a :exc:`ValueError` to
        serialize out-of-range float values (``nan``, ``inf``, ``-inf``).
        Otherwise, their JavaScript equivalents (``NaN``, ``Infinity``,
        ``-Infinity``) will be used. (Default: ``True``)
    :param indent: If a positive integer, then JSON array elements and object
        members will be pretty-printed with that many spaces per level. If a
        string, that string is used to indent each level. An indent level of 0,
        negative, or ``""`` will only insert newlines. ``None`` selects the most
        compact representation. (Default: ``None``)
    :type indent: int or str
    :param default: If specified, it must be a function that gets called for
        objects that can’t otherwise be serialized, and it must return an
        encodable version of the object. If not specified, :exc:`TypeError` is
        raised. (Default: ``None``)
    :param bool sort_keys: If true, then the output of dictionaries will be
        sorted by key. (Default: ``False``)
    """

    def _attrs(name=None):
        return AttributesNSImpl({(None, 'name'): name} if name is not None else {}, None)

    def _str(value):
        if value is None:
            return 'null'
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, float):
            if isnan(value):
                return 'NaN'
            if isinf(value):
                return 'Infinity' if value > 0 else '-Infinity'
        return str(value)

    def _dump(value, name=None):
        nonlocal stack, level
        if indent is not None:
            gen.ignorableWhitespace(indent * level)

        if isinstance(value, dict):
            if check_circular:
                if id(value) in stack:
                    raise ValueError('container has circular reference')
                stack.add(id(value))

            gen.startElementNS((JSONX_NS_URI, 'object'), None, attrs=_attrs(name))

            if value:
                if indent is not None:
                    gen.ignorableWhitespace('\n')
                level += 1

                for k, v in sorted(value.items(), key=lambda kv: kv[0]) if sort_keys else value.items():
                    if k is not None and not isinstance(k, (str, int, float, bool)):
                        if not skipkeys:
                            raise TypeError(f'dictionary key is not of a basic type: {k!r}')
                        continue
                    _dump(v, name=_str(k))

                level -= 1
                if indent is not None:
                    gen.ignorableWhitespace(indent * level)

            gen.endElementNS((JSONX_NS_URI, 'object'), None)

            if check_circular:
                stack.remove(id(value))

        elif isinstance(value, list):
            if check_circular:
                if id(value) in stack:
                    raise ValueError('container has circular reference')
                stack.add(id(value))

            gen.startElementNS((JSONX_NS_URI, 'array'), None, attrs=_attrs(name))

            if value:
                if indent is not None:
                    gen.ignorableWhitespace('\n')
                level += 1

                for v in value:
                    _dump(v)

                level -= 1
                if indent is not None:
                    gen.ignorableWhitespace(indent * level)

            gen.endElementNS((JSONX_NS_URI, 'array'), None)

            if check_circular:
                stack.remove(id(value))

        elif isinstance(value, str):
            gen.startElementNS((JSONX_NS_URI, 'string'), None, attrs=_attrs(name))
            gen.characters(value)
            gen.endElementNS((JSONX_NS_URI, 'string'), None)

        elif isinstance(value, bool):
            gen.startElementNS((JSONX_NS_URI, 'boolean'), None, attrs=_attrs(name))
            gen.characters(_str(value))
            gen.endElementNS((JSONX_NS_URI, 'boolean'), None)

        elif isinstance(value, (int, float)):
            if not allow_nan and (isinf(value) or isnan(value)):
                raise ValueError(f'float value is out of range: {value!r}')

            gen.startElementNS((JSONX_NS_URI, 'number'), None, attrs=_attrs(name))
            gen.characters(_str(value))
            gen.endElementNS((JSONX_NS_URI, 'number'), None)

        elif value is None:
            gen.startElementNS((JSONX_NS_URI, 'null'), None, attrs=_attrs(name))
            gen.endElementNS((JSONX_NS_URI, 'null'), None)

        elif default:
            _dump(default(value), name=name)

        else:
            raise TypeError(f'cannot serialize object: {value!r}')

        if indent is not None:
            gen.ignorableWhitespace('\n')

    stack = set()
    level = 0
    if indent is not None and isinstance(indent, int):
        indent = ' ' * indent if indent > 0 else ''

    gen = XMLGenerator(fp, encoding='UTF-8', short_empty_elements=True)
    gen.startDocument()
    gen.startPrefixMapping(JSONX_PREFIX, JSONX_NS_URI)
    _dump(obj)
    gen.endPrefixMapping(JSONX_PREFIX)
    gen.endDocument()


def dumps(obj, *, skipkeys=False, check_circular=True, allow_nan=True, indent=None, default=None, sort_keys=False):
    """
    Serialize a value to a string in JSONx format.

    The arguments have the same meaning as in :func:`dump`.

    :return: JSONx string.
    :rtype: str
    """

    s = StringIO()
    dump(obj, s, skipkeys=skipkeys, check_circular=check_circular, allow_nan=allow_nan, indent=indent, default=default, sort_keys=sort_keys)
    return s.getvalue()
