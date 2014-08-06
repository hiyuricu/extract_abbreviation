#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import MeCab

#perfect_sentence_candidate_dicとabbreviation_scoreの辞書の構成として、keyにはstring,valueにはlistが入るように設計してある
perfect_sentence_candidate_dic = {}
abbreviation_score = {}

#一文ある毎に改行されているテキストが引数にあると想定している
def main(read_file):
    output_abbreviation(read_file)
    sentence_wakati()
    make_perfect_sentence_candidate_dic()
    calculate_perfect_sentence_score()
    for key in abbreviation_score:
        print key, abbreviation_score[key][0],abbreviation_score[key][1]

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
def make_perfect_sentence_candidate_dic():
    for line in open('abbreviation_and_wakati_sentence.txt',"r"):
        #abbr_and_cand_list[0]には略語、abbr_and_cand_list[1]以降には完全文を分かち書きしたものが入っている
        abbr_and_cand_list = line.split()
        candidate_str = ""
        for i in range(0,len(abbr_and_cand_list) - 1):
            #candidate_strには完全文候補が代入されて、iが増える毎に候補の長さが伸びていく構造になっている
            candidate_str = abbr_and_cand_list[- i - 1] + candidate_str
            dic_key = abbr_and_cand_list[0] + "_" + candidate_str
            #if (要素) in (辞書):で辞書のキーに要素があるかどうか見ている
            if dic_key in perfect_sentence_candidate_dic:
                perfect_sentence_candidate_dic[dic_key][0] += 1
                #abbr_and_cand_list[0]には略語が入っているので、それが完全文候補にならないようにしている
                if abbr_and_cand_list[- i - 2] != abbr_and_cand_list[0]:
                    #hypernym_dic_keyは完全文候補のdic_keyの上位語である。例えばdic_keyがピースなら、hypernym_dic_keyはワンピース等である
                    hypernym_dic_key = abbr_and_cand_list[0] + "_" + abbr_and_cand_list[- i - 2] + candidate_str
                    #辞書のvalueに入っているリストに上位の完全文候補があるかどうか見ている
                    if hypernym_dic_key not in perfect_sentence_candidate_dic[dic_key]:
                        perfect_sentence_candidate_dic[dic_key].append(hypernym_dic_key)
                #print dic_key, perfect_sentence_candidate_dic[dic_key][0], perfect_sentence_candidate_dic[dic_key][1].decode("utf-8")

            #辞書のキーに要素が無い場合には辞書に新しいkeyとvalueの組を作るようにしている
            else:
                #abbr_and_cand_list[0]には略語が入っているので、それが完全文候補にならないようにしている
                if abbr_and_cand_list[- i - 2] != abbr_and_cand_list[0]:
                    #hypernym_dic_keyは完全文候補のdic_keyの上位語である。例えばdic_keyがピースなら、hypernym_dic_keyはワンピース等である
                    hypernym_dic_key = abbr_and_cand_list[0] + "_" + abbr_and_cand_list[- i - 2] + candidate_str
                    perfect_sentence_candidate_dic[dic_key] = [1,hypernym_dic_key]
                #辞書において末端の部分のキーを作る。つまり上位語が存在しない場合。
                elif abbr_and_cand_list[- i - 2] == abbr_and_cand_list[0]:
                    perfect_sentence_candidate_dic[dic_key] = [1,"s"]
                #print dic_key, perfect_sentence_candidate_dic[dic_key][0], perfect_sentence_candidate_dic[dic_key][1].decode("utf-8")

#完全文候補のスコアの値を計算する関数
def calculate_perfect_sentence_score():
    for key,value_list in perfect_sentence_candidate_dic.items():
        perfect_sentence_score = value_list[0]
        total_of_hypernym_score = 0
        hypernym_score_list = []
        #freq(Tw)にあたるtotal_of_hypernym_scoreと、freq(t)をリストにまとめたhypernym_score_listを作る制御文
        for i in range(1,len(value_list)):
            #上位語候補には文字列sがあり、sをキーとした項目は辞書にはないのでそれ以外について動作させようとしている
            if value_list[i] != "s":
                total_of_hypernym_score += perfect_sentence_candidate_dic[value_list[i]][0]
                hypernym_score_list.append(perfect_sentence_candidate_dic[value_list[i]][0])

        #TH(w)を求める時のシグマの引き算の部分の計算を行っている
        for hypernym_score in hypernym_score_list:
            perfect_sentence_score -= float(hypernym_score) * hypernym_score / total_of_hypernym_score

        """#上位語がない部分(bosから始まっている)の計算を行っている
        if total_of_hypernym_score != 0:
            #freq(w)を表すvalue_list[0]からfreq(Tw)を表すtotal_of_hypernym_scoreを引けば、bosから始まる完全文候補の出現頻度となる
            bos_score = value_list[0] - total_of_hypernym_score
            if bos_score != 0:
                perfect_sentence_score -= bos_score * bos_score / total_of_hypernym_score
        #上位語が存在しない場合を考えている。
        else:
            perfect_sentence_score = 0"""

        compare_perfect_sentence_score(key, perfect_sentence_score)


#完全文候補のスコアを比較することで略語と対応する完全文のペアを出力する関数
def compare_perfect_sentence_score(key, perfect_sentence_score):
    #keyをsplitして[(略語), (完全文候補)]という構成のリストを作成する
    abbreviation_and_candidate_list = key.split("_")
    #abbreviation_scoreに略語のキーがあるかどうか見ている
    if abbreviation_and_candidate_list[0] in abbreviation_score:
        #ある略語の完全文候補のTH(w)を比較して、TH(w)の値が大きい方の完全文候補の、完全文とTH(w)の値をvalueのlistに代入する
        if perfect_sentence_score > abbreviation_score[abbreviation_and_candidate_list[0]][1]:
            abbreviation_score[abbreviation_and_candidate_list[0]][0] = abbreviation_and_candidate_list[1]
            abbreviation_score[abbreviation_and_candidate_list[0]][1] = perfect_sentence_score
    #辞書に新しくkeyを作成する
    else:
        abbreviation_score[abbreviation_and_candidate_list[0]] = [abbreviation_and_candidate_list[1], perfect_sentence_score]

if __name__ == "__main__":
    main(sys.argv[1])
