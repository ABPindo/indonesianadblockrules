# This file is part of Adblock Plus <https://adblockplus.org/>,
# Copyright (C) 2006-present eyeo GmbH
# Copyright (C) 2024-present ABPIndo and contributors
#
# Adblock Plus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Adblock Plus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adblock Plus.  If not, see <http://www.gnu.org/licenses/>.

from os import path
from setuptools import setup

with open(path.join(path.dirname(__file__), 'README.rst')) as fh:
    long_description = fh.read()

setup(
    name='python-abp',
    version='0.2.0',
    description='A library for working with Adblock Plus filter lists.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='eyeo GmbH',
    author_email='info@adblockplus.org',
    url='https://hg.adblockplus.org/python-abp/',
    packages=['abp', 'abp.filters', 'abp.stats'],
    entry_points={
        'console_scripts': ['flrender=abp.filters.render_script:main',
                            'fldiff=abp.filters.diff_script:main'],
    },
    include_package_data=True,
    license='GPLv3',
    zip_safe=False,
    keywords='filterlist adblockplus ABP',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
