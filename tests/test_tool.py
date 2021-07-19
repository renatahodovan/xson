# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import os
import pytest
import subprocess
import sys

import xson


question_json = '''
{
    "answer": 42,
    "name": {
        "first": "Douglas",
        "last": "Adams",
        "von": null
    },
    "series": [
        "The Hitchhiker's Guide to the Galaxy",
        "The Restaurant at the End of the Universe",
        "Life, the Universe and Everything",
        "So Long, and Thanks for all the Fish",
        "Mostly Harmless"
    ],
    "triolgy": true
}
'''

question_jsonx = '''
<?xml version="1.0" encoding="UTF-8"?>
<json:object xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx">
    <json:number name="answer">42</json:number>
    <json:object name="name">
        <json:string name="first">Douglas</json:string>
        <json:string name="last">Adams</json:string>
        <json:null name="von"/>
    </json:object>
    <json:array name="series">
        <json:string>The Hitchhiker's Guide to the Galaxy</json:string>
        <json:string>The Restaurant at the End of the Universe</json:string>
        <json:string>Life, the Universe and Everything</json:string>
        <json:string>So Long, and Thanks for all the Fish</json:string>
        <json:string>Mostly Harmless</json:string>
    </json:array>
    <json:boolean name="triolgy">true</json:boolean>
</json:object>
'''


def indent_default(s):
    return s


def indent_tab(s):
    return s.replace('    ', '\t')


def indent_2(s):
    return s.replace('    ', '  ')


def indent_noindent_json(s):
    return s.replace('    ', '').replace(',\n', ', \n').replace('\n', '')


def indent_noindent_jsonx(s):
    return s.replace('    ', '').replace('>\n', '>').replace('?>', '?>\n')


@pytest.mark.parametrize('indent_arg, indent_jsonx, indent_json', [
    (None, indent_default, indent_default),
    ('--tab', indent_tab, indent_tab),
    ('--indent=2', indent_2, indent_2),
    ('--no-indent', indent_noindent_jsonx, indent_noindent_json),
])
@pytest.mark.parametrize('infile, outfile', [
    (False, False),  # stdin to stdout
    (True, False),  # file to stdout
    (True, True),  # file to file
])
@pytest.mark.parametrize('infile_json, outfile_json', [
    (False, False),  # jsonx to jsonx
    (False, True),  # jsonx to json
    (True, False),  # json to jsonx
    (True, True),  # json to json
])
def test_tool(indent_arg, indent_jsonx, indent_json, infile, outfile, infile_json, outfile_json, tmpdir):
    cmd = [sys.executable, '-m', 'xson.tool', '--sort-keys']

    if infile_json:
        input = question_json
        input_ext = '.json'
        cmd += ['--infile-json']
    else:
        input = question_jsonx
        input_ext = '.jsonx'
    input = input.strip()

    if outfile_json:
        expected = question_json
        expected = indent_json(expected)
        output_ext = '.json'
        cmd += ['--outfile-json']
    else:
        expected = question_jsonx
        expected = indent_jsonx(expected)
        output_ext = '.jsonx'
    expected = expected.strip()

    if indent_arg:
        cmd += [indent_arg]

    if infile:
        infile = os.path.join(str(tmpdir), 'in' + input_ext)
        with open(infile, 'w') as f:
            f.write(input)
        cmd += [infile]
        input = None

    if outfile:
        outfile = os.path.join(str(tmpdir), 'out' + output_ext)
        cmd += [outfile]
        stdout = None
    else:
        stdout = subprocess.PIPE

    result = subprocess.run(cmd, input=input, stdout=stdout, universal_newlines=True, check=True)

    if outfile:
        with open(outfile, 'r') as f:
            output = f.read()
    else:
        output = result.stdout
    output = output.strip()

    assert output == expected
