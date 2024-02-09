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

"""Combine filter list fragments to produce filter lists."""

from __future__ import unicode_literals

import itertools
import logging
import time

from .parser import parse_filterlist, Comment, Metadata
from .sources import NotFound

__all__ = ['IncludeError', 'MissingHeader', 'render_filterlist', 'render_diff']

_logger = logging.getLogger(__name__)


class IncludeError(Exception):
    """Error in processing include instruction."""

    def __init__(self, error, stack):
        stack_str = ' from '.join(map("'{}'".format, reversed(stack)))
        if stack_str:
            error = '{} when including {}'.format(error, stack_str)
        Exception.__init__(self, error)


class MissingHeader(Exception):
    """First line of the result is not a valid header."""


def _get_and_parse_fragment(name, sources, default_source, include_stack=[]):
    """Retrieve and parse fragment.

    Returns
    -------
    tuple (iterator of str, Source)
        First part is the content of the fragment line by line; second part is
        the default source to be used for included fragments.

    """
    if ':' in name:
        source_name, name_in_source = name.split(':', 1)
        try:
            source = sources[source_name]
        except KeyError:
            raise IncludeError("Unknown source: '{}'".format(source_name),
                               include_stack)
    else:
        source, name_in_source = default_source, name

    if source is None:
        raise IncludeError("Source name is absent in: '{}'".format(name),
                           include_stack)

    return (parse_filterlist(source.get(name_in_source)),
            source if source.is_inheritable else None)


def _process_includes(sources, default_source, parent_include_stack, lines):
    """Replace include instructions with the lines of included fragment."""
    for line in lines:
        if line.type == 'include':
            name = line.target
            include_stack = parent_include_stack + [name]
            if name in parent_include_stack:
                raise IncludeError('Include loop encountered', include_stack)

            try:
                included, inherited_source = _get_and_parse_fragment(
                    name, sources, default_source, include_stack)
                all_included = _process_includes(
                    sources, inherited_source, include_stack, included)

                _logger.info('- including: %s', name)
                yield Comment(' *** {} ***'.format(name))
                for line in all_included:
                    if line.type not in {'header', 'metadata'}:
                        yield line
            except (NotFound, ValueError) as exc:
                raise IncludeError(exc, include_stack)
        else:
            yield line


def _process_timestamps(lines):
    """Convert timestamp markers into actual timestamps."""
    for line in lines:
        if line.type == 'metadata' and line.value == '%timestamp%':
            timestamp = time.strftime('%d %b %Y %H:%M UTC', time.gmtime())
            yield Metadata(line.key, timestamp)
        else:
            yield line


def _first_and_rest(iterable):
    """Return the first item from the iterable and the rest as an iterator."""
    iterator = iter(iterable)
    first_item = next(iterator)
    return first_item, iterator


def _insert_version(lines):
    """Insert metadata comment with version (a.k.a. date)."""
    first_line, rest = _first_and_rest(lines)
    version = Metadata('Version', time.strftime('%Y%m%d%H%M', time.gmtime()))
    return itertools.chain([first_line, version], rest)


def _remove_checksum(lines):
    """Remove metadata comments giving a checksum.

    Adblock Plus is no longer verifying checksums, so we don't have to
    calculate the checksum for the resulting filter list. But we have
    to strip them for compatibility with older versions of Adblock Plus
    and other ad blockers which might still verify a checksum if given.
    """
    for line in lines:
        if line.type != 'metadata' or line.key.lower() != 'checksum':
            yield line


def _validate(lines):
    """Validate the final list."""
    first_line, rest = _first_and_rest(lines)
    if first_line.type != 'header':
        raise MissingHeader('No header found at the beginning of the input.')
    return itertools.chain([first_line], rest)


def render_filterlist(name, sources, top_source=None):
    """Produce filter list from fragments.

    Parameters
    ----------
    name : str
        Name of the top level fragment.
    sources : dict of str -> Source
        Sources for loading included fragments.
    top_source : Source
        The source used to load the top level fragment.

    Returns
    -------
    iterable of namedtuple (see `_line_type` in parser.py)
        Rendered filter list.

    Raises
    ------
    IncludeError
        When an include error can't be processed.
    ParseError
        When any of the fragments contain lines that can't be parsed.
    MissingHeader
        If the top level fragment doesn't start with a valid header. This would
        lead to rendering an invalid filter list, so we immediately abort.

    """
    _logger.info('Rendering: %s', name)
    lines, default_source = _get_and_parse_fragment(name, sources, top_source)
    lines = _process_includes(sources, default_source, [name], lines)
    for proc in [_process_timestamps, _insert_version, _remove_checksum,
                 _validate]:
        lines = proc(lines)
    return lines


def _split_list_for_diff(list_in):
    """Split a filter list into metadata and rules."""
    metadata = {}
    rules = set()
    for line in parse_filterlist(list_in):
        if line.type == 'metadata':
            metadata[line.key.lower()] = line
        elif line.type == 'filter':
            rules.add(line.to_string())
    return metadata, rules


def render_diff(base, latest):
    """Return a diff between two filter lists.

    Parameters
    ----------
    base : iterator of str
        The base (old) list that we want to update to latest.
    lastest : iterator  of str
        The latest (most recent) list that we want to update to.

    Returns
    -------
    iterable of str
        A diff between two lists (https://issues.adblockplus.org/ticket/6685)

    """
    latest_metadata, latest_rules = _split_list_for_diff(latest)
    base_metadata, base_rules = _split_list_for_diff(base)

    yield '[Adblock Plus Diff]'
    for key, latest in latest_metadata.items():
        base = base_metadata.get(key)
        if not base or base.value != latest.value:
            yield latest.to_string()
    for key in set(base_metadata) - set(latest_metadata):
        yield '! {}:'.format(base_metadata[key].key)
    # The removed filters are listed first because, in case a filter is both
    # removed and added, (and the client processes the diff in order), the
    # filter will be added.
    for rule in base_rules - latest_rules:
        yield '- {}'.format(rule)
    for rule in latest_rules - base_rules:
        yield '+ {}'.format(rule)
