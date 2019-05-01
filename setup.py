# Copyright (c) 2019 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from os.path import dirname, join
from setuptools import find_packages, setup


with open(join(dirname(__file__), 'xson/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()


setup(
    name='xson',
    version=version,
    packages=find_packages(),
    url='https://github.com/renatahodovan/xson',
    license='BSD',
    author='Renata Hodovan, Akos Kiss',
    author_email='hodovan@inf.u-szeged.hu, akiss@inf.u-szeged.hu',
    description='XSON: XML Encoding for JSON',
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
)
