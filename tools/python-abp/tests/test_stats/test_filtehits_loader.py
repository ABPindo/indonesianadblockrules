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

import pytest
import py

from abp.stats.filterhits import load_filterhit_statistics

DATA_PATH = py.path.local(__file__).dirpath('data')


@pytest.fixture
def filterhits_file():
    return DATA_PATH.join('filterhits.csv')


@pytest.fixture
def filterhits_file_missing_columns():
    return DATA_PATH.join('filterhits_missing_columns.csv')


def test_filterhits_load_no_filtering(filterhits_file):
    entries = load_filterhit_statistics(str(filterhits_file))

    count = 0

    for entry in entries:
        count += 1
        assert isinstance(entry['hits'], int)
        assert isinstance(entry['onehour_sessions'], int)
        assert isinstance(entry['domains'], int)
        assert isinstance(entry['rootdomains'], int)

    assert count == 2


@pytest.mark.parametrize('sources,exp_count', [
    (['www.exceptionlist.com'], 1),
    (['www.exceptionlist.com', 'www.blocklist.com'], 2),
    (['inexistent_source', 'foo', 'bar'], 0),
])
def test_filterhits_load_with_filtering(sources, exp_count, filterhits_file):
    entries = load_filterhit_statistics(str(filterhits_file), sources)

    assert len(list(entries)) == exp_count


def test_filterhits_load_missing_columns(filterhits_file_missing_columns):
    entries = load_filterhit_statistics(str(filterhits_file_missing_columns))

    assert len(list(entries)) == 2
