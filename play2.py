from wordletrie import Trie, WORDLEN
import json, copy

from listofwords import SOLUTIONS

# create root TRIE and insert all words

ROOT = Trie()
for word in SOLUTIONS:
    ROOT.insert(word)

print('Welcome to Wordle-Solve')
print('   word length =', WORDLEN)
print('\n')
guess = ''
while True:
    print('\n   1 - new guess')
    print('   2 - enter feedback from a guess')
    selection = int(input('choice: '))
    if selection < 1 or selection > 3:
        print('Invalid choice - try again')    
    if selection == 1:
        guess = 'TESTINGGUESS'
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
        # knowledge.update_knowledge(guess, feedback)
        # valid_words = knowledge.getUpdatedWordList(valid_words)
        print('Feedback processed')