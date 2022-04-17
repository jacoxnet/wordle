import time
import copy
import random
from wordletrie import Trie, WORDLEN
from listofwords import ALLWORDS, SOLUTIONS

class Knowledge:

    # structure for scoring guess words
    guessWords = {}
    for word in ALLWORDS:
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
        returnVal = ""
        nsecret = secret
        for i in range(len(guess)):
            if guess[i] == nsecret[i]:
                returnVal = returnVal + 'G'
                nsecret = nsecret.replace(nsecret[i], " ", 1)
            elif guess[i] in nsecret:
                returnVal = returnVal + 'Y'
                nsecret = nsecret.replace(nsecret[i], " ", 1)
            else:
                returnVal = returnVal + 'B'
        return returnVal

    # return the number of letters in common between two words
    @staticmethod
    def letterOverlap(word1, word2):
        return len(set(word1).intersection(set(word2)))


    def getBestGuess(self):
        # zero out score
        for word in Knowledge.guessWords:
            Knowledge.guessWords[word] = 0
        # for each secret word, assume it is the solution and then calculate
        # a score for each guess word
        secretWords = self.allWords()
        #if len(secretWords) > 50:
        #    secretWords = random.sample(secretWords, 50)
        numWords = len(secretWords)
        start = time.time()
        for i in range(0, numWords):
            print(i, '/', numWords)
            print("elapsed seconds ", time.time() - start)
            for guessWord in Knowledge.guessWords:
                fakeK = Knowledge(secretWords)
                fakeK.mandatory = copy.deepcopy(self.mandatory)
                fakeK.solved = copy.deepcopy(self.solved)
                fakeResponse = Knowledge.colorCalc(guessWord, secretWords[i])
                fakeK.updateKnowledge(guessWord, fakeResponse)
                Knowledge.guessWords[guessWord] = Knowledge.guessWords[guessWord] + len(fakeK.allWords())
                del fakeK
        minKey = {}
        for i in range(0, 10):
            minKey[i] = min(Knowledge.guessWords, key=Knowledge.guessWords.get)
            del Knowledge.guessWords[minKey[i]]
        return minKey
        



