from wordletrie import WORDLEN
from knowledge import Knowledge
from listofwords import SOLUTIONS, ALLWORDS

# initialize knowledge (which initializes underlying trie)

k = Knowledge(SOLUTIONS)
g = Knowledge(ALLWORDS)

print('Welcome to Wordle-Solve')
print('   word length =', WORDLEN)
print('\n')
guess = ''
while True:
    guess = ""
    print('\n   1 - new guess')
    print('   2 - enter feedback from a guess')
    selection = int(input('choice: '))
    if selection < 1 or selection > 3:
        print('Invalid choice - try again')    
    if selection == 1:
        print("Calculating best guess ...")
        guess = k.getBestGuess()
        print('New guess is ', guess)
    if selection == 2:
        print('Word guess: ')
        if guess != '':
            print('(hit enter for prior guess ', guess, '): ')
        new_guess = input()
        if new_guess != '':
            guess = new_guess
        print('Feedback - ', WORDLEN, 'letters')
        feedback = input('B for Black, Y for Yellow, G for Green: ')
        if len(feedback) != WORDLEN or not min([c == 'B' or c == 'G' or c == 'Y' for c in feedback]):
            print('Error in input')
            continue
        k.updateKnowledge(guess, feedback)
        print('Feedback processed')
        print("solution trie: ", k)
        print("words:", k.allWords())