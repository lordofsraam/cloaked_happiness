#!/usr/bin/python
"""
C++ Source Code Obfuscator

-Created by Piero Barbagelata (Lordofsraam) and Kile Deal (Aurenos)


TODO:
-More elegant keyword loading
-Support more languages
"""

DEFAULT_FILENAME = "test.cpp"
FILE_TO_PARSE = ""
KEYWORDS_DB_FILENAME = "keywords.txtdb"

import re
import sys
import os.path

if len(sys.argv) > 1:
	print "CLI input detected. Will obfuscate file named:",sys.argv[1]
	FILE_TO_PARSE = sys.argv[1]
	if not os.path.isfile(FILE_TO_PARSE):
		print "File",FILE_TO_PARSE,"not found. Exiting...\n"
		exit()
	print "\n"
else:
	print "No CLI arguments detected. Will obfuscate file named:",DEFAULT_FILENAME
	FILE_TO_PARSE = DEFAULT_FILENAME

keywords = ["class","for","if",
	"true","false","public",
	"private","printf","cout",
	"cin","int","float","double"
	"string","std","main","delete",
	"return","char","include",
	"const","define","ifndef","endif",
	"inline","replaceme",
	"replacemeinclude", "new","unsigned",
	"switch","typedef","bool"]

if os.path.isfile(KEYWORDS_DB_FILENAME):
	print "Found a keyword database file"
	kdbf = open(KEYWORDS_DB_FILENAME,"r")
	print "Loading keywords from file",KEYWORDS_DB_FILENAME
	kdb = kdbf.read().split()
	if(raw_input("See the keywords?[y/N]: ") == "y"):
		print kdb
	print "Adding keywords to internal database"
	for k in kdb:
		keywords.append(k)
	print "Keywords added\n"
else:
	print "No external keyword database file found. Using default.\n"

print "Making keywords a set"
keywords = set(keywords)
print "Set made\n"

code_file = open(FILE_TO_PARSE, 'rw')

print "Loading code from file."
code = code_file.read()
print "Done loading code\n"

code_file.close()
print "File closed\n"

print "Finding includes"
code_includes = re.findall('\#include.*',code)
print "Replacing includes with temp vals\n"
code = re.sub(r'\#include.*',"replacemeinclude",code)

print "Finding string literals"
code_strings = re.findall('\".*\"',code)
print "Replacing string literals with temp vals\n"
code = re.sub(r'\".*\"',"replaceme",code)

print "Tokenizing the code"
code_tokens = set(filter(lambda cologne: cologne != '',re.split('\W+|[0-9]',code)))
print "Tokenization done\n"

if(raw_input("See the tokens?[y/N]: ") == "y"):
	print code_tokens

print "\n"

variables = code_tokens.difference(keywords)

if(raw_input("See the variables?[y/N]: ") == "y"):
	print variables

print "\n"

obfus_offset = 1

for v in variables:
	if(v in code):	code = re.sub(r"\b{0}\b".format(v),"_"*obfus_offset,code)
	obfus_offset += 1

print "Replacing old includes"
for x in xrange(len(code_includes)):
	if("replacemeinclude" in code): code = code.replace("replacemeinclude",code_includes[x],1)
print "All old includes back in place\n"

print "Replacing old string literals"
for x in xrange(len(code_strings)):
	if("replaceme" in code): code = code.replace("replaceme",code_strings[x],1)
print "All old strings back in place\n"

if(raw_input("See the new code?[y/N]: ") == "y"):
	print code

print "Creating new file..."
if os.path.isfile("obfuscated_"+FILE_TO_PARSE):
	print "Old obfuscation file detected. Will overwrite."
newfile = open("obfuscated_"+FILE_TO_PARSE,"w")
newfile.write(code)
newfile.close()
print "New file 'obfuscated_"+FILE_TO_PARSE+"' created.\n"
