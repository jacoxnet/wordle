import csv
import json
from wordlists.listofwords import SOLUTIONS, ALLWORDS

myfile = 'wordlists/en_50k.txt'


# first do big word list - load in from json file
# f = open('bigdictionary.json')
# word_list = json.load(f)
# words1 = set()
# for word in word_list:
#     if len(word) == 5:
#         words1.add(word)
# f.close()
# print(f"there were {len(words1)} five letter words")

with open(myfile) as dictionary:
    csv_reader = csv.reader(dictionary, delimiter=' ')
    line_count = 0
    words = dict()
    sum_freq = 0
    for row in csv_reader:
        if len(row[0]) == 5:
            freq = int(row[1])
            words[row[0]] = freq
            sum_freq += sum_freq + freq
    
for word in SOLUTIONS:
    if word not in words:
        print(f"solution word {word} not in words")

for word in ALLWORDS:
    if word not in words:
        print(f"allword word {word} not in words")
    