@echo off
:: Firefox
C:\strawberry\perl\bin\perl generate_subscriptions.pl
FOP.py
hgtk commit