from wordletrie import WORDLEN, Trie
from knowledge import Knowledge
from listofwords import SOLUTIONS, ALLWORDS
import random

# initialize knowledge (which initializes underlying trie)

k = Knowledge(SOLUTIONS)
g = Knowledge(ALLWORDS + SOLUTIONS)

record = {}

print('Welcome to Wordle-Solve')
print('   word length =', WORDLEN)
print('\n')

print("Evaluating each solution word to see how many guesses it takes to solve")

for i in range(len(SOLUTIONS)):
    target = SOLUTIONS[i]
    print("------------------------")
    print("solution word is ", target)
    guessNumber = 0
    k = Knowledge(SOLUTIONS)
    g = Knowledge(ALLWORDS + SOLUTIONS)
    while True:
        if guessNumber == 0:
            print("Guessing ", "slate")
            record[target] = {0: "slate"}
            response = k.colorCalc("slate", target)
            print("Response is ", response)
            if response == "GGGGG":
                print("solution found on guess 0")
                break
            else:
                print("Updating knowledge")
                k.updateKnowledge("slate", response)
                guessNumber = guessNumber + 1
        else:
            guess = k.getBestGuess()[0]
            print("Guessing ", guess)
            record[target][guessNumber] = guess
            response = k.colorCalc(guess, target)
            print("Response is ", response)
            if response == "GGGGG":
                print("solution found on guess ", guessNumber)
                break
            else:
                print("Updating knowledge")
                k.updateKnowledge(guess, response)
                guessNumber = guessNumber + 1
            