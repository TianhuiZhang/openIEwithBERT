import numpy as np

input_lines = []
with open('label_addressed.txt','r',encoding='utf-8') as f:
    for i in f.readlines():
        input_lines.append(i)

words = []
labels = []
examples = []
arg1 = []
rel = []
arg2 = []

for line in input_lines:
    if line.strip(' ') != '\n':
        word = line.strip().split('\t')[0]
        label = line.strip().split('\t')[-1]
        words.append(word)
        labels.append(label)
    else:
        examples.append([words, labels])
        words = []
        labels = []


print(len(examples))
'''
for x in range(len(examples)):
    if 'A0-B' not in examples[x][1]:
        print('Index is: ',x,examples[x][0],examples[x][1])
'''
# Connect the tag
new_example = []
for x in range(len(examples)):
    for index in range(len(examples[x][1])):
        labels = examples[x][1]
        words = examples[x][0]

        if labels[0] == 'A1-B':
            labels[0]='O'

        if index >0:
            if labels[index] == 'O' and index< len(labels)-2:
                if labels[index-1] != 'O' and labels[index-1] == labels[index+1]:
                    labels[index] = labels[index-1]

            if labels[index] == 'A1-I':
                if labels[index - 1] != 'A1-I' and labels[index - 1] == labels[index + 1]:
                    labels[index] = 'O'
            if labels[index] == 'A0-I':
                if labels[index - 1] != 'A0-I' and labels[index - 1] == labels[index + 1]:
                    labels[index] = 'O'

            if labels[index] == 'A0-I' and 'A0-B' not in labels:
                labels[index-1] = 'A0-B'
            if labels[index] == 'P-I' and 'P-B' not in labels:
                if labels[index-1] != 'O':
                    labels[index] = 'P-B'
                else:
                    labels[index - 1] = 'P-B'

            if labels[index] == 'A1-I' and 'A1-B' not in labels:
                if labels[index-1] != 'O' or labels[index-1] != 'A0-B':
                    labels[index] = 'A1-B'
                else:
                    labels[index] = 'A1-B'

    new_example.append([words, labels])

print(len(new_example))


def get_argument(argstr):
    arg = []
    argstr = argstr.strip()
    if argstr+'-B' in labels:
        start = labels.index(argstr+'-B')
        if argstr+'-I' in labels:
            end = np.where(np.array(labels)==argstr+'-I')[0][-1]
            arg = words[start:end+1]
        else:
            arg = words[start:start+1]
    else:
        arg = [' ']
    return ' '.join([str(label) for label in arg])


lines = []
for x in range(len(new_example)):
    labels = new_example[x][1]
    words = new_example[x][0]
    #print(words, labels)
    arg1 = get_argument('A0')
    rel = get_argument('P')
    arg2 = get_argument('A1')
    sentence = ' '.join([str(label) for label in words])
    if rel != ' ':
        line = sentence + '\t' + str(1) + '\t' + rel + '\t' + arg1 + '\t' + arg2 + '\n'
        lines.append(line)

with open('test_on_carb.txt','w',encoding='utf-8') as f:
    for line in lines:
        f.write(line)
