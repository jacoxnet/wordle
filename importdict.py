import csv
from wordletrie import WORDLEN
from wordlists.listofwords import SOLUTIONS, ALLWORDS
MAX_BEST = 2000
MAX_OTHER = 5000


def get_wordlists():
    wordlist = []
    with open("wordlists/unigram_freq.csv", "r") as unigram:
        dreader = csv.DictReader(unigram)
        for row in dreader:
            if len(row["word"]) == WORDLEN:
                wordlist.append(row["word"])
    
    # print(f"read a total of {len(wordlist)} valid words")
    # sort by frequency and choose top 1000
    
    best_words = set(wordlist[:MAX_BEST])
    other_words = set(wordlist[MAX_BEST:MAX_OTHER])
    # add original solutions and other words
    for word in SOLUTIONS:
        best_words.add(word)
    for word in ALLWORDS:
        other_words.add(word)
    
    with open("wordlists/RIDYHEWordList.csv", "r") as rid:
        dreader = csv.DictReader(rid)
        for row in dreader:
            if len(row["Word"]) == WORDLEN:
                other_words.add(row["Word"])

    print(f"Working with {len(best_words)} best words and {len(other_words)} other words")
    return list(best_words), list(other_words)

