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

"""Functional tests for the rendering script.

These tests create files on the filesystem, bring up a small webserver and
generally test the script under reasonably realistic conditions.
"""

from __future__ import unicode_literals

import os
import pytest
import subprocess
import threading

try:
    import SimpleHTTPServer
    import SocketServer
except ImportError:  # The modules were renamed/moved in Python 3.
    from http import server as SimpleHTTPServer  # noqa: N812
    import socketserver as SocketServer  # noqa: N812


@pytest.fixture
def rootdir(tmpdir):
    """Directory with prepared list fragments."""
    rootdir = tmpdir.join('root')
    rootdir.mkdir()
    # Simple file with just `Ok` and a non-ascii unicode character in it.
    rootdir.join('simple.txt').write('[Adblock]\nOk')
    # Fragment with a non-ascii character.
    rootdir.join('unicode.txt').write(
        '[Adblock]\n\u1234'.encode('utf-8'), mode='wb')
    # Fragment with an include.
    rootdir.join('includer.txt').write('[Adblock]\n%include inc:includee.txt%')
    # Fragment that includes a circular include file.
    rootdir.join('circ.txt').write('[Adblock]\n%include inc:circular.txt%')
    # Fragment that includes a file with broken include.
    rootdir.join('brk.txt').write('[Adblock]\n%include inc:broken.txt%')
    # Source directory for includes.
    incdir = rootdir.join('inc')
    incdir.mkdir()
    # Fragment that's included into includer.txt.
    incdir.join('includee.txt').write('I am included!')
    # Fragment that has a broken include.
    incdir.join('broken.txt').write('%include missing.txt%')
    # Fragment that includes itself.
    incdir.join('circular.txt').write('%include circular.txt%')
    return rootdir


@pytest.fixture
def webserver_port(tmpdir, request):
    """Serve fragments via HTTP on a random port (return the port number)."""
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(('', 0), handler)
    port = httpd.socket.getsockname()[1]
    # Create some files to serve.
    webroot = tmpdir.join('webroot')
    webroot.mkdir()
    webroot.join('inc.txt').write('Web \u1234'.encode('utf-8'), mode='wb')
    webroot.join('metainc.txt').write(
        '%include http://localhost:{}/inc.txt%'.format(port))
    # Change to this directory and start the webserver in another thread.
    os.chdir(str(webroot))
    thread = threading.Thread(target=httpd.serve_forever)
    thread.setDaemon(True)
    thread.start()
    # Make sure we shut it down at the end of the test.
    request.addfinalizer(httpd.shutdown)
    return port


@pytest.fixture
def dstfile(tmpdir):
    """Destination file for saving rendered list."""
    return tmpdir.join('dst')


def run_script(*args, **kw):
    """Run rendering script with given arguments and return its output."""
    cmd = ['flrender'] + list(args)

    test_in = kw.pop('test_in', None)
    if test_in is not None:
        test_in = test_in.encode('utf-8')

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            **kw)
    stdout, stderr = proc.communicate(input=test_in)
    return proc.returncode, stderr.decode('utf-8'), stdout.decode('utf-8')


@pytest.mark.parametrize('test_input, args', [
    ('None', ["'simple.txt'", 'str(dstfile)']),
    ('None', ["'simple.txt'"]),
    ("rootdir.join('simple.txt').read()", []),
])
def test_render_no_includes(test_input, args, rootdir, dstfile):
    test_input = eval(test_input)
    args = list(map(eval, args))
    _, _, stdout = run_script(*args, cwd=str(rootdir), test_in=test_input)

    if len(args) > 1:
        output = dstfile.read()
    else:
        output = stdout

    assert 'Ok' in output


def test_render_unicode(rootdir, dstfile):
    code, err, _ = run_script(str(rootdir.join('unicode.txt')), str(dstfile))
    assert '\u1234' in dstfile.read(mode='rb').decode('utf-8')


def test_render_with_includes(rootdir, dstfile):
    run_script(str(rootdir.join('includer.txt')), str(dstfile),
               '-i', 'inc=' + str(rootdir.join('inc')))
    assert 'I am included!' in dstfile.read()


def test_render_with_includes_relative(rootdir, dstfile):
    run_script('includer.txt', str(dstfile), '-i', 'inc=inc', cwd=str(rootdir))
    assert 'I am included!' in dstfile.read()


def test_render_verbose(rootdir, dstfile):
    code, err, _ = run_script('includer.txt', str(dstfile),
                              '-i', 'inc=inc', '-v', cwd=str(rootdir))
    assert err == 'Rendering: includer.txt\n- including: inc:includee.txt\n'


def test_no_header(rootdir, dstfile):
    code, err, _ = run_script('inc/includee.txt', str(dstfile),
                              cwd=str(rootdir))
    assert code == 1
    assert err == 'No header found at the beginning of the input.\n'


def test_wrong_file(dstfile):
    code, err, _ = run_script('wrong.txt', str(dstfile))
    assert code == 1
    assert err == "File not found: 'wrong.txt'\n"


def test_wrong_include_source(rootdir, dstfile):
    code, err, _ = run_script('brk.txt', str(dstfile), cwd=str(rootdir))
    assert code == 1
    assert err == ("Unknown source: 'inc' when including 'inc:broken.txt' "
                   "from 'brk.txt'\n")


def test_wrong_include(rootdir, dstfile):
    code, err, _ = run_script('brk.txt', str(dstfile),
                              '-i', 'inc=inc', cwd=str(rootdir))
    missing_path = str(rootdir.join('inc', 'missing.txt'))
    expect = ("File not found: '{}' when including 'missing.txt' "
              "from 'inc:broken.txt' from 'brk.txt'\n").format(missing_path)
    assert code == 1
    assert err == expect


def test_circular_includes(rootdir, dstfile):
    code, err, _ = run_script('circ.txt', str(dstfile),
                              '-i', 'inc=inc', cwd=str(rootdir))
    expect = ("Include loop encountered when including 'circular.txt' "
              "from 'circular.txt' from 'inc:circular.txt' from 'circ.txt'\n")
    assert code == 1
    assert err == expect


def test_wrong_source(rootdir, dstfile):
    code, err, _ = run_script('foo:bar.txt', str(dstfile))
    assert code == 1
    assert err == "Unknown source: 'foo'\n"


@pytest.mark.tryfirst
@pytest.mark.slowtest
def test_web_include(rootdir, dstfile, webserver_port):
    url = 'http://localhost:{}/metainc.txt'.format(webserver_port)
    webinc = rootdir.join('webinc.txt')
    webinc.write('[Adblock]\n%include {}%'.format(url))
    code, err, _ = run_script(str(webinc), str(dstfile))
    assert 'Web \u1234' in dstfile.read(mode='rb').decode('utf-8')


@pytest.mark.slowtest
def test_failed_web_include(rootdir, dstfile, webserver_port):
    url = 'http://localhost:{}/missing.txt'.format(webserver_port)
    webinc = rootdir.join('webinc.txt')
    webinc.write('[Adblock]\n%include {}%'.format(url))
    code, err, _ = run_script(str(webinc), str(dstfile))
    assert code == 1
    assert err.startswith(
        "HTTP 404 Not found: '{0}' when including '{0}'".format(url))
