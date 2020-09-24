from bert_serving.client import BertClient
import numpy as np
from tqdm import tqdm

rf = open('test.txt', 'r', encoding='utf-8')
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
        if len(words)<=64:
            with open('addressed_test.txt', 'a', encoding='utf-8') as f:
                for index in range(len(words)):
                    f.write(str(index) + '\t' + words[index] + '\t' + poss[index] + '\t' + str(last_pred_id)
                                + '\t' + last_pred_pos + '\t' + labels[index] + '\n')
                f.write('\n')
        words = []
        poss = []
        labels = []
    words.append(word)
    poss.append(pos)
    labels.append(label)
    last_pred_id = pred_id
    last_pred_pos = pred_pos
rf.close()