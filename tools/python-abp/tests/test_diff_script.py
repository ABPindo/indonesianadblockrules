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

"""Functional tests for the diff script."""

from __future__ import unicode_literals

import pytest
import subprocess
import io
import os
import re

from test_differ import BASE, LATEST


@pytest.fixture
def rootdir(tmpdir):
    """Root directory for test files."""
    rootdir = tmpdir.join('root')
    rootdir.mkdir()
    rootdir.join('latest.txt').write_text(LATEST, encoding='utf8')
    return rootdir


@pytest.fixture
def archive_dir(rootdir):
    return rootdir.mkdir('archive')


@pytest.fixture
def diff_dir(rootdir):
    return rootdir.mkdir('diff')


@pytest.fixture
def archived_files(archive_dir):
    base2 = BASE + '&adnet=\n'
    base2 = re.sub(r'! Version: \d+', '! Version: 112', base2)
    archive_dir.join('list111.txt').write_text(BASE, encoding='utf8')
    archive_dir.join('list112.txt').write_text(base2, encoding='utf8')
    return [str(x) for x in archive_dir.listdir()]


@pytest.fixture
def base_no_version(archive_dir):
    base = re.sub(r'! Version: \d+', '! ', BASE)
    archive_dir.join('list113.txt').write_text(base, encoding='utf8')
    return [str(x) for x in archive_dir.listdir()]


def run_script(*args, **kw):
    """Run diff rendering script with given arguments and return its output."""
    cmd = ['fldiff'] + list(args)

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            **kw)
    stdout, stderr = proc.communicate()
    return proc.returncode, stderr.decode('utf-8'), stdout.decode('utf-8')


def test_diff_with_outfile(rootdir, archived_files, diff_dir):
    run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir),
               *archived_files)
    assert len(diff_dir.listdir()) == 2
    for file in diff_dir.visit():
        with io.open(str(file), encoding='utf-8') as dst:
            result = dst.read()
        assert '- &ad.vid=$~xmlhttprequest' in result
        assert '+ &ad_channel=\xa3' in result
        assert '! Version: 123' in result


def test_diff_no_outfile(rootdir, archived_files):
    os.chdir(str(rootdir))
    run_script(str(rootdir.join('latest.txt')), *archived_files)
    for file in ['diff111.txt', 'diff112.txt']:
        with io.open(file, encoding='utf-8') as dst:
            result = dst.read()
        assert '- &ad.vid=$~xmlhttprequest' in result
        assert '+ &ad_channel=\xa3' in result
        assert '! Version: 123' in result


def test_no_base_file(rootdir):
    code, err, _ = run_script(str(rootdir.join('latest.txt')))
    assert code == 2
    assert 'usage: fldiff' in err


def test_wrong_file(rootdir):
    code, err, _ = run_script(str(rootdir.join('base.txt')), 'wrong.txt')
    assert code == 1
    assert 'No such file or directory' in err


def test_diff_to_self(rootdir, diff_dir):
    run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir),
               str(rootdir.join('latest.txt')))
    assert len(diff_dir.listdir()) == 1
    for file in diff_dir.visit():
        with io.open(str(file), encoding='utf-8') as dst:
            result = dst.read()
        assert result == '[Adblock Plus Diff]\n'


def test_no_version(rootdir, base_no_version):
    code, err, _ = run_script(str(rootdir.join('latest.txt')), '-o',
                              str(diff_dir), *base_no_version)
    assert code == 1
    assert 'Unable to find Version in ' in err


def test_write_and_overwrite(rootdir, archived_files, diff_dir):
    test_diff_with_outfile(rootdir, archived_files, diff_dir)
    latest = re.sub(r'&act=ads_', '! ', BASE) + '&adurl=\n'
    rootdir.join('latest.txt').write_text(latest, encoding='utf8')
    run_script(str(rootdir.join('latest.txt')), '-o', str(diff_dir),
               *archived_files)
    assert len(diff_dir.listdir()) == 2
    for file in diff_dir.visit():
        with io.open(str(file), encoding='utf-8') as dst:
            result = dst.read()
        assert '- &act=ads_' in result
        assert '+ &adurl=' in result
        assert '- &ad.vid=$~xmlhttprequest' not in result
