# Copyright (c) 2019-2023 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import os

from math import inf, isnan, nan

import pytest

import xson


inp_tuple = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:array name="$tuple">
        <json:number>1</json:number>
        <json:number>2</json:number>
    </json:array>
</json:object>
'''
exp_tuple_dict = {'$tuple': [1, 2]}
exp_tuple = (1, 2)
exp_list = [1, 2]


def tuple_object_hook(obj):
    if '$tuple' in obj:
        return tuple(obj['$tuple'])
    return obj


def tuple_list_object_pairs_hook(pairs):
    obj = dict(pairs)
    if '$tuple' in obj:
        return list(obj['$tuple'])
    return obj


inp_one = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">1</json:number>
'''
exp_one_str = '$int: 1'


def parse_int_str(s):
    return f'$int: {s}'


inp_pi = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">3.14</json:number>
'''
exp_pi_str = '$float: 3.14'


def parse_float_str(s):
    return f'$float: {s}'


inp_nan = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">NaN</json:number>
'''
exp_nan_str = '$constant: NaN'

inp_inf = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">Infinity</json:number>
'''
exp_inf_str = '$constant: Infinity'

inp_neginf = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:number xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">-Infinity</json:number>
'''
exp_neginf_str = '$constant: -Infinity'


def parse_constant_str(s):
    return f'$constant: {s}'


@pytest.mark.parametrize('inp, kw, exp', [
    # object_hook (default: None)
    (inp_tuple, {}, exp_tuple_dict),
    (inp_tuple, {'object_hook': None}, exp_tuple_dict),
    (inp_tuple, {'object_hook': tuple_object_hook}, exp_tuple),
    # object_pairs_hook (default: None)
    (inp_tuple, {'object_pairs_hook': None}, exp_tuple_dict),
    (inp_tuple, {'object_pairs_hook': tuple_list_object_pairs_hook}, exp_list),
    (inp_tuple, {'object_pairs_hook': tuple_list_object_pairs_hook, 'object_hook': tuple_object_hook}, exp_list),
    # parse_int (default: None/int)
    (inp_one, {}, int(1)),
    (inp_one, {'parse_int': None}, int(1)),
    (inp_one, {'parse_int': parse_int_str}, exp_one_str),
    # parse_float (default: None/float)
    (inp_pi, {}, float(3.14)),
    (inp_pi, {'parse_float': None}, float(3.14)),
    (inp_pi, {'parse_float': parse_float_str}, exp_pi_str),
    # parse_constant (default: None/float)
    (inp_nan, {}, nan),
    (inp_nan, {'parse_constant': None}, nan),
    (inp_nan, {'parse_constant': parse_constant_str}, exp_nan_str),
    (inp_inf, {}, inf),
    (inp_inf, {'parse_constant': None}, inf),
    (inp_inf, {'parse_constant': parse_constant_str}, exp_inf_str),
    (inp_neginf, {}, -inf),
    (inp_neginf, {'parse_constant': None}, -inf),
    (inp_neginf, {'parse_constant': parse_constant_str}, exp_neginf_str),
])
def test_load(inp, kw, exp, tmpdir):
    def _loads():
        return xson.loads(inp.strip(), **kw)

    def _load():
        tmpfn = os.path.join(str(tmpdir), 'tmp.jsonx')
        with open(tmpfn, 'w', encoding='utf-8') as tmpf:
            tmpf.write(inp.strip())
        with open(tmpfn, 'r', encoding='utf-8') as tmpf:
            return xson.load(tmpf, **kw)

    for load in (_loads, _load):
        if isinstance(exp, type):
            with pytest.raises(exp):
                load()
        else:
            val = load()
            if isinstance(val, float) and isnan(val):
                assert isinstance(exp, float) and isnan(exp)
            else:
                assert val == exp
