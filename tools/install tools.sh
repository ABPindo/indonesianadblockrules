#!/bin/bash

# a script for rendering diffs between filter lists, and the script that is used for building Adblock Plus filter lists from the form in which they are authored into the format suitable for consumption by the adblocking software (aka rendering).
# https://github.com/adblockplus/python-abp
pip install --upgrade python-abp

# A set of tools for the decoding and conversion of AdBlock and filter lists. The decoder itself is part of the PyFunceble project.
# https://github.com/PyFunceble/adblock-decoder
pip install adblock-decoder

# This is a simple tool that checks adblock filtering rules for dead domains.
# https://github.com/AdguardTeam/DeadDomainsLinter
npm i -g @adguard/dead-domains-linter

# FOP - Filter Orderer and Preener (Rust Edition)
# https://github.com/ryanbr/fop-rs
npm install -g fop-cli

read -p "Press any key to resume ..."