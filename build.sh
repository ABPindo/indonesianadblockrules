#!/bin/bash

# Orderer and Preener
python tools/FOP.py

# render it and save it into
flrender -i abpindo=. abpindo.template subscriptions/abpindo.txt
flrender -i abpindo=. abpindo_hosts.template subscriptions/abpindo_hosts.txt
flrender -i abpindo=. abpindo_hosts_annoyance.template subscriptions/abpindo_hosts_annoyance.txt
flrender -i abpindo=. abpindo_noannoyance.template subscriptions/abpindo_noannoyance.txt
flrender -i abpindo=. abpindo_noelemhide.template subscriptions/abpindo_noelemhide.txt

adblock2hosts --ip 0.0.0.0 -o subscriptions/hosts.txt subscriptions/abpindo_hosts.txt
adblock2hosts --ip 0.0.0.0 -o subscriptions/hosts_annoyance.txt subscriptions/abpindo_hosts_annoyance.txt

read -p "Press any key to resume ..."