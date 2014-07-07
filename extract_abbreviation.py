#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re

#一文ある毎に改行されているテキストを想定している
file_object = open('sample.txt',"r")
wf = open('output_file.txt',"w")
for line in file_object:
    line = line.strip()
    for m in re.finditer(r'\((.+?)\)', line):
        wf.write("%s\t%s\n" % (line,m.group(1)))