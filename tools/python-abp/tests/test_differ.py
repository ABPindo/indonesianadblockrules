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

from abp.filters.renderer import render_diff

BASE = '''[Adblock Plus 2.0]
! Version: 111
! diff-url: https://easylist-downloads.adblockplus.org/easylist/diffs/111.txt
! diff-expires: 1 hours
! Title: EasyList
! Expires: 1 days (update frequency)
! Homepage: https://easylist.to/
! Licence: https://easylist.to/pages/licence.html
!
! Please report any unblocked adverts or problems
! in the forums (https://forums.lanik.us/)
! or via e-mail (easylist.subscription@gmail.com).
!
!-----------------------General advert blocking filters-----------------------!
! *** easylist:easylist/easylist_general_block.txt ***
test
&act=ads_
&ad.vid=$~xmlhttprequest
&ad_box_
'''

LATEST = '''[Adblock Plus 2.0]
! Version: 123
! Diff-URL: https://easylist-downloads.adblockplus.org/easylist/diffs/123.txt
! Diff-Expires: 1 hours
! Title: EasyList
! Homepage: https://easylist.to/
! Licence: https://easylist.to/pages/licence.html
!
! Please report any unblocked adverts or problems
! in the forums (https://forums.lanik.us/)
! or via e-mail (easylist.subscription@gmail.com).
!
!-----------------------General advert blocking filters-----------------------!
! *** easylist:easylist/easylist_general_block.txt ***
&act=ads_
&ad_box_
&ad_channel=\U000000a3
 test
&test_
'''


EXPECTED = '''[Adblock Plus Diff]
! Diff-URL: https://easylist-downloads.adblockplus.org/easylist/diffs/123.txt
! Expires:
! Version: 123
- &ad.vid=$~xmlhttprequest
+ &ad_channel=\U000000a3
+ &test_
'''


def test_differ():
    exp = set(EXPECTED.splitlines())
    gen = set(render_diff(BASE.splitlines(), LATEST.splitlines()))
    assert(gen == exp)
