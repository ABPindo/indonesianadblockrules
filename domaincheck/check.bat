@echo off > gooddomains.log
for /f %%I in (DomainList.txt) do (
ping %%I > %temp%\#
find "Reply" < %temp%\# > nul
if errorlevel 1 (
	echo 
) else (
	echo %%I Reachable >> gooddomains.log
)
type %temp%\# >> all.log
)