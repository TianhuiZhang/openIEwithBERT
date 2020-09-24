# coding=utf-8
import csv
import numpy as np
import re

import os
from stanfordcorenlp import StanfordCoreNLP
class Labelr(object):
    def __init__(self, corenlp_dir):
        self.model = StanfordCoreNLP(r'stanford-corenlp-4.1.0', lang='en')

    def get_features(self, sentence):
        words = self.model.word_tokenize(sentence)
        postags = self.model.pos_tag(sentence)  # POS TAGGING
        words = list(words)
        postags = list(postags)

        return words, postags

    def get_words(self,sentence):
        words = self.model.word_tokenize(sentence)
        words = list(words)
        return words

lines = []
with open('original.tsv', "r",encoding='utf-8') as f:
    reader = csv.reader(f, delimiter="\t")
    for line in reader:
        lines.append(line)

def find_loc(a,sub):
    locs = [-1]
    window = len(sub)
    for j in range(0, len(a)-window+1):
        test = a[j:j+window]
        if test == sub:
            locs.append(j)
    return locs

posmap={}
depmap={}
poscount = 1
depcount = 1
laber = Labelr('corenlp')
count = 0
for index in range(len(lines)):
    print(index)
    line = lines[index]
    sentence = line[0]
    tokens, pos = laber.get_features(sentence)
    temp = ['O'] * len(tokens)
    sentence = ' '.join([word for word in tokens if len(word) > 0])
    extractions = line[1]
    p_b = 0
    try:
        pattern_arg1 = re.compile(r'<arg1>(.*?)</arg1>')
        arg1 = pattern_arg1.findall(extractions)[0].strip()
        arg1 = laber.get_words(arg1)
        loc = int(find_loc(tokens,arg1)[1])
        for i in range(len(arg1)):
            temp[loc+i]='A0-I'
        temp[loc] = 'A0-B'

        pattern_rel = re.compile(r'<rel>(.*?)</rel>')
        rel = pattern_rel.findall(extractions)[0].strip()
        rel = laber.get_words(rel)
        loc = int(find_loc(tokens, rel)[1])
        for i in range(len(rel)):
            temp[loc + i] = 'P-I'
        temp[loc] = 'P-B'
        p_b = loc

        pattern_arg2 = re.compile(r'<arg2>(.*?)</arg2>')
        arg2 = pattern_arg2.findall(extractions)[0].strip()
        arg2 = laber.get_words(arg2)
        loc = int(find_loc(tokens, arg2)[1])
        for i in range(len(arg2)):
            temp[loc + i] = 'A1-I'
        temp[loc] = 'A1-B'

        for index in range(len(temp)):
            if pos[index][1] in posmap.keys():
                posindex = posmap[pos[index][1]]
            else:
                posmap[pos[index][1]] = poscount
                poscount += 1

        for index in range(len(temp)):
            if pos[index][1] in posmap.keys():
                posindex = posmap[pos[index][1]]
            else:
                posmap[pos[index][1]] = poscount
                poscount += 1

        with open('posr.txt', 'a', encoding='utf-8') as f:
            for index in range(len(temp)):

                f.write(str(index) + '\t' + tokens[index] + '\t'+str(posmap[pos[index][1]]) + '\t' + str(p_b) + '\t' + str(posmap[pos[p_b][1]])+ '\t' +temp[index] + '\n')
            f.write('\n')
        count +=1
        print(count)
    except IndexError:
        print()
laber.model.close()
print(posmap)
