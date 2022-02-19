import json
import copy
import random

# length of words we're working with
WORDLEN = 11

# contains what we know about each letter position (e.g., 0-4)
# There is a PositionList instance for each position
# code:  '+' letter confirmed in that position
#        '-' letter confirmed NOT in that position
#        '^' letter possible in that position but not confirmed

class PositionList:
    def __init__(self, number):
        self.letter = {}
        # set all positions and letters to ^ (possible not confirmed)
        for i in range(ord('a'), ord('z') + 1):
            self.letter[chr(i)] = '^'

class WordKnowledge:
    def __init__(self):
        self.position = []
        for i in range(WORDLEN):
            self.position.append(PositionList(i))
        # mandatory letters but not in a specific position
        self.mandatory = []
    
    def addman(self, ltr):
        if ltr not in self.mandatory:
            self.mandatory.append(ltr)

    def removeman(self, ltr):
        if ltr in self.mandatory:
            self.mandatory.remove(ltr)
    
    def isman(self, ltr):
        return (ltr in self.mandatory)
        
    # confirm a letter in a specific position
    def confirm(self, posn, ltr):
        for i in range(ord('a'), ord('z') + 1):
            self.position[posn].letter[chr(i)] = '-'
        self.position[posn].letter[ltr] = '+'

    # rule out a letter in a specific position
    def rule_out(self, posn, ltr):
        self.position[posn].letter[ltr] = '-'
    
    # rule out a letter in all positions
    # except if already specific position (G)
    # or already on mandatory list (Y)
    # to account for double letter situation
    def rule_out_all(self, posn, ltr):
        # if already in mandatory, only rule out here
        if ltr in self.mandatory:
            self.position[posn].letter[ltr] = '-'
        # otherwise, rule out everywhere not already declared a G
        else:
            for i in range(WORDLEN):
                if self.position[i].letter[ltr] != '+':
                    self.position[i].letter[ltr] = '-'

    def test_word(self, word):
        # test a word to see if comports with knowledge. Returns T or F
        for i in range(len(word)):
            if self.position[i].letter[word[i]] == '-':
                return False
        for j in range(0, len(self.mandatory)):
            if self.mandatory[j] not in word:
                return False
        return True

    # go through list of words passed (validWords) and
    # test to see if they meet current knowledge criteria
    # returns updated word list
    def getUpdatedWordList(self, wordlist):
        returnVal = []
        for word in wordlist:
            if self.test_word(word):
                returnVal.append(word)
        return returnVal

    # update knowledge based on color response to guess word
    # response is in the form of a string of G, B, and Y. 
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    def update_knowledge(self, guess, response):
        for i in range(len(response)):
            if response[i] == 'G':
                # confirm where required 
                self.confirm(i, guess[i])
            if response[i] == 'Y':
                # rule out here and add to mandatory list
                self.rule_out(i, guess[i])
                self.addman(guess[i])
            if response[i] == 'B':
                # rule out everywhere unless G somewhere else
                self.rule_out_all(i, guess[i])

    # take guess and secret word and calculate a color response
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    def color_calc(self, guess, secret):
        returnVal = ""
        for i in range(len(guess)):
            if guess[i] == secret[i]:
                returnVal = returnVal + 'G'
            elif guess[i] in secret:
                returnVal = returnVal + 'Y'
            else:
                returnVal = returnVal + 'B'
        return returnVal

    # calculate score for word
    def score(self, guess, valids):
        score = 0
        if len(valids) == 1:
            return 100 * (guess == valids[0])
        for word in valids:
            k2 = copy.deepcopy(self)
            # calculate the response assuming word is the secret
            response = k2.color_calc(guess, word)
            # update copy of knowledge with that response
            k2.update_knowledge(guess, response)
            # delta score is difference between # of original valids minus assumed new valids
            score = score + (len(valids) - len(k2.getUpdatedWordList(valids)))
        return score

    def nextGuess2(self, valids):
        # prepare a list of counts of letters in valid words
        counts = {}
        for ch in range(ord('a'), ord('z') + 1):
            count1 = 0
            for word in valids:
                if chr(ch) in word:
                    count1 = count1 + 1
            counts[chr(ch)] = count1
        def wsum(word):
            # by using set, we eliminate duplicates
            return sum(set(counts[c] for c in word))
        sum_list = [wsum(w) for w in valids]
        maxindexes = [i for i, x in enumerate(sum_list) if x == max(sum_list)]
        return valids[random.choice(maxindexes)]
                
        

    # figure out word marked active with largest score and return
    def nextGuess(self, valids):
        print('Evaluating ', len(valids), 'possibilities')
        if len(valids) > 400:
            print('Using word count method')
            return self.nextGuess2(valids)
        else:
            print('Using dynamic max elimination method')
        topscore = 0
        topwords = []
        for word in valids:
            s = self.score(word, valids)
            if s == topscore:
                topwords.append(word)
            elif s > topscore:
                topwords = [word]
                top = s
        if len(topwords) == 0:
            print('Error in selecting guess')
        topword = random.choice(topwords)
        print('Next guess is ', topword)
        print('word count method would have returned ', self.nextGuess2(valids))
        return topword
