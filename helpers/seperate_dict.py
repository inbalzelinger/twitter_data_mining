import re


arabizi_words = []
new_arabizi_words = []
with open('training_set.txt',  encoding='utf-8') as f:
    lines = f.readlines()
for line in lines:
    arabizi_words.append(re.split(r'\t+', line.rstrip('\t')))
for line in arabizi_words:
    new_arabizi_words.append(line[0])

with open('elda_dict.txt','w', encoding='utf-8') as f:
    for word in new_arabizi_words:
        print(word)
        f.write(word)
        f.write('\n')





