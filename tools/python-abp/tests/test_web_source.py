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

try:
    from StringIO import StringIO
    from urllib2 import HTTPError
except ImportError:  # The modules were renamed/moved in Python 3.
    from io import BytesIO as StringIO
    from urllib.error import HTTPError

from abp.filters.sources import WebSource, NotFound


@pytest.fixture
def web_mock(request):
    """Replace urlopen with our test implementation."""
    patcher = mock.patch('abp.filters.sources.urlopen')
    ret = patcher.start()
    request.addfinalizer(patcher.stop)
    return ret


@pytest.fixture
def http_source():
    return WebSource('http')


def response_mock(encoding, data):
    """Make a fake response with specific encoding and content."""
    resp = StringIO(data)
    info = mock.Mock()
    info.get_param = mock.Mock(return_value=encoding)
    resp.info = mock.Mock(return_value=info)
    return resp


def test_fetch_file(web_mock, http_source):
    web_mock.return_value = response_mock(None, b'! Line 1\n! Line 2')
    assert list(http_source.get('//foo/bar.txt')) == ['! Line 1', '! Line 2']


def test_charset_handling(web_mock, http_source):
    web_mock.return_value = response_mock('latin-1', b'\xfc')
    assert list(http_source.get('//foo/bar.txt')) == ['\xfc']
    web_mock.return_value = response_mock('utf-8', b'\xc3\xbc')
    assert list(http_source.get('//foo/bar.txt')) == ['\xfc']
    web_mock.return_value = response_mock(None, b'\xc3\xbc')
    assert list(http_source.get('//foo/bar.txt')) == ['\xfc']


def test_404(web_mock, http_source):
    web_mock.side_effect = HTTPError('', 404, 'Not found', [], StringIO(b''))
    with pytest.raises(NotFound):
        list(http_source.get('//foo/bar.txt'))


def test_500(web_mock, http_source):
    web_mock.side_effect = HTTPError('', 500, 'Internal Server Error', [],
                                     StringIO(b''))
    with pytest.raises(HTTPError):
        list(http_source.get('//foo/bar.txt'))
