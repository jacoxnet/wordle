import json, copy
WORDLEN = [4, 11]
puzzle = ['p', ['g', 'u', 'n', 'r', 'b', 'i' ]] 
alph = [x for x in 'abcdefghijklmnopqrstuvwxyz']

# word list - load in from json file
# f = open('bigdictionary.json')
f = open('bigdictionary.json')
wordList = json.load(f)
wordList = set(wordList.keys())
f.close()
print(f"Loaded {len(wordList)} words")

len(wordList)
lexicon = set()

for letter in alph:
    if letter in puzzle[1] or letter == puzzle[0]:
        alph.remove(letter)

for word in copy.copy(wordList):
    if len(word) < WORDLEN[0] or len(word) >= WORDLEN[1]:
        wordList.remove(word)
    elif any([ltr in alph for ltr in word]):
        wordList.remove(word)
    elif puzzle[0] not in word:
        wordList.remove(word)
    else:
        pass

