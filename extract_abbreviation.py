#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re

#一文ある毎に改行されているテキストを想定している
file_object = open('resource_data.txt')
abbreviation_list = []
for line in file_object:
    match = re.search('(.+?)')
    if match is not None:
        abbreviation_list.append(line)

print abbreviation_list
