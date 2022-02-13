# source: https://gist.github.com/iam-py-test/ba35ce681e195c690ea3590f79479a3b
# how to use: domains_to_dnsmasq hosts-input.txt hosts-output.txt

import os
import sys


# check if we have the right amount of args
if len(sys.argv) != 3:
	# we don't, so print a help message and exit
	print("Wrong number of arguments.\nHelp: {} {} [input file] [output file]".format(sys.executable,sys.argv[0]))
	sys.exit()
else:
	print("Generating the dnsmasq_address version from domains file {}...".format(sys.argv[1]))
	domainsfile = open(sys.argv[1],"r")
	outputfile = open(sys.argv[2],"w")
	lines = domainsfile.read().split("\n")
	for line in lines:
		if line.startswith("#"):
			outputfile.write(line)
		elif line == "":
			continue
		elif line.startswith("127.0.0.1") or line.startswith("0.0.0.0"):
			try:
				outputfile.write("address=/{}/0.0.0.0".format(line.split(" ")[1]))
			except:
				# this may fail, don't crash
				pass
		else:
			outputfile.write("address=/{}/0.0.0.0".format(line))
		outputfile.write("\n")
		

