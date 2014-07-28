#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import MeCab

#一文ある毎に改行されているテキストが引数にあると想定している
def main(read_file):
    output_abbreviation(read_file)
    setence_wakati()

#略語と略語を含む文を出力する関数
def output_abbreviation(read_file):
    wf = open('abbreviation_and_sentence.txt',"w")
    for line in open(read_file,"r"):
        line = line.strip()
        for abb in re.finditer(r'(.+?)\((.+?)\)', line):

            wf.write("%s\t%s\n" % (abb.group(2), abb.group(1)))
    wf.close()

#文章を分かち書きする関数
def setence_wakati():
    wf = open('abbreviation_and_wakati_sentence.txt',"w")
    tagger = MeCab.Tagger('-Owakati')
    for line in open('abbreviation_and_sentence.txt',"r"):
        temp_list = line.split()
        result = tagger.parse(temp_list[1])
        wf.write("%s\t%s" % (temp_list[0], result))
    wf.close()

if __name__ == "__main__":
    main(sys.argv[1])
