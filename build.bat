TITLE render ABPindo

ECHO OFF 
python tools/FOP.py

flrender -i abpindo=. abpindo.template subscriptions/abpindo.txt
flrender -i abpindo=. abpindo_noannoyance.template subscriptions/abpindo_noannoyance.txt
flrender -i abpindo=. abpindo_noelemhide.template subscriptions/abpindo_noelemhide.txt
flrender -i abpindo=. tools/validatehost/host.template tools/validatehost/host.txt
