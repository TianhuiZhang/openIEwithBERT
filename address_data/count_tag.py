
posmax = 0
depmax = 0
tag_count = [0]*10

with open('formodel.txt','r',encoding='utf-8')as f:
    for line in f.readlines():
        l = line.strip('\n').split('\t')
        if len(l)>1:

            if posmax< int(l[2]):
                posmax = int(l[2])
            if depmax < int(l[3]):
                depmax = int(l[3])
            #print(l[-1])
            if l[-1] == 'A0-B':
                tag_count[0] += 1
            elif l[-1]=='A0-I':
                tag_count[1]+=1
            elif l[-1]=='A1-B':
                tag_count[2]+=1
            elif l[-1]=='A1-I':
                tag_count[3]+=1
            elif l[-1]=='P-B':
                tag_count[4]+=1
            elif l[-1]=='P-I':
                tag_count[5]+=1
            elif l[-1] == 'A2-B':
                tag_count[6] += 1
            elif l[-1] == 'A2-I':
                tag_count[7] += 1
            elif l[-1] == 'O':
                tag_count[8] += 1
            else:
                tag_count[9] +=1
print(tag_count, posmax, depmax)