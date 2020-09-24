from bert_serving.client import BertClient
import numpy as np
from tqdm import tqdm
import json


posmap = {'NNP': 1, 'VBD': 2, ':': 3, 'IN': 4, 'DT': 5, 'NN': 6, ',': 7, 'CD': 8, 'NNS': 9, 'JJ': 10, '.': 11, 'CC': 12, 'VBG': 13, 'TO': 14, 'VB': 15, 'WDT': 16, 'WP': 17, 'VBN': 18, 'RB': 19, 'PRP': 20, 'RP': 21, 'PRP$': 22, 'MD': 23, 'JJR': 24, 'NNPS': 25, 'POS': 26, 'VBZ': 27, '-LRB-': 28, '-RRB-': 29, 'VBP': 30, 'JJS': 31, 'RBS': 32, 'FW': 33, 'WRB': 34, '$': 35, 'HYPH': 36, 'WP$': 37, 'RBR': 38, 'SYM': 39, 'EX': 40, 'PDT': 41, '``': 42, "''": 43, 'UH': 44, 'AFX': 45, 'ADD': 46, 'NFP': 47, 'LS': 48, 'GW': 49}

def get_keys(d, value):
    x = list(d.keys())[list(d.values()).index(value)]
    return x

countmap={}
rf = open('addressed_train.txt', 'r', encoding='utf-8')
lines = []
words = []
poss = []
last_pred_id = 0
last_pred_pos = 0
labels = []
for line in tqdm(rf):
    if len(line.strip()) == 0:
        continue

    word = line.strip().split('\t')[1]
    if " " in word:
        print(word)
        word = word.split(' ')[0]
    pos = line.strip().split('\t')[2]
    pred_id = int(line.strip().split('\t')[3])
    pred_pos = line.strip().split('\t')[4]
    label = line.strip().split('\t')[-1]

    if line[0] == "0" and words:
        #last_pred_pos = get_keys(posmap, int(last_pred_pos))

        if last_pred_pos in countmap.keys():
            countmap[last_pred_pos] += 1
        else:
            countmap[last_pred_pos] = 1
        words = []
        poss = []
        labels = []
    words.append(word)
    poss.append(pos)
    labels.append(label)
    last_pred_id = pred_id
    last_pred_pos = pred_pos
rf.close()

print(sorted(countmap.items(), key = lambda kv:(kv[1], kv[0]),reverse=True))