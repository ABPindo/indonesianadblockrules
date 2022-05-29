#!/bin/bash

# Orderer and Preener
python tools/FOP.py

# render it and save it into
flrender -i abpindo=. abpindo.template subscriptions/abpindo.txt
flrender -i abpindo=. abpindo_hosts.template subscriptions/abpindo_hosts.txt
flrender -i abpindo=. abpindo_hosts_adult.template subscriptions/abpindo_hosts_adult.txt
flrender -i abpindo=. abpindo_noadult.template subscriptions/abpindo_noadult.txt
flrender -i abpindo=. abpindo_noelemhide.template subscriptions/abpindo_noelemhide.txt

adblock2hosts --ip 0.0.0.0 -o subscriptions/hosts.txt subscriptions/abpindo_hosts.txt
adblock2hosts --ip 0.0.0.0 -o subscriptions/hosts_adult.txt subscriptions/abpindo_hosts_adult.txt

adblock2plain -o subscriptions/domain.txt subscriptions/abpindo_hosts.txt
adblock2plain -o subscriptions/domain_adult.txt subscriptions/abpindo_hosts_adult.txt

adblock2plain -o tools/domain_plain.txt subscriptions/abpindo.txt
adblock2plain --aggressive -o tools/domain_plain_aggressive.txt subscriptions/abpindo.txt

python tools/hosts_to_dnsmasq_address.py subscriptions/hosts.txt subscriptions/dnsmasq.txt
python tools/hosts_to_dnsmasq_address.py subscriptions/hosts_adult.txt subscriptions/dnsmasq_adult.txt
python tools/hosts_to_dnsmasq_server.py subscriptions/hosts.txt subscriptions/dnsmasq_server.txt
python tools/hosts_to_dnsmasq_server.py subscriptions/hosts_adult.txt subscriptions/dnsmasq_adult_server.txt

python tools/hosts_to_rpz.py subscriptions/hosts.txt subscriptions/rpz.txt
python tools/hosts_to_rpz.py subscriptions/hosts_adult.txt subscriptions/rpz_adult.txt

python tools/hosts_to_aghome.py subscriptions/hosts.txt subscriptions/aghome.txt
python tools/hosts_to_aghome.py subscriptions/hosts_adult.txt subscriptions/aghome_adult.txt

#adblock2hosts -o subscriptions/domain.txt subscriptions/abpindo_hosts.txt
#adblock2hosts -o subscriptions/domain_adult.txt subscriptions/abpindo_hosts_adult.txt

read -p "Press any key to resume ..."