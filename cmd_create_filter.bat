@echo off
:: Firefox
echo Sort Firefox Subscriptions...
perl sorter.pl abpindo_specific_block.txt
perl sorter.pl abpindo_adservers.txt
perl sorter.pl abpindo_general_block.txt
perl sorter.pl abpindo_general_hide.txt
perl sorter.pl abpindo_noelemhide.txt
perl sorter.pl abpindo_specific_block.txt
perl sorter.pl abpindo_specific_hide.txt
perl sorter.pl abpindo_thirdparty.txt
perl sorter.pl abpindo_whitelist.txt
perl sorter.pl _longcat.txt
perl sorter.pl _computer_prank.txt
C:\strawberry\perl\bin\perl generate_subscriptions.pl
hgtk commit