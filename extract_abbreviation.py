#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import MeCab

perfect_sentence_candidate_dic = {}
#一文ある毎に改行されているテキストが引数にあると想定している
def main(read_file):
    output_abbreviation(read_file)
    sentence_wakati()
    make_candidate_dic()

#略語と略語を含む文を出力する関数
def output_abbreviation(read_file):
    wf = open('abbreviation_and_sentence.txt',"w")
    for line in open(read_file,"r"):
        line = line.strip()
        for abb in re.finditer(r'(.+?)\((.+?)\)', line):

            wf.write("%s\t%s\n" % (abb.group(2), abb.group(1)))
    wf.close()

#文章を分かち書きする関数
def sentence_wakati():
    wf = open('abbreviation_and_wakati_sentence.txt',"w")
    tagger = MeCab.Tagger('-Owakati')
    for line in open('abbreviation_and_sentence.txt',"r"):
        temp_list = line.split()
        result = tagger.parse(temp_list[1])
        wf.write("%s\t%s" % (temp_list[0], result))
    wf.close()

#完全文候補をキーとし、略語や頻度などが示されているリストをvalueとする辞書を作成する関数。論文では第三ステップに当たる
def make_candidate_dic():
    wf = open('candidate_dictionary.txt',"w")
    for line in open('abbreviation_and_wakati_sentence.txt',"r"):
        #abbr_and_cand_list[0]には略語、abbr_and_cand_list[1]以降には完全文を分かち書きしたものが入っている
        abbr_and_cand_list = line.split()
        candidate_str = ""
        for i in range(0,len(abbr_and_cand_list) - 1):
            #abbr_and_cand_list[- i - 1]には完全文を分かち書きしたものが代入されていて、文字の後ろから順に代入されている
            candidate_str = abbr_and_cand_list[- i - 1] + candidate_str
            dic_key = abbr_and_cand_list[0] + "_" + candidate_str
            #if (要素) in (辞書):で辞書のキーに要素があるかどうか見ている
            if dic_key in perfect_sentence_candidate_dic:
                perfect_sentence_candidate_dic[dic_key][0] += 1
                #abbr_and_cand_list[0]には略語が入っているので、それが完全文候補にならないようにしている
                if abbr_and_cand_list[- i - 2] != abbr_and_cand_list[0]:
                    #hypernym_dic_keyは完全文候補のdic_keyの上位語である。例えばdic_keyがピースなら、hypernym_dic_keyはワンピース等である。
                    hypernym_dic_key = abbr_and_cand_list[0] + "_" + abbr_and_cand_list[- i - 2] + candidate_str
                    #辞書のvalueに入っているリストに上位の完全文候補があるかどうか見ている
                    if hypernym_dic_key not in perfect_sentence_candidate_dic[dic_key]:
                        perfect_sentence_candidate_dic[dic_key].append(hypernym_dic_key)
                print dic_key, perfect_sentence_candidate_dic[dic_key][0], perfect_sentence_candidate_dic[dic_key][1].decode("utf-8")

            #辞書のキーに要素が無い場合には辞書に新しいkeyとvalueの組を作るようにしている
            else:
                #abbr_and_cand_list[0]には略語が入っているので、それが完全文候補にならないようにしている
                if abbr_and_cand_list[- i - 2] != abbr_and_cand_list[0]:
                    #hypernym_dic_keyは完全文候補のdic_keyの上位語である。例えばdic_keyがピースなら、hypernym_dic_keyはワンピース等である。
                    hypernym_dic_key = abbr_and_cand_list[0] + "_" + abbr_and_cand_list[- i - 2] + candidate_str
                    perfect_sentence_candidate_dic[dic_key] = [1,hypernym_dic_key]
                    print dic_key, perfect_sentence_candidate_dic[dic_key][0], perfect_sentence_candidate_dic[dic_key][1].decode("utf-8")

    wf.close()

if __name__ == "__main__":
    main(sys.argv[1])
