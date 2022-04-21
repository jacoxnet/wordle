from wordletrie import WORDLEN, Trie
from knowledge import Knowledge
from listofwords import SOLUTIONS, ALLWORDS
import json, signal

# initialize knowledge (which initializes underlying trie)

k = Knowledge(SOLUTIONS)
g = Knowledge(ALLWORDS + SOLUTIONS)

record = {}

print('Welcome to Wordle-Solve')
print('   word length =', WORDLEN)
print('\n')

print("Evaluating each solution word to see how many guesses it takes to solve")
 
def handler(signum, frame):
    print("Interrupt - saving record")
    f = open('record.json', 'w')
    f.write(json.dumps(record))
    f.close()
    exit(1)
 
signal.signal(signal.SIGINT, handler)

def processGuess(guess, target):
    print("Guessing ", guess)
    response = k.colorCalc(guess, target)
    print("Response ", response)
    return response

for i in range(len(SOLUTIONS)):
    target = SOLUTIONS[i]
    print("------------------------")
    print("solution word is ", target)
    guessNumber = 0
    k = Knowledge(SOLUTIONS)
    g = Knowledge(ALLWORDS + SOLUTIONS)
    while True:
        if guessNumber == 0:
            guess = "slate"
        else:
            guess = k.getBestGuess()[0]
        response = processGuess(guess, target)
        record[target] = {0: {guess: response}}
        if response == "GGGGG":
            print("solution found on guess ", guessNumber)
            break
        else:
            print("Updating knowledge")
            k.updateKnowledge(guess, response)
            guessNumber = guessNumber + 1

            