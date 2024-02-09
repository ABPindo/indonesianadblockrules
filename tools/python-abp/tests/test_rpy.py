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

"""Functional tests for testing rPython integration."""

from collections import namedtuple
import pytest

from abp.filters.rpy import line2dict, lines2dicts


_SAMPLE_TUPLE = namedtuple('tuple', 'foo,bar')

_TEST_EXAMPLES = {
    'header': {
        'in': '[Adblock Plus 2.0]',
        'out': {
            'type': 'Header',
            'version': 'Adblock Plus 2.0',
        },
    },
    'metadata': {
        'in': '! Title: Example list',
        'out': {
            'type': 'Metadata',
            'key': 'Title',
            'value': 'Example list',
        },
    },
    'comment': {
        'in': '! Comment',
        'out': {
            'type': 'Comment',
            'text': 'Comment',
        },
    },
    'empty': {
        'in': '',
        'out': {
            'type': 'EmptyLine',
        },
    },
    'include': {
        'in': '%include www.test.py/filtelist.txt%',
        'out': {
            'type': 'Include',
            'target': 'www.test.py/filtelist.txt',
        },
    },
    'filter_single': {
        'in': 'foo.com##div#ad1',
        'out': {
            'type': 'Filter',
            'text': 'foo.com##div#ad1',
            'selector': {'type': 'css', 'value': 'div#ad1'},
            'action': 'hide',
            'options': {'domain': {'foo.com': True}},
        },
    },
    'filter_with_%': {
        'in': '%22banner%*%22idzone%',
        'out': {
            'type': 'Filter',
            'text': '%22banner%*%22idzone%',
            'selector': {'type': 'url-pattern',
                         'value': '%22banner%*%22idzone%'},
            'action': 'block',
            'options': {},
        },
    },
    'filter_multiple': {
        'in': 'foo.com,bar.com##div#ad1',
        'out': {
            'type': 'Filter',
            'text': 'foo.com,bar.com##div#ad1',
            'selector': {'type': 'css', 'value': 'div#ad1'},
            'action': 'hide',
            'options': {'domain': {'foo.com': True, 'bar.com': True}},
        },
    },
    'filter_with_sitekey_list': {
        'in': '@@bla$ping,domain=foo.com|~bar.foo.com,sitekey=foo|bar',
        'out': {
            'text':
                '@@bla$ping,domain=foo.com|~bar.foo.com,sitekey=foo|bar',
                'selector': {'value': 'bla', 'type': 'url-pattern'},
                'action': 'allow',
                'options': {
                    'ping': True,
                    'domain': {'foo.com': True,
                               'bar.foo.com': False},
                    'sitekey': ['foo', 'bar']},
                'type': 'Filter',
        },
    },
}


@pytest.mark.parametrize('line_type', list(_TEST_EXAMPLES.keys()))
def test_line2dict_format(line_type):
    """Test that the API result has the appropriate format.

    Checks for both keys and datatypes.
    """
    position = 'start' if line_type in {'header', 'metadata'} else 'body'
    data = line2dict(_TEST_EXAMPLES[line_type]['in'], position)

    assert data == _TEST_EXAMPLES[line_type]['out']


def test_lines2dicts_start_mode():
    """Test that the API returns the correct result in the appropriate format.

    Checks for 'start' mode, which can handle headers and metadata.
    """
    tests = [t for t in _TEST_EXAMPLES.values()]
    ins = [ex['in'] for ex in tests]
    outs = [ex['out'] for ex in tests]

    assert lines2dicts(ins, 'start') == outs


def test_lines2dicts_default():
    """Test that the API returns the correct result in the appropriate format.

    By default, lines2dicts() does not correctly parse headers and metadata.
    """
    tests = [t for t in _TEST_EXAMPLES.values()
             if t['out']['type'] not in {'Header', 'Metadata'}]
    ins = [ex['in'] for ex in tests]
    outs = [ex['out'] for ex in tests]

    assert lines2dicts(ins) == outs
