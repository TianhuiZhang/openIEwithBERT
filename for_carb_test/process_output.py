input_lines = []
predict_lines = []

with open('input_set.txt','r',encoding='utf-8') as f:
    for i in f.readlines():
        input_lines.append(i)

with open('label_test2.txt','r',encoding='utf-8') as f:
    for i in f.readlines():
        predict_lines.append(i)


# Validate
address_lines = []
for index in range(len(input_lines)):
    if input_lines[index] == '\n':
        if input_lines[index] != predict_lines[index]:
            print(index)

        new_line = '\n'
    else:
        true_word = input_lines[index].split('\t')[1]
        predict_tags = predict_lines[index].split('\t')[-1]
        new_line = true_word + '\t' + predict_tags
    address_lines.append(new_line)

with open('label_addressed.txt','w',encoding='utf-8') as f:
    for line in address_lines:
        f.write(line)
