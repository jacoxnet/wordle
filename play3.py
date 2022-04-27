from wordletrie import WORDLEN, Trie
from knowledge import Knowledge
from shortlist import SOLUTIONS, ALLWORDS
import json, signal



def handler(signum, frame):
    print("Interrupt - saving record")
    f = open('record.json', 'w')
    f.write(json.dumps(record))
    f.close()
    raise RuntimeError

def processGuess(guess, target):
    print("Guessing ", guess)
    response = k.colorCalc(guess, target)
    print("Response ", response)
    return response

if __name__ == '__main__':
    # initialize knowledge (which initializes underlying trie)

    k = Knowledge(SOLUTIONS)
    g = Knowledge(ALLWORDS + SOLUTIONS)

    record = {}

    print('Welcome to Wordle-Solve')
    print('   word length =', WORDLEN)
    print('\n')

    print("Evaluating each solution word to see how many guesses it takes to solve")

    STARTGUESS = 'roate'



 
    signal.signal(signal.SIGINT, handler)



    for i in range(len(SOLUTIONS)):
        target = SOLUTIONS[i]
        print("------------------------")
        print("solution word is ", target)
        guessNumber = 0
        k = Knowledge(SOLUTIONS)
        g = Knowledge(ALLWORDS + SOLUTIONS)
        while True:
            if guessNumber == 0:
                guess = STARTGUESS
            else:
                guess = k.getBestGuess()[0]
            response = processGuess(guess, target)
            # print ('recording {', target, ': {', guessNumber, ': {', guess, ': ', response, '}}')
            if target in record:
                record[target][guessNumber] = {guess: response}
            else:
                record[target] = {guessNumber: {guess: response}}
            if response == "GGGGG":
                print("solution found on guess ", guessNumber)
                break
            elif guessNumber > 100:
                print("solution not found")
                break
            else:
                print("Updating knowledge")
                k.updateKnowledge(guess, response)
                guessNumber = guessNumber + 1

    f = open('record.json', 'w')
    f.write(json.dumps(record))
    f.close()
    histo = {}
    for k, v in record.items():
        if len(v) in histo:
            histo[len(v)] = histo[len(v)] + 1
        else:
            histo[len(v)] = 1
    print("Total words evaluated: ", sum(histo.values()))
    print("Average guesses per word: ", sum([k * v for k, v in histo.items()])/sum(histo.values()))
    for item in sorted(histo):
        print (item, ": ", histo[item])
    print