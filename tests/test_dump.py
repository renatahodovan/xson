# Copyright (c) 2019-2023 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import os

from collections import OrderedDict
from math import inf, nan

import pytest

import xson


val_tuplekey = {(1, 2): 3, 4: 5}
exp_tuplekey_skipkeys = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:number name="4">5</json:number></json:object>
'''

val_circular_list = []
val_circular_list.append(val_circular_list)

val_circular_dict = {}
val_circular_dict[None] = val_circular_dict

val_nan = nan
exp_nan_allownan = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">NaN</json:number>
'''

val_inf = inf
exp_inf_allownan = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">Infinity</json:number>
'''

val_neginf = -inf
exp_neginf_allownan = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">-Infinity</json:number>
'''

val_dict_list = {1: [2]}
exp_dict_list_compact = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:array name="1"><json:number>2</json:number></json:array></json:object>
'''
exp_dict_list_newline = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
<json:array name="1">
<json:number>2</json:number>
</json:array>
</json:object>
'''
exp_dict_list_indent = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
  <json:array name="1">
    <json:number>2</json:number>
  </json:array>
</json:object>
'''

val_list_dict = [{1: 2}]
exp_list_dict_compact = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:array xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:object><json:number name="1">2</json:number></json:object></json:array>
'''
exp_list_dict_newline = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:array xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
<json:object>
<json:number name="1">2</json:number>
</json:object>
</json:array>
'''
exp_list_dict_indent = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:array xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
  <json:object>
    <json:number name="1">2</json:number>
  </json:object>
</json:array>
'''

val_object = object()

val_tuple = (1, 2)
exp_tuple_default = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:array xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:number>1</json:number><json:number>2</json:number></json:array>
'''


def tuple_default(val):
    if isinstance(val, tuple):
        return list(val)
    raise TypeError


val_ordereddict = OrderedDict([(4, 3), (2, 1)])
exp_ordereddict = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:number name="4">3</json:number><json:number name="2">1</json:number></json:object>
'''
exp_ordereddict_sortkeys = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:number name="2">1</json:number><json:number name="4">3</json:number></json:object>
'''

val_ordereddict_mixedkeys = OrderedDict([('a', 'b'), (1, 2)])
exp_ordereddict_mixedkeys = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"><json:string name="a">b</json:string><json:number name="1">2</json:number></json:object>
'''


@pytest.mark.parametrize('val, kw, exp', [
    # skipkeys (default: False)
    (val_tuplekey, {}, TypeError),
    (val_tuplekey, {'skipkeys': False}, TypeError),
    (val_tuplekey, {'skipkeys': True}, exp_tuplekey_skipkeys),
    # check_circular (default: True)
    (val_circular_list, {}, ValueError),
    (val_circular_list, {'check_circular': True}, ValueError),
    (val_circular_list, {'check_circular': False}, RuntimeError),
    (val_circular_dict, {}, ValueError),
    (val_circular_dict, {'check_circular': True}, ValueError),
    (val_circular_dict, {'check_circular': False}, RuntimeError),
    # allow_nan (default: True)
    (val_nan, {}, exp_nan_allownan),
    (val_nan, {'allow_nan': True}, exp_nan_allownan),
    (val_nan, {'allow_nan': False}, ValueError),
    (val_inf, {}, exp_inf_allownan),
    (val_inf, {'allow_nan': True}, exp_inf_allownan),
    (val_inf, {'allow_nan': False}, ValueError),
    (val_neginf, {}, exp_neginf_allownan),
    (val_neginf, {'allow_nan': True}, exp_neginf_allownan),
    (val_neginf, {'allow_nan': False}, ValueError),
    # indent (default: None)
    (val_dict_list, {}, exp_dict_list_compact),
    (val_dict_list, {'indent': None}, exp_dict_list_compact),
    (val_dict_list, {'indent': -1}, exp_dict_list_newline),
    (val_dict_list, {'indent': 0}, exp_dict_list_newline),
    (val_dict_list, {'indent': ''}, exp_dict_list_newline),
    (val_dict_list, {'indent': 2}, exp_dict_list_indent),
    (val_dict_list, {'indent': '  '}, exp_dict_list_indent),
    (val_list_dict, {}, exp_list_dict_compact),
    (val_list_dict, {'indent': None}, exp_list_dict_compact),
    (val_list_dict, {'indent': -1}, exp_list_dict_newline),
    (val_list_dict, {'indent': 0}, exp_list_dict_newline),
    (val_list_dict, {'indent': ''}, exp_list_dict_newline),
    (val_list_dict, {'indent': 2}, exp_list_dict_indent),
    (val_list_dict, {'indent': '  '}, exp_list_dict_indent),
    # default (default: None)
    (val_object, {}, TypeError),
    (val_object, {'default': None}, TypeError),
    (val_object, {'default': tuple_default}, TypeError),
    (val_tuple, {}, TypeError),
    (val_tuple, {'default': None}, TypeError),
    (val_tuple, {'default': tuple_default}, exp_tuple_default),
    # sort_keys (default: False)
    (val_ordereddict, {}, exp_ordereddict),
    (val_ordereddict, {'sort_keys': False}, exp_ordereddict),
    (val_ordereddict, {'sort_keys': True}, exp_ordereddict_sortkeys),
    (val_ordereddict_mixedkeys, {}, exp_ordereddict_mixedkeys),
    (val_ordereddict_mixedkeys, {'sort_keys': False}, exp_ordereddict_mixedkeys),
    (val_ordereddict_mixedkeys, {'sort_keys': True}, TypeError),
])
def test_dump(val, kw, exp, tmpdir):
    def _dumps():
        return xson.dumps(val, **kw)

    def _dump():
        tmpfn = os.path.join(str(tmpdir), 'tmp.jsonx')
        with open(tmpfn, 'w', encoding='utf-8') as tmpf:
            xson.dump(val, tmpf, **kw)
        with open(tmpfn, 'r', encoding='utf-8') as tmpf:
            return tmpf.read()

    for dump in (_dumps, _dump):
        if isinstance(exp, type):
            with pytest.raises(exp):
                dump()
        else:
            out = dump()
            assert out.strip() == exp.strip()
