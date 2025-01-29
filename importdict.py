import csv
from wordletrie import WORDLEN
MAX_INDEX = 1000


def get_wordlists():
    wordlist = {}
    with open("wordlists/unigram_freq.csv", "r") as unigram:
        dreader = csv.DictReader(unigram)
        for row in dreader:
            wordlist[row["word"]] = row["count"]
    
    print(f"read a total of {len(wordlist)} words")

    valid_words = {k:int(v) for (k, v) in wordlist.items() if len(k) == WORDLEN}
    print(f"there are {len(valid_words)} valid words")

    maxk = max(valid_words.values())
    # replace freq with index with MAX_INDEX
    valid_words = {word: int(MAX_INDEX*freq/maxk) for (word, freq) in valid_words.items()}
    best_words = []
    other_words = []
    for word, freq in valid_words.items():
        if valid_words[word] > 0:
            best_words.append(word)
        else:
            other_words.append(word)
    return best_words, other_words

