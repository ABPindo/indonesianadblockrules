#!/bin/bash

# Orderer and Preener
python tools/FOP.py

# render it and save it into
flrender -i abpindo=. abpindo.template subscriptions/abpindo.txt
flrender -i abpindo=. abpindo_hosts.template subscriptions/hosts.txt
flrender -i abpindo=. abpindo_noannoyance.template subscriptions/abpindo_noannoyance.txt
flrender -i abpindo=. abpindo_noelemhide.template subscriptions/abpindo_noelemhide.txt

