# Copyright (c) 2019 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pkg_resources


__version__ = pkg_resources.get_distribution(__package__).version

JSONX_PREFIX = 'json'
JSONX_NS_URI = 'http://www.ibm.com/xmlns/prod/2009/jsonx'
