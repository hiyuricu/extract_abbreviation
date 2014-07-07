#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import MeCab

#一文ある毎に改行されているテキストが引数にあると想定している
def main(read_file):
    output_abbreviation(read_file)
    setense_wakati()

#略語と略語を含む文を出力する関数
def output_abbreviation(read_file):
    file_object = open(read_file,"r")
    wf = open('output_file.txt',"w")
    for line in file_object:
        line = line.strip()
        for m in re.finditer(r'\((.+?)\)', line):
            wf.write("%s\t%s\n" % (line,m.group(1)))
    file_object.close()
    wf.close()

#文章を分かち書きする関数
def setense_wakati():
    rf = open('output_file.txt',"r").read()
    tagger = MeCab.Tagger('-Owakati')
    result = tagger.parse(rf)
    print result

if __name__ == "__main__":
    main(sys.argv[1])