from wordletrie import Trie, WORDLEN
from listofwords import ALLWORDS, SOLUTIONS

class Knowledge:

    def __init__(self):
        self.trie = Trie()
        for word in SOLUTIONS:
            self.trie.insert(word)
        self.mandatory = []
        self.solved = [WORDLEN]


    def __repr__(self):
        return ("Trie of length ", len(self.trie.allWords()))

    # update knowledge based on color response to guess word
    # response is in the form of a string of G, B, and Y. 
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    def update_knowledge(self, guess, response):
        for i in range(len(response)):
            if response[i] == 'G':
                # delete all solution words without this letter in this posn
                self.trie.delNNLetter(guess[i], i)
            if response[i] == 'Y':
                # delete all solution words without this letter in some position
                self.trie.delNLetter(guess[i])
            if response[i] == 'B':
                # rule out everywhere unless G somewhere else
                self.rule_out_all(i, guess[i])



    # take guess and secret word and calculate a color response
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    # because there can be duplicate letters, when we find a match we
    # replace the letter in the secret with space so it isn't found again
    @staticmethod
    def color_calc(guess, secret):
        returnVal = ""
        nsecret = secret
        for i in range(len(guess)):
            if guess[i] == nsecret[i]:
                returnVal = returnVal + 'G'
                nsecret = nsecret.replace(nsecret[i], " ", 1)
            elif guess[i] in secret:
                returnVal = returnVal + 'Y'
                nsecret = nsecret.replace(nsecret[i], " ", 1)
            else:
                returnVal = returnVal + 'B'
        return returnVal
