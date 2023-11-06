# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import sys

from argparse import ArgumentParser, FileType
from json import dump as json_dump, load as json_load

from .dump import dump as xson_dump
from .load import load as xson_load


def execute():
    parser = ArgumentParser(description='''
        A simple command line interface for the xson module to validate,
        pretty-print, and convert between JSONx and JSON objects.
    ''')

    parser.add_argument('infile', nargs='?', type=FileType('r', encoding='utf-8'), default=sys.stdin,
                        help='input file to be validated or pretty-printed (default: stdin)')
    parser.add_argument('outfile', nargs='?', type=FileType('w', encoding='utf-8'), default=sys.stdout,
                        help='write the output of infile to outfile (default: stdout)')
    parser.add_argument('--sort-keys', action='store_true',
                        help='sort the output of dictionaries alphabetically by key')

    indent_group = parser.add_mutually_exclusive_group()
    indent_group.add_argument('--indent', metavar='N', type=int, default=4,
                              help='separate items with newlines and use N spaces for indentation')
    indent_group.add_argument('--tab', dest='indent', action='store_const', const='\t',
                              help='separate items with newlines and use tabs for indentation')
    indent_group.add_argument('--no-indent', dest='indent', action='store_const', const=None,
                              help='separate items with spaces rather than newlines')

    parser.add_argument('-j', '--infile-json', action='store_true',
                        help='read input as JSON rather than JSONx')
    parser.add_argument('-J', '--outfile-json', action='store_true',
                        help='write output as JSON rather than JSONx')

    args = parser.parse_args()

    load = json_load if args.infile_json else xson_load
    dump = json_dump if args.outfile_json else xson_dump

    with args.infile as infile:
        obj = load(infile)
    with args.outfile as outfile:
        dump(obj, outfile, sort_keys=args.sort_keys, indent=args.indent)


if __name__ == '__main__':
    execute()
