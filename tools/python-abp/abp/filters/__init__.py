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

"""Tools for working with Adblock Plus filter lists.

This is a library for parsing and rendering filter lists that are used by
adblocking software to determine what content to block and what to let through.

Example
-------

    from abp.filters import parse_filterlist

    with open(fl_path, 'rt') as fl_file:
        for line in parse_filterlist(fl_file):
            if line.type == 'filter':
                print('Filter:' + line.text)
                print('| Selector: {0[type]}:{0[value]}'.format(line.selector))
                print('| Action: ' + line.action)
                for key, value in line.options:
                    print('| Option[{}]: {}'.format(key, value))

Exported members
----------------

Functions:

  - parse_filterlist - Parse a filter list from an iterable of strings.
  - parse_line - Parse one line of a filter list.
  - render_filterlist - Combine filter list fragments into a filter list.

Filter list fragment sources for filter list rendering:

  - WebSource - loads fragments from the web.
  - FSSource - loads fragments from a directory on the filesystem.
  - TopSource - a specialized FSSource that represents current directory and
    should be used as the starting source of render_filterlist.

Exceptions that thrown by the functions in this module:

  - ParseError - thrown by the parser when invalid input is encountered.
  - IncludeError - thrown by the renderer when an include instruction cannot
    be processed.
  - MissingHeader - thrown by the renderer when the output doesn't start with a
    header.

Constants for code that works with filter lists:

  - SelectorType - Namespace for constants that determine how the filter
    matches content (for example: SelectorType.CSS):

    - URL_PATTERN - Match URL against a pattern (see
      https://adblockplus.org/filters#basic),
    - URL_REGEXP - Match URL against a regular expression,
    - CSS - Select elements via a CSS selector,
    - XCSS - CSS selector with extensions (to emulate CSS4),
    - ABP_SIMPLE - Deprecated simplified element selection syntax.

  - FilterAction - Namespace for constants that determine what the filter does
    with selected content (for example: FilterAction.BLOCK):

    - BLOCK - Block the request,
    - ALLOW - Allow the request (even if blocked by other filters),
    - HIDE - Hide selected element,
    - SHOW - Show selected element (even if hidden by other filters).

  - FilterOption - Namespace for filter option constants (for example
    FilterOption.IMAGE). See https://adblockplus.org/filters#options for the
    full list of options.

See docstrings of module members for further information.

Notes
-----
`str` in function and method signatures always means a unicode string (Python3
meaning of `str`).

"""

from .parser import (
    FilterAction,
    FilterOption,
    SelectorType,
    ParseError,
    parse_filterlist,
    parse_line,
)
from .renderer import (
    IncludeError,
    MissingHeader,
    render_filterlist,
)
from .sources import (
    FSSource,
    TopSource,
    WebSource,
)

__all__ = [
    # Constants
    'FilterAction',
    'FilterOption',
    'SelectorType',
    # Exceptions
    'ParseError',
    'IncludeError',
    'MissingHeader',
    # File sources
    'FSSource',
    'TopSource',
    'WebSource',
    # Functions
    'parse_filterlist',
    'parse_line',
    'render_filterlist',
]
