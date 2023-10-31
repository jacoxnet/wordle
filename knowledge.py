import time
from upload import WORDLEN, word_index, letter_index
import multiprocessing as mp

# multiproceessing threads are used to calculate best guess
THREADS = mp.cpu_count()

class Knowledge:

    def __init__(self, word_list):
        self.all_words = list(word_list)
        self.solution_set = set(word_list)
        self.mandatory = set()
        # solved = {0: 's', 2:'l', 3:'a' ... }
        self.solved = dict()

    # update knowledge based on color response to guess word
    # response is in the form of a string of G, B, and Y. 
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    #   because of serial nature of this inquiry, we need to process in order of G, Y, B
    def update_knowledge(self, guess, response):
        tresp = {'G': [], 'Y': [], 'B': []}
        for i in range(0, len(response)):
            tresp[response[i]].append(i)
        for i in tresp['G']:
            # reduce word_set by intersecting with words with that letter in that posn
            self.solution_set = self.solution_set & letter_index[i][guess[i]]
            self.solved[i] = guess[i]
        for i in tresp["Y"]:
            # because it's Y not G, delete words with this letter in this spot
            # and reduce by intersecting words with this letter in some spot
            self.solution_set = (self.solution_set - letter_index[i][guess[i]]) & word_index[guess[i]]
            self.mandatory.add(guess[i])
        for i in tresp["B"]:
            # delete words with this letter in this spot
            self.solution_set = self.solution_set - letter_index[i][guess[i]]
            # only if letter not in mandatory or solved, delete all words with that letter
            if guess[i] not in self.mandatory and guess[i] not in self.solved.values():
                self.solution_set = self.solution_set - word_index[guess[i]]

    
    def is_solved(self):
        if len(self.solution_set) <= 1:
            return True
        else:
            return False
        
    # take guess and secret word and calculate a color response
    #   G - green (letter correct in proper position)
    #   Y - yellow (letter correc in wrong position)
    #   B - black or shadow (letter not in word)
    # because there can be duplicate letters, when we find a match we
    # replace the letter in the secret with space so it isn't found again
    @staticmethod
    def color_calc(guess, secret):
        listSecret = list(secret)
        response = WORDLEN * [' ']
        for i in range(len(guess)):
            if guess[i] == listSecret[i]:
                response[i] = 'G'
                listSecret[i] = ' '
        for i in range(len(guess)):
            if response[i] != 'G' and guess[i] in listSecret:
                response[i] = 'Y'
                listSecret[listSecret.index(guess[i])] = ' '
        response = [item if item != ' ' else 'B' for item in response]
        return ''.join(response)

    # given a guessword, returns the expected size of resulting groupings
    # that guess word could divide the solution words
    def score_guess(self, guess_word):
        rdict = {}
        for word in self.solution_set:
            result = Knowledge.color_calc(guess_word, word)
            if result in rdict:
                rdict[result] = rdict[result] + 1
            else:
                rdict[result] = 1
        return sum([v ** 2 for v in rdict.values()]) / sum(rdict.values())

    def all_mins(self, wordList, scoreList):
        # find minimum value
        mm = min(scoreList)
        #create list of all minimum words
        rv = [word for word in wordList if scoreList[wordList.index(word)] == mm]
        return rv

    def get_best_guess(self):
        if self.is_solved():
            return self.solution_set
        # place all  words in queue for multithreading
        start = time.time()
        p = mp.Pool(processes=THREADS)
        guess_results = list(p.map(self.score_guess, self.all_words))
        endtime = time.time()
        print(f'Threads {THREADS} total time: {endtime - start}')
        return self.all_mins(self.all_words, guess_results)
