from upload import WORDLEN, all_words
from knowledge import Knowledge

if __name__ == '__main__':

    k = Knowledge(all_words.keys())

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
            print("Calculating best guess ...")
            guesses = k.get_best_guess()
            guess = guesses[0]
            print('New guess is ', guess)
            print('All guesses:', guesses)
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
            k.update_knowledge(guess, feedback)
            print('Feedback processed')
            if k.is_solved() == True:
                print("Solution found: ", k.solution_set)