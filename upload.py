import csv
import json

WORDLEN = 5

# myfile = 'wordlists/en_full.txt'
myfile = 'wordlists/wordledictionary.json'

all_words = dict()
word_index = dict()
letter_index = dict()

# initialize letter_index
# letter_index[0], letter_index[1], ... contain a-z entries for words matching letter in [0], [1], position
# letter_index[0] == {'a': set('aabc', 'aacd', ...), 'b': set(...) ... 'z': set(...)}
for i in range(0, WORDLEN):
    letter_index[i] = dict()
    for j in range(ord('a'), ord('z') + 1):
        letter_index[i][chr(j)] = set()

# initialize word index
# like word index but contains words with letter in any spot
for j in range(ord('a'), ord('z') + 1):
    word_index[chr(j)] = set()


# first do big word list - load in from json file
with open('wordlists/wordledictionary.json') as f:
    words1 = json.load(f)
    for word in words1:
        if len(word) == 5 and word.isalpha() and word.isascii():
            all_words[word] = 0

# read in WORDLEN letter words and store frequencies
# with open(myfile) as dictionary:
#     csv_reader = csv.reader(dictionary, delimiter=' ')
#     for row in csv_reader:
#         if len(row[0]) == WORDLEN and row[0].isalpha() and row[0].isascii():
#             all_words[row[0]] = int(row[1])

for word in all_words.keys():
    for i in range(0, len(word)):
        letter_index[i][word[i]].add(word)
        word_index[word[i]].add(word)
        

