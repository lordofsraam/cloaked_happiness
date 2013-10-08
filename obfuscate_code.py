#!/usr/bin/python
"""
C++ Source Code Obfuscator

-Created by Piero Barbagelata (Lordofsraam) and Kile Deal (Aurenos)


TODO:
-More elegant keyword loading
-Support more languages
"""

import re

keywords = set(["class","for","if",
	"true","false","public",
	"private","printf","cout",
	"cin","int","float","double"
	"string","std","main","delete",
	"return","char","include",
	"const","define","ifndef","endif",
	"stdio","inline","replaceme",
	"replacemeinclude", "new","unsigned",
	"switch","typedef"])

code_file = open("test.cpp", 'rw')

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
print "Tokenization done"

if(raw_input("See the tokens?[y/N]: ") == "y"):
	print code_tokens

variables = code_tokens.difference(keywords)

if(raw_input("See the variables?[y/N]: ") == "y"):
	print variables

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
newfile = open("obfuscated_file.cpp","w")
newfile.write(code)
newfile.close()
print "New file 'obfuscated_file.cpp' created.\n"
