#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re

#一文ある毎に改行されているテキストを想定している
file_object = open('sample.txt',"r")
wf = open('output_file.txt',"w")
#wf2 = open('output_file2.txt',"w")
abbreviation_list = []
for line in file_object:
    if re.search(r'\(.+?\)', line) is not None:
        print re.search(r'\((.+?)\)', line).group(1)
        abbreviation_list.append(line)
#        wf2.write(line)
for i in range(0,len(abbreviation_list)):
    wf.write(abbreviation_list[i])
