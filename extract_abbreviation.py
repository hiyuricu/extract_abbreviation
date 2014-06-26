#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re

#一文ある毎に改行されているテキストを想定している
file_object = open('sample.txt')
abbreviation_list = []
for line in file_object:
    match = re.search('(.+?)', line)
    if match is not None:
        abbreviation_list.append(line)
        print line
