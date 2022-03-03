import wordle_solve, json, copy

# word list - load in from json file
# f = open('bigdictionary.json')
f = open('wordledictionary.json')
wordList = json.load(f)
f.close

# initialize all_words and valid_words lists - dictionary with words of proper length
# and with T or F indicating whether word valid with current Knowledge
all_words = []
for word in wordList:
    if len(word) == wordle_solve.WORDLEN and word.isalpha():
        all_words.append(word)
valid_words = copy.deepcopy(all_words)

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
        print('Word to remove')
        if guess != '':
            print('  (hit enter for prior guess', guess, '):')
        removeword = input()
        if removeword == '':
            removeword = guess
        valid_words.remove(removeword)
        all_words.remove(removeword)
    if selection == 1:
        guess = knowledge.nextGuess(valid_words, all_words)
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
        valid_words = knowledge.getUpdatedWordList(valid_words)
        print('Feedback processed')