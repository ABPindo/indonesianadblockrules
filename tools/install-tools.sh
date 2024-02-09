#!/bin/bash

# A script for rendering diffs between filter lists, and the script that is
# used for building Adblock Plus filter lists from the form in which they are
# authored into the format suitable for consumption by the adblocking software
# (aka rendering). Adapted from the `python-abp` project.
pip install -e tools/python-abp

# A set of tools for the decoding and conversion of AdBlock and filter lists.
# The decoder itself is part of the PyFunceble project.
pip install adblock-decoder

read -p "Press any key to resume ..."