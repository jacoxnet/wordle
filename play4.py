import thewords
from wordletrie import WORDLEN, Trie
from knowledge import Knowledge


if __name__ == '__main__':
    
    guesswords, solutions = thewords.get_wordlists()
    # initialize knowledge (which initializes underlying trie)
    k = Knowledge(solutions)
    g = Knowledge(guesswords)

    print('Welcome to Wordle-Solve')
    print('   word length =', WORDLEN)
    print('\n')
    guess = ''
    while True:
        print('\n   1 - ask me to make a new guess')
        print('   2 - enter feedback from a guess')

        selection = int(input('choice: '))
        if selection < 1 or selection > 2:
            print('Invalid choice - try again')    
        if selection == 1:
            print("Calculating best guess ...")
            guesses = k.getBestGuess(guesswords)
            guess = guesses[0]
            print('Best guess is ', guess)

        if selection == 2:
            print('Word guess: ')
            if guess != '':
                print('(hit enter for prior guess ', guess, '): ')
            new_guess = input()
            if new_guess != '':
                guess = new_guess
            print('Feedback - ', WORDLEN, 'letters')
            feedback = input('B for Black, Y for Yellow, G for Green: ').upper()
            if len(feedback) != WORDLEN or not min([c == 'B' or c == 'G' or c == 'Y' for c in feedback]):
                print('Error in input')
                continue
            k.updateKnowledge(guess, feedback)
            print('Feedback processed')
            print('Remaining possible solutions: ', len(k.allWords()))
            if len(k.allWords()) < 50:
                print(k.allWords())
            if len(k.allWords()) == 1:
                print("Solution found: ", k.allWords()[0])