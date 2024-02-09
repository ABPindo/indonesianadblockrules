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

"""Extract blocks of filters separated by comments.

Blocks of filters separated by comments are common in real world filter lists
(e.g. easylist). This structure itself is not documented or standardized but
it's often useful to be able to parse it.

This module exports one function: to_blocks(), that further processes a filter
list (after has been parsed by abp.filters.parser) by splitting it into blocks
of filters. The comments preceeding each block are merged to produce block
description.

Some filter lists (e.g. ABP exception list) also make use of variable notation
("!:varname=value") to define specific attributes of filters blocks. This
module supports this notation and will collect those variables in a dictionary
that's placed into `variables` attribute of the block. If variables are present
in comments preceeding a block, only non-variable comments that follow the
first variable declaration will be included into the block description.

Blocks also provide a method to convert them to dictionaries: .to_dict() --
this can be used for JSON conversion.

Example
-------

The following code will dump the blocks as dictionaries:

    from abp.filters import parse_filterlist
    from abp.filters.blocks import to_blocks

    with open(fl_path) as f:
        for block in to_blocks(parse_filterlist(f)):
            print(block.to_dict())

This will produce output like this:

    {'variables': {'partner_token': 'abc', 'partner_id': '3372',
     'type': 'partner'}, 'description': 'Some comments', 'filters': [...]}

"""

from __future__ import unicode_literals

import re

__all__ = ['to_blocks']

VAR_REGEXP = re.compile(r'^:(\w+)=(.*)$')


class FiltersBlock(object):
    """A block of filters (preceded by comments)."""

    def __init__(self, comments, filters):
        """Create a filter block from filters and comments preceding them."""
        self.filters = filters
        self.variables = {}
        descr_lines = []

        for comment in comments:
            match = VAR_REGEXP.search(comment.text)
            if match:
                if not self.variables:
                    # Normal comments before first variable are not included in
                    # the description.
                    descr_lines = []
                name, value = match.groups()
                self.variables[name] = value
            else:
                descr_lines.append(comment.text)

        self.description = '\n'.join(descr_lines)

    def to_dict(self):
        ret = dict(self.__dict__)
        ret['filters'] = [f.to_dict() for f in ret['filters']]
        return ret


def to_blocks(parsed_lines):
    """Convert a sequence of parser filter list lines to blocks.

    Parameters
    ----------
    parsed_lines : iterable of namedtuple
        Parsed filter list (see `parser.py` for details on how it's
        represented).

    Returns
    -------
    blocks : iterable of FiltersBlock.
        Blocks extracted from the parsed filter list. Each block carries
        filters in `.filters` attribute, comments in `.description` attribute
        and variable-defining comments in `.variables`.

    """
    comments = []
    filters = []

    for line in parsed_lines:
        if line.type == 'comment':
            if filters:
                yield FiltersBlock(comments, filters)
                comments = []
                filters = []
            comments.append(line)
        elif line.type == 'filter':
            filters.append(line)

    if filters:
        yield FiltersBlock(comments, filters)
