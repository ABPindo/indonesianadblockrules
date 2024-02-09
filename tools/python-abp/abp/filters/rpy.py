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

"""
Functions for integrating with rPython.

see: https://cran.r-project.org/web/packages/rPython/index.html
"""

from abp.filters import parse_line

__all__ = ['line2dict']


def line2dict(text, mode='body'):
    """Convert a filterlist line to a dictionary.

    All strings in the output dictionary will be UTF8 byte strings. This is
    necessary to prevent unicode encoding errors in rPython conversion layer.

    Parameters
    ----------
    text: str
        The filter text we want to parse
    mode: str
        Parsing mode (see `abp.filters.parser.parse_line`).

    Returns
    -------
    dict
        With the parsing results and all strings converted to utf8 byte
        strings.

    """
    return parse_line(text, mode).to_dict()


def lines2dicts(string_list, mode='body'):
    """Convert a list of filterlist strings to a dictionary.

    All strings in the output dictionary will be UTF8 byte strings. This is
    necessary to prevent unicode encoding errors in rPython conversion layer.

    Parameters
    ----------
    string_list: iterable of str
        Each string in the list can be an empty line, include instruction, or
        filter. If the mode is 'start', headers and metadata can also be
        parsed.
    mode: str
        Parsing mode (see `abp.filters.parser.parse_line`).

    Returns
    -------
    list of dict
        With the parsing results and all strings converted to utf8 byte
        strings.

    """
    result = []
    for string in string_list:
        result.append(line2dict(string, mode))
    return result
