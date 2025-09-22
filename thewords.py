FILEH = "wordlists/alex_hidden"
FILEA = "wordlists/alex_all"

def get_wordlists():
    all_words = []
    hidden_words = []
    with open(FILEA, "r") as afile:
        for line in afile:
            if line.strip():
                all_words.append(line.strip())
    with open(FILEH, "r") as afile:
        for line in afile:
            if line.strip():
                hidden_words.append(line.strip())

    #print(f"read a total of {len(all_words)} valid words from allwords list")
    #print(f"read a total of {len(hidden_words)} valid words from hidden words list")
    
    return all_words, hidden_words

