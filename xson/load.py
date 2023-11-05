# Copyright (c) 2019-2023 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from io import StringIO
from math import isinf, isnan
from xml.sax import make_parser
from xml.sax.handler import ContentHandler, ErrorHandler, feature_namespaces

from .pkgdata import JSONX_NS_URI


class JSONxElement:
    def __init__(self, localname, key, value):
        self.localname = localname
        self.key = key
        self.value = value


class JSONxHandler(ContentHandler, ErrorHandler):

    def __init__(self, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None):
        super().__init__()

        self._object_hook = object_hook
        self._parse_float = parse_float
        self._parse_int = parse_int
        self._parse_constant = parse_constant
        self._object_pairs_hook = object_pairs_hook

        self.stack = [JSONxElement('root', None, None)]

    def startElement(self, name, attrs):
        self._expect(False, f'unsupported non-namespaced element {name}')

    def endElement(self, name):
        assert False, 'SAX parser must ensure that non-namespaced end of element does not occur'

    def startElementNS(self, name, qname, attrs):
        uri, localname = name
        self._expect(uri == JSONX_NS_URI, f'unsupported namespace URI {uri}')

        self._expect(self.stack[-1].localname in ('root', 'object', 'array'), f'{self.stack[-1].localname} element cannot contain other elements')

        key = attrs[(None, 'name')] if (None, 'name') in attrs else None
        if self.stack[-1].localname == 'object':
            self._expect(key is not None, 'element within an object element must have a name attribute')

        if localname == 'object':
            self.stack.append(JSONxElement(localname, key, []))
        elif localname == 'array':
            self.stack.append(JSONxElement(localname, key, []))
        elif localname in ('string', 'number', 'boolean'):
            self.stack.append(JSONxElement(localname, key, StringIO()))
        elif localname == 'null':
            self.stack.append(JSONxElement(localname, key, None))
        else:
            self._expect(False, f'unsupported element {localname}')

    def endElementNS(self, name, qname):
        uri, localname = name
        assert uri == JSONX_NS_URI, 'SAX parser must ensure that namespace URIs of start and end of elements match'

        element = self.stack.pop()
        assert element.localname == localname, 'SAX parser must ensure that localnames of start and end of elements match'

        value = element.value
        if localname == 'object':
            if self._object_pairs_hook:
                value = self._object_pairs_hook(value)
            else:
                value = dict(value)
                if self._object_hook:
                    value = self._object_hook(value)
        elif localname == 'string':
            value = value.getvalue()
        elif localname == 'number':
            value = value.getvalue()
            try:
                value_default = int(value)
                value_parser = self._parse_int
            except ValueError:
                try:
                    value_default = float(value)
                    value_parser = self._parse_float if not isnan(value_default) and not isinf(value_default) else self._parse_constant
                except ValueError:
                    self._expect(False, 'number element must contain text content in floating point format')
            value = value_parser(value) if value_parser else value_default
        elif localname == 'boolean':
            value = value.getvalue()
            self._expect(value in ('true', 'false'), 'boolean element must contain either true or false text content')
            value = value == 'true'

        container = self.stack[-1]
        if container.localname == 'root':
            container.value = value
        elif container.localname == 'object':
            container.value.append((element.key, value))
        elif container.localname == 'array':
            container.value.append(value)
        else:
            assert False, f'unexpected container element {container.localname}'

    def characters(self, content):
        element = self.stack[-1]
        if isinstance(element.value, StringIO):
            element.value.write(content)
        else:
            self._expect(content.isspace(), f'{element.localname} element must not have non-whitespace character content {content}')

    def error(self, exception):
        self._expect(False, exception.getMessage())

    fatalError = error

    def warning(self, exception):
        # Suppress warnings.
        pass

    def _expect(self, expr, msg):
        if not expr:
            raise ValueError(f'{msg} [line {self._locator.getLineNumber()}, column {self._locator.getColumnNumber()}]')


def load(fp, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None):
    """
    Deserialize a JSONx file to a Python object.

    :param fp: File-like object to be deserialized.
    :param object_hook: If specified, it must be a function that will be called
        with the result of any object decoded (a :class:`dict`), and its return
        value will be used instead. (Default: ``None``)
    :param object_pairs_hook: If specified, it must be a function that will be
        called with the result of any object decoded into an ordered list of
        pairs, and its return value will be used instead. If ``object_hook`` is
        also specified, ``object_pairs_hook`` takes priority. (Default:
        ``None``)
    :param parse_float: If specified, it must be a function that will be called
        with the string of every float to be decoded. (Default: :class:`float`)
    :param parse_int: If specified, it must be a function that will be called
        with the string of every int to be decoded. (Default: :class:`int`)
    :param parse_constant: If specified, it must be a function that will be
        called with one of the following strings: ``'-Infinity'``,
        ``'Infinity'``, or ``'NaN'``. (Default: :class:`float`)
    :return: The value deserialized.
    :raises ValueError: If the data being deserialized is not a valid JSONx
        document.
    """

    handler = JSONxHandler(object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook)

    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(handler)
    parser.setFeature(feature_namespaces, True)
    parser.parse(fp)

    assert len(handler.stack) == 1 and handler.stack[0].localname == 'root'
    return handler.stack[0].value


def loads(s, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None):
    """
    Deserialize a JSONx string to a Python object.

    :param str s: String to be deserialized.

    The keyword arguments have the same meaning as in :func:`load`.
    """

    return load(StringIO(s), object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook)
