#!/bin/bash

flrender -i abpindo=. tools/validatehost/host.template tools/validatehost/host.txt

python tools/validatehost/validatehost.py
