import time
import copy
import random
from wordletrie import Trie, WORDLEN
from listofwords import ALLWORDS, SOLUTIONS

class Knowledge:

    # structure for scoring guess words
    guessWords = {}
    for word in SOLUTIONS:
        guessWords[word] = 0

    def __init__(self, wordList):
        self.trie = Trie()
        for word in wordList:
            self.trie.insert(word)
        self.mandatory = set()
        self.solved = {}


    def __repr__(self):
        return ("Trie of length " + str(len(self.trie.allWords())) + " mandatory:" + str(self.mandatory) +
                " solved:" + str(self.solved))

    def allWords(self):
        return self.trie.allWords()

    # update knowledge based on color response to guess word
    # response is in the form of a string of G, B, and Y. 
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    #   because of serial nature of this inquiry, we need to process in order of G, Y, B
    def updateKnowledge(self, guess, response):
        tresp = {'G': [], 'Y': [], 'B': []}
        for i in range(0, len(response)):
            tresp[response[i]].append(i)
        for i in tresp['G']:
            # delete all solution words without this letter in this posn
            self.trie.delNLetterPos(guess[i], i)
            # updated solved dict
            self.solved[i] = guess[i]
        for i in tresp["Y"]:
            # delete all solution words without this letter in some position
            self.trie.delNLetter(guess[i])
            # update mandatory list
            self.mandatory.add(guess[i])
        for i in tresp["B"]:
            if guess[i] in self.mandatory or guess[i] in self.solved.values():
                # mandatory or solved letter - we can only delete words with this guess letter at this pos
                self.trie.delLetterPos(guess[i], i)
            else:
                self.trie.delLetter(guess[i])


    # take guess and secret word and calculate a color response
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    # because there can be duplicate letters, when we find a match we
    # replace the letter in the secret with space so it isn't found again
    @staticmethod
    def colorCalc(guess, secret):
        listSecret = [letter for letter in secret]
        response = WORDLEN * [' ']
        for i in range(len(guess)):
            if guess[i] == listSecret[i]:
                response[i] = 'G'
                listSecret[i] = ' '
        for i in range(len(guess)):
            if guess[i] in listSecret:
                response[i] = 'Y'
                listSecret = [' ' if item == guess[i] else item for item in listSecret]
        response = ['B' if item == ' ' else item for item in response]
        return ''.join(response)

    # return the number of letters in common between two words
    @staticmethod
    def letterOverlap(word1, word2):
        return len(set(word1).intersection(set(word2)))

    # given a guessword, returns the average size of resulting groupings
    # that guess word could divide the solution words
    rdict = {}
    
    def scoreGuess(self, guessword):
        rdict = {}
        for secretword in self.allWords():
            result = Knowledge.colorCalc(guessword, secretword)
            if result in rdict:
                rdict[result] = rdict[result] + 1
            else:
                rdict[result] = 1
        aveGSize = sum(rdict.values())/len(rdict)
        Knowledge.rdict = rdict
        return aveGSize

    def allMins(self, dictWords):
        # find minimum value
        mm = min(dictWords.values())
        #create list of all minimum words
        rv = [k for k in dictWords.keys() if dictWords[k] == mm]
        # create smaller list of secretwords in earlier list
        sv = [secretWord for secretWord in rv if self.trie.search(secretWord) != -1]
        # return only secret words if there are some
        if len(sv) > 0:
            return sv
        else:
            return rv

    def getBestGuess(self):
        if len(self.allWords()) == 1:
            return self.allWords()
        for word in Knowledge.guessWords:
            aveGSize =  self.scoreGuess(word)
            Knowledge.guessWords[word] = aveGSize
        return self.allMins(Knowledge.guessWords)
        



