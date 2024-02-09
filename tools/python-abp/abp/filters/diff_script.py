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

"""Command line script for rendering Adblock Plus filter list diffs."""

from __future__ import print_function

import argparse
import io
import sys
import os

from .renderer import render_diff
from .parser import parse_filterlist

__all__ = ['main']


class MissingVersionError(Exception):
    """Unable to find Version in filter list."""


def _get_version(filterlist, filename):
    for line in parse_filterlist(filterlist):
        if line.type == 'metadata' and line.key == 'Version':
            return line.value
    raise MissingVersionError('Unable to find Version in {}'.format(filename))


def parse_args():
    parser = argparse.ArgumentParser(description='Render a filter list diff.')
    parser.add_argument('latest',
                        help='The most recent version of the filter list')
    parser.add_argument('-o', '--output_dir', default=os.getcwd(),
                        help='The directory to write the diffs to')
    parser.add_argument('base_files', nargs='+',
                        help='One or more archived filter lists')
    return parser.parse_args()


def main():
    """Entry point for the diff rendering script (fldiff)."""
    args = parse_args()
    with io.open(args.latest, 'r', encoding='utf8') as latest_list:
        latest = latest_list.readlines()

    for base_file in args.base_files:
        with io.open(base_file, 'r', encoding='utf8') as base_file:
            base = base_file.readlines()

        lines = render_diff(base, latest)
        try:
            version = _get_version(base, base_file.name)
        except MissingVersionError as exc:
            sys.exit(exc)

        outfile = os.path.join(args.output_dir, 'diff{}.txt'.format(version))
        with io.open(outfile, 'w', encoding='utf-8') as out_fp:
            for line in lines:
                out_fp.write(line + '\n')
