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

"""Helper classes that handle IO for filter list parsing and rendering."""

import io
from os import path
import sys

try:
    from urllib2 import urlopen, HTTPError
except ImportError:  # pragma: no py2 cover
    from urllib.request import urlopen
    from urllib.error import HTTPError

__all__ = ['NotFound', 'FSSource', 'TopSource', 'WebSource']


class NotFound(Exception):
    """Requested file doesn't exist in this source.

    The file with requested name doesn't exist. If this results from an
    include, the including list probably contains an error.
    """


class FSSource(object):
    """Directory on the filesystem.

    Parameters
    ----------
    root_path : str
        The path to the directory.
    encoding : str
        Encoding to use for reading the files (default: utf-8).

    """

    is_inheritable = True

    def __init__(self, root_path, encoding='utf-8'):
        root_path = path.abspath(root_path)
        self.root_path = root_path
        self.encoding = encoding

    def _resolve_path(self, path_in_source):
        parts = path_in_source.split('/')
        full_path = path.abspath(path.join(self.root_path, *parts))
        if not full_path.startswith(self.root_path):
            raise ValueError("Invalid path: '{}'".format(path_in_source))
        return full_path

    def get(self, path_in_source):
        """Read file from the source.

        Parameters
        ----------
        path_in_source : str
            Path to the file inside of the source.

        Returns
        -------
        iterable of str
            Lines of the file.

        """
        full_path = self._resolve_path(path_in_source)
        try:
            with io.open(full_path, encoding=self.encoding) as open_file:
                for line in open_file:
                    yield line.rstrip()
        except IOError as exc:
            if exc.errno == 2:  # No such file or directory.
                raise NotFound("File not found: '{}'".format(full_path))
            raise exc


class TopSource(FSSource):
    """Current directory without path conversion.

    Also supports absolute paths. This source is used for the top fragment.

    Parameters
    ----------
    encoding : str
        Encoding to use for reading the files (default: utf-8).

    """

    is_inheritable = False

    def __init__(self, encoding='utf-8'):
        super(TopSource, self).__init__('.', encoding)

    def _resolve_path(self, path_in_source):
        return path_in_source

    def get(self, path_in_source):
        """Read the data. Handles stdin, on top of file input.

        Parameters
        ----------
        path_in_source : str
            Path to the file inside of source or '-' for stdin.

        Returns
        -------
        generator or str
            Lines in the file/ from stdin.

        """
        if path_in_source == '-':
            lines = sys.stdin.readlines()
            for line in lines:
                yield line.rstrip('\n')
        else:
            lines = super(TopSource, self).get(path_in_source)
            for line in lines:
                yield line


class WebSource(object):
    """Handler for http or https.

    Parameters
    ----------
    protocol : str
        Protocol to use: "http" or "https".
    default_encoding : str
        Encoding to use when the server doesn't specify it (default: utf-8).

    """

    is_inheritable = False

    def __init__(self, protocol, default_encoding='utf-8'):
        self.protocol = protocol
        self.default_encoding = default_encoding

    def get(self, path_in_source):
        """Read file from the source.

        Parameters
        ----------
        path_in_source : str
            The rest of the URL after "http(s):".

        Returns
        -------
        iterable of str
            Lines of the file.

        """
        url = '{}:{}'.format(self.protocol, path_in_source)
        try:
            response = urlopen(url)
            info = response.info()
            # info.getparam became info.get_param in Python 3 so we'll
            # try both.
            get_param = (getattr(info, 'get_param', None)
                         or getattr(info, 'getparam', None))
            encoding = get_param('charset') or self.default_encoding
            for line in response:
                yield line.decode(encoding).rstrip()
        except HTTPError as err:
            if err.code == 404:
                raise NotFound("HTTP 404 Not found: '{}:{}'"
                               .format(self.protocol, path_in_source))
            raise err
