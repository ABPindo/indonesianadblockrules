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

from abp.filters.sources import FSSource, NotFound


@pytest.fixture
def fssource_dir(tmpdir):
    tmpdir.mkdir('root')
    not_in_source = tmpdir.join('not-in-source.txt')
    not_in_source.write('! secret')
    root = tmpdir.join('root')
    root.mkdir('foo')
    foobar = root.join('foo', 'bar.txt')
    foobar.write('! foo/bar.txt\n! end')
    return str(root)


@pytest.fixture
def fssource(fssource_dir):
    return FSSource(fssource_dir)


def test_read_file(fssource):
    assert list(fssource.get('foo/bar.txt')) == ['! foo/bar.txt', '! end']


def test_escape_source(fssource):
    with pytest.raises(ValueError):
        list(fssource.get('../not-in-source.txt'))


def test_read_missing_file(fssource):
    with pytest.raises(NotFound):
        list(fssource.get('foo/baz.txt'))


def test_fssource_get_err(fssource):
    with pytest.raises(IOError):
        list(fssource.get(''))
