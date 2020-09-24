# coding=utf-8
import csv
import numpy as np
import re

import os
from stanfordcorenlp import StanfordCoreNLP

posmap = {'NNP': 1, 'VBD': 2, ':': 3, 'IN': 4, 'DT': 5, 'NN': 6, ',': 7, 'CD': 8, 'NNS': 9, 'JJ': 10, '.': 11, 'CC': 12, 'VBG': 13, 'TO': 14, 'VB': 15, 'WDT': 16, 'WP': 17, 'VBN': 18, 'RB': 19, 'PRP': 20, 'RP': 21, 'PRP$': 22, 'MD': 23, 'JJR': 24, 'NNPS': 25, 'POS': 26, 'VBZ': 27, '-LRB-': 28, '-RRB-': 29, 'VBP': 30, 'JJS': 31, 'RBS': 32, 'FW': 33, 'WRB': 34, '$': 35, 'HYPH': 36, 'WP$': 37, 'RBR': 38, 'SYM': 39, 'EX': 40, 'PDT': 41, '``': 42, "''": 43, 'UH': 44, 'AFX': 45, 'ADD': 46, 'NFP': 47, 'LS': 48, 'GW': 49}


class Labelr(object):
    def __init__(self, corenlp_dir):
        self.model = StanfordCoreNLP(r'stanford-corenlp-4.1.0', lang='en')

    def get_features(self, sentence):
        words = self.model.word_tokenize(sentence)
        postags = self.model.pos_tag(sentence)  # part-of-speech
        words = list(words)
        postags = list(postags)

        return words, postags

    def get_words(self,sentence):
        words = self.model.word_tokenize(sentence)
        words = list(words)
        return words


lines = []
with open('input.txt', "r",encoding='utf-8') as f:
    for line in f.readlines():
        lines.append(line)

laber = Labelr('corenlp')

for index in range(len(lines)):
    print(index)
    sentence = lines[index]
    tokens, pos = laber.get_features(sentence)
    temp = ['O'] * len(tokens)
    pos_index = []
    for i in pos:
        if i[1] in posmap.keys():
            pos_index.append(posmap[i[1]])
        else:
            pos_index.append(0)



    pb_collected = []
    position_collected = []

    pos_array = np.array(pos_index)
    # Define the search order according to the possibility
    search_order = [2, 27, 30, 18, 13, 23, 14]
    for poss_pos in search_order:
        # Select top 4 possible words to be 'P-B'
        if len(pb_collected) < 4:
            x = np.where(pos_array == poss_pos)[0]
            if len(x) > 0:
                # The POSs not need to check
                if poss_pos in [2, 27, 30, 23]:
                    position_collected.extend(list(x))
                    pb_collected.extend([poss_pos]*len(x))
                else:
                    # Other POSs with small probabilities
                    if len(position_collected) > 0:
                        for poss_pb in x:
                            relative_distance = np.where(abs(np.array(position_collected)-poss_pb) > 3 )[0]
                            if len(relative_distance)== len(position_collected) and len(pb_collected) < 4:
                                position_collected.append(poss_pb)
                                pb_collected.append(poss_pos)
                    else:
                        position_collected.extend(list(x))
                        pb_collected.extend([poss_pos] * len(x))

    for collected in range(len(pb_collected)):
        with open('input_set.txt','a',encoding='utf-8') as f:
            for i in range(len(temp)):
                f.write(str(i) + '\t' + tokens[i] + '\t' + str(pos_index[i]) + '\t' + str(
                    position_collected[collected]) + '\t' + str(pb_collected[collected]) + '\t' + temp[i] + '\n')
            f.write('\n')









