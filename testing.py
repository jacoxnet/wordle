import json

# length of words we're working with
WORDLEN = 5

# word list - load in from json file
f = open('words_dictionary.json')
wordList = json.load(f)
f.close

# initialize activeWord list - dictionary with words of proper length
# and with T or F indicating whether word still active
activeWords = {}
for word in wordList:
    if len(word) == WORDLEN:
        activeWords[word] = True

# initialize global knowledge
# knownLetters:
#   a list with WORDLEN elements
#   if a letter is known to be in posn x, it's in that position in list
#   if no letter is known to be in that position, a zero

knownLetters = []
for pos in range (0, WORDLEN):
    knownLetters.append(0)

# anyLetters = list of letters that must be there but can be anywhere

anyLetters = []

# noLetters = list of letters not in word

noLetters = []

# test a word to see if comports with knowledge. Returns T or F
def testWord(word):
    # print ('Testing ', word)
    returnVal = True
    for i in range(len(word)):
        # note that for duplicate letters in guess, Wordle can return both Green (or Yellow) and Shadow
        # to account for this, returnVal needs to be True in that case
        if word[i] in noLetters and word[i] not in anyLetters and word[i] not in knownLetters:
            returnVal = False
        if (knownLetters[i] != 0):
            if (knownLetters[i] != word[i]):
                returnVal = False
    for j in range(0, len(anyLetters)):
        if (anyLetters[j] not in word):
            returnVal = False
    return returnVal

# update knowledge based on color response to guess word
# response is in the form of a string of G, S, and Y. 
#   G - green (letter correct in proper position)
#   Y - yellow (letter correc in wrong position)
#   S - shadow (letter not in word)
def updateKnowledge(guess, response):
    for i in range(len(response)):
        if (response[i] == 'G'):
            knownLetters[i] = guess[i]
        if (response[i] == 'Y'):
            anyLetters.append(guess[i])
        if (response[i] == 'S'):
            noLetters.append(guess[i])


# calculate score for word
# for each letter of guess word, calculate how many of the current wordlist
# have that letter in any position
def score(guess, valids):
    score = 0
    for i in range(len(guess)):
        # don't score duplicate letters
        if i > 0 and guess[i] in guess[0:i-1]:
            continue
        # print('Scoring ', guess[i])
        for word in valids:
            if guess[i] in word:
                    score = score + 1
        # print('Cumulative score ', score)
    return score

# take guess and secret word and calculate a color response
#   G - green (letter correct in proper position)
#   Y - yellow (letter correc in wrong position)
#   S - shadow (letter not in word)
def colorCalc(guess, secret):
    returnVal = ""
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            returnVal = returnVal + 'G'
        elif guess[i] in secret:
            returnVal = returnVal + 'Y'
        else:
            returnVal = returnVal + 'S'
    return returnVal

# go through active words and
# test to see if they meet current knowledge criteria
# mark them inactive if they don't
def updateWordList():

    for word in activeWords:
        if activeWords[word]:
            # print('testing ', word)
            activeWords[word] = testWord(word)

# return list of words marked active
def getValidWords():
    returnVal = []
    for word in activeWords:
        if activeWords[word]:
            returnVal.append(word)
    return returnVal

# figure out word marked active with largest score and return
def nextGuess():
    top = 0
    topword = ''
    valids = getValidWords()
    for word in valids:
        s = score(word, valids)
        if s > top:
            topword = word
            top = s
    print('Next guess is ', topword)
    return topword
