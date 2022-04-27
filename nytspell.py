import json, copy
WORDLEN = [4, 25]
puzzle = ['f', ['t', 'n', 'o', 'e', 'c', 'i']]
alph = set([x for x in 'abcdefghijklmnopqrstuvwxyz'])

# word list - load in from json file
# f = open('bigdictionary.json')
f = open('bigdictionary.json')
wordList = json.load(f)
f.close()
lexicon = set()
print(f"Loaded {len(wordList)} words")

for letter in copy.copy(alph):
    if letter in puzzle[1] or letter == puzzle[0]:
        alph.remove(letter)

for word in wordList:
    if all([len(word) >= WORDLEN[0],
             len(word) < WORDLEN[1],
             all([ltr not in alph for ltr in word]),
             puzzle[0] in word]):
        lexicon.add(word)
    else:
        pass

print (lexicon)
