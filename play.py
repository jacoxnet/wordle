import wordle_solve, json

# word list - load in from json file
f = open('words_dictionary.json')
wordList = json.load(f)
f.close

# initialize validWords list - dictionary with words of proper length
# and with T or F indicating whether word valid with current Knowledge
validWords = []
for word in wordList:
    if len(word) == wordle_solve.WORDLEN and word.isalpha():
        validWords.append(word)

# initialize knowledge

knowledge = wordle_solve.WordKnowledge()

print('Welcome to Wordle-Solve')
print('   word length =', wordle_solve.WORDLEN)
print('\n')
guess = ''
while True:
    print('\n   1 - new guess')
    print('   2 - enter feedback from a guess')
    print('   3 - remove a guess word not in Wordle dictionary\n')
    selection = int(input('choice: '))
    if selection < 1 or selection > 3:
        print('Invalid choice - try again')    
    if selection == 3:
        word = input('word to remove: ')
        validWords.remove(word)
    if selection == 1:
        guess = knowledge.nextGuess(validWords)
        print('New guess is ', guess)
    if selection == 2:
        print('Word guess: ')
        if guess != '':
            print('(hit enter for prior guess ', guess, '): ')
        new_guess = input()
        if new_guess != '':
            guess = new_guess
        print('Feedback - ', wordle_solve.WORDLEN, 'letters')
        feedback = input('B for Black, Y for Yellow, G for Green: ')
        if len(feedback) != wordle_solve.WORDLEN or not min([c == 'B' or c == 'G' or c == 'Y' for c in feedback]):
            print('Error in input')
            continue
        knowledge.update_knowledge(guess, feedback)
        validWords = knowledge.getUpdatedWordList(validWords)
        print('Feedback processed')
