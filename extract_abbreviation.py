#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import MeCab

#一文ある毎に改行されているテキストを想定している
def main(read_file):
    file_object = open(read_file,"r")
    wf = open('output_file.txt',"w")
    for line in file_object:
        line = line.strip()
        for m in re.finditer(r'\((.+?)\)', line):
            wf.write("%s\t%s\n" % (line,m.group(1)))
    file_object.close()
    wf.close()

if __name__ == "__main__":
    main(sys.argv[1])