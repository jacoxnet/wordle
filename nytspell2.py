WORDLEN = [4, 20]
puzzle = ['l', ['p', 'g', 'm', 'a', 'e', 'x' ]] 


import json
# word list - load in from json file
# f = open('bigdictionary.json')
f = open('bigdictionary.json')
wordList = json.load(f)
f.close()

len(wordList)

import itertools as it

lexicon = set()

for word in wordList:
    qualified = True
    if len(word) < WORDLEN[0] or len(word) >= WORDLEN[1]:
        qualified = False
        continue
    if puzzle[0] not in word:
        qualified = False
        continue
    for letter in word:
        if letter != puzzle[0] and letter not in puzzle[1]:
            qualified = False
            break
    if qualified:
        lexicon.add(word)

print(lexicon)