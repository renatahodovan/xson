# Copyright (c) 2019-2023 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import json

from math import inf

import pytest

import xson


@pytest.mark.parametrize('value', [
    # null (None)
    None,
    # boolean (bool)
    True,
    False,
    # number (int, float; except NaN, which cannot be cross-validated as NaN != NaN)
    0,
    1,
    -1,
    42,
    3.14,
    -1.28,
    inf,
    -inf,
    # string (str)
    '',
    'foo',
    # array (list)
    [],
    [None, True, False, 0, 1, -1, 42, 3.14, -1.28, inf, -inf, '', 'foo', [], {}],
    # object (dict)
    {},
    {None: None},
    {True: True, False: False},
    {0: 0, 1: 1, -1: -1, 42: 42, 3.14: 3.14, -1.28: -1.28, inf: inf, -inf: -inf},
    {'': None, 'a': True, 'b': False, 'c': 0, 'd': 1, 'e': -1, 'foo': 42, 'g': 3.14, 'h': -1.28, 'i': inf, 'j': -inf, 'k': '', 'l': 'foo', 'm': [], 'n': {}},
])
def test_cross_validate(value):
    xson_repr = xson.dumps(value)
    xson_value = xson.loads(xson_repr)

    json_repr = json.dumps(value)
    json_value = json.loads(json_repr)

    assert xson_value == json_value
