# Copyright (c) 2019-2023 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import json

import pytest

import xson


# Test cases taken from:
#   Muschett, B., Salz, R., and Schenker, M., "JSONx, an XML Encoding for JSON",
#   Internet-Draft draft-rsalz-jsonx-00, May 2011,
#   <https://tools.ietf.org/html/draft-rsalz-jsonx-00>.
#
# NOTE:
# - Several inputs have been changed by wrapping them in curly braces to make
#   them valid JSON. The expected outputs have been changed accordingly to have
#   <json:object> as the outmost element.
# - Several outputs have been changed to include XML output declaration as well
#   as the JSONx namespace declaration.
# - Several outputs have been edited for whitespace.
# - The extended example input has been fixed to make it valid JSON (had both
#   missing and extra commas). The output has been sorted by object property
#   names to stabilize the test case.

object_json = '{ "Ticker" : "IBM" }'
object_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:string name="Ticker">IBM</json:string>
</json:object>
'''

array_json = '''
{
    "phoneNumbers": [
        "212 555-1111",
        "212 555-2222"
    ]
}
'''
array_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:array name="phoneNumbers">
        <json:string>212 555-1111</json:string>
        <json:string>212 555-2222</json:string>
    </json:array>
</json:object>
'''

boolean_json = '{ "remote": false }'
boolean_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:boolean name="remote">false</json:boolean>
</json:object>
'''

string_json = '{ "name": "John Smith" }'
string_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:string name="name">John Smith</json:string>
</json:object>
'''

number_json = '{ "height": 62.4 }'
number_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:number name="height">62.4</json:number>
</json:object>
'''

null_json = '{ "additionalInfo": null }'
null_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:null name="additionalInfo"/>
</json:object>
'''

example_json = '''
{
    "name": "John Smith",
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": 10021
    },
    "phoneNumbers": [
        "212 555-1111",
        "212 555-2222"
    ],
    "additionalInfo": null,
    "remote": false,
    "height": 62.4,
    "ficoScore": "> 640"
}
'''
example_xson = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:null name="additionalInfo"/>
    <json:object name="address">
        <json:string name="city">New York</json:string>
        <json:number name="postalCode">10021</json:number>
        <json:string name="state">NY</json:string>
        <json:string name="streetAddress">21 2nd Street</json:string>
    </json:object>
    <json:string name="ficoScore">&gt; 640</json:string>
    <json:number name="height">62.4</json:number>
    <json:string name="name">John Smith</json:string>
    <json:array name="phoneNumbers">
        <json:string>212 555-1111</json:string>
        <json:string>212 555-2222</json:string>
    </json:array>
    <json:boolean name="remote">false</json:boolean>
</json:object>
'''


@pytest.mark.parametrize('json_inp, xson_exp', [
    (object_json, object_xson),
    (array_json, array_xson),
    (boolean_json, boolean_xson),
    (string_json, string_xson),
    (number_json, number_xson),
    (null_json, null_xson),
    (example_json, example_xson),
])
def test_internet_draft(json_inp, xson_exp):
    json_val = json.loads(json_inp)
    xson_out = xson.dumps(json_val, indent=4, sort_keys=True)

    assert xson_out.strip() == xson_exp.strip()

    xson_val = xson.loads(xson_out)

    assert xson_val == json_val
