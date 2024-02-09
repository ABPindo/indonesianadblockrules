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

from __future__ import unicode_literals

import pytest
import mock
import time

from abp.filters import render_filterlist, MissingHeader, IncludeError


@pytest.fixture()
def gmtime(request):
    """Patch time.gmtime to freeze timestamps."""
    patcher = mock.patch('time.gmtime')
    gmtime_mock = patcher.start()
    request.addfinalizer(patcher.stop)
    gmtime_mock.return_value = time.struct_time([2001] + [1] * 8)
    return gmtime_mock


@pytest.fixture()
def head(gmtime):
    """Typical start of the rendered list."""
    version = time.strftime('%Y%m%d%H%M', gmtime())
    return '[Adblock]\n! Version: {}\n'.format(version)


class MockSource(object):

    def __init__(self, **kw):
        self.is_inheritable = kw.get('is_inheritable', True)
        self.files = kw

    def get(self, filename):
        return self.files[filename].split('\n')


def render_str(*args, **kw):
    return '\n'.join(l.to_string() for l in render_filterlist(*args, **kw))


def test_simple_render(head):
    src = MockSource(fl='[Adblock]\n! Comment.')
    got = render_str('fl', {}, src)
    assert got == head + '! Comment.'


def test_include(head):
    src = MockSource(fl='[Adblock]\n%include src:inc%', inc='!:foo=bar')
    got = render_str('src:fl', {'src': src})
    assert got.startswith(head + '! *** src:inc ***\n! :foo=bar')


def test_include2(head):
    src1 = MockSource(fl='[Adblock]\n%include inc1%',
                      inc1='%include src2:inc2%')
    src2 = MockSource(inc2='%include inc3%', inc3='Included')
    got = render_str('src1:fl', {'src1': src1, 'src2': src2})
    expect = (
        head + '! *** inc1 ***\n! *** src2:inc2 ***\n! *** inc3 ***\nIncluded'
    )
    assert got.startswith(expect)


def test_circular_includes():
    src = MockSource(fl='[Adblock]\n%include src:fl%')
    with pytest.raises(IncludeError):
        render_str('src:fl', {'src': src})


def test_timestamp(gmtime):
    src = MockSource(fl='[Adblock]\n! Last modified: %timestamp%')
    got = render_str('fl', {}, src)
    assert time.strftime('Last modified: %d %b %Y %H:%M UTC', gmtime()) in got


def test_wrong_source():
    src = MockSource(fl='[Adblock]\n%include missing:fl%')
    with pytest.raises(IncludeError):
        render_str('fl', {}, src)


def test_missing_top_source():
    with pytest.raises(IncludeError):
        render_str('fl', {})


def test_deduplication():
    src = MockSource(
        fl='[Adblock]\n! Title: foo\n%include inc1%',
        inc1='[Adblock]\n! Title: bar\nfilter')
    got = render_str('fl', {}, src)
    assert '! Title: foo\n! *** inc1 ***\nfilter' in got


def test_source_non_inheritance():
    src1 = MockSource(fl='[Adblock]\n%include src2:inc1%')
    src2 = MockSource(is_inheritable=False,
                      inc1='%include inc2%', inc2='Included')
    with pytest.raises(IncludeError):
        render_str('src1:fl', {'src1': src1, 'src2': src2})


def test_missing_header():
    src = MockSource(fl='! No header')
    with pytest.raises(MissingHeader):
        render_str('fl', {}, src)


def test_remove_checksum(head):
    src = MockSource(fl='[Adblock]\n! Comment\n! Checksum: foo')
    got = render_str('fl', {}, src)
    assert got == head + '! Comment'
