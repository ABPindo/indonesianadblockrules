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

"""Helping methods for filterhit-related statistics."""

import csv


def load_filterhit_statistics(path, sources=None):
    """Load filterhit statistics from a csv file.

    Parameters
    ----------
    path: str
        Path to the csv file with the filterhit statistics.
    sources: iterable of str
        With the filter sources we're interested in. If not None, only filters
        from these sources will be included in the result.

    Returns
    -------
    generator of dict
        With the csv entries.

    """
    integer_cols = ['onehour_sessions', 'hits', 'domains', 'rootdomains']

    with open(path) as csvstream:
        reader = csv.DictReader(csvstream)

        for entry in reader:
            if sources and entry['source'] not in sources:
                continue
            for col in integer_cols:
                try:
                    entry[col] = int(entry[col])
                except KeyError:
                    continue

            yield entry
