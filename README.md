# WORDLE-SOLVE

This python3 program solves Wordle puzzles of any letter length.

## How to Use

- Set the correct puzzle length in `wordle_solve.py` (Wordle default is 5)
- Start the program using `python3 play.py`
- Select from the menu items 1-3
    - Item 1 - compute a new guess word
    - Item 2 - after entering the word in Wordle, input feedback from the wordle program to update the program's knowledge. Use one capital letter for each letter's color feedback:
        - G green
        - Y yellow
        - B black
    - Item 3 - remove a guess word that isn't in Wordle's dictionary. This is necessary because the program users its own dictionary (courtesy of https://github.com/dwyl/english-words) and doesn't use a copy of the Wordle program's lexicon. 
        - The dictionary used here is in `words_dictionary.json`. 
        - For convenience and comparison purposes, the Wordle lexicon as downloaded in February 2022 from the Wordle site is included here as `listofwords.py`

## How It Works

- The program uses the class `WordKnowledge` to capture all of the feedback the user has input from the Wordle program's responses. For each letter of the puzzle, the program tracks which letters have been confirmed (G), ruled out (B), or still remain possibilities. It separately keeps track of letters that are mandatory (Y) but whose position hasn't been determined yet.
- The program also keeps a current list of all possible words `validWords` that satisfy the `WordKnowledge` requirements.
- The program includes two methods for selecting new guesses:
    - The first and preferred method is 'dynamic max elimination' method. 
        - For each word in the `validWords` list, the program updates a temporary copy of the `WordKnowledge` assuming that word is the solution to the puzzle. 
        - It then recalculates the number of `validWords` based on that assumption. 
        - Each possible `validWord` is scored by noting how many words would be eliminated from the `validWords` list if that word is, in fact, the secret. 
        - The guess is the word with the highest score (or if words are tied for the max, a random selection from these words).
    - The second method is a character-frequency count. 
        - The program counts the frequencies of all letters in the remaining `validWords`.
        - The program scores each `validWord` by summing the counts for each of that word's letters.
        - The guess is the word (or if a tie, a random selection from the tied words) with the highest score.
- In my experience, the dynamic max elimination method usually outperforms the character-frequency count method by a substantial margin. The reason both methods are included is that it is impractical to calculate the dynamic max elimination method (at least on my hardware) when there are more than a few hundred `validWords`.
- Luckily, feedback from even one guess usually reduces the number of `validWords` to a few hundred or fewer.

## Results

In my experience, the program generally solves 5-letter Wordles in four or five guesses. Perhaps surprisingly, longer Wordles seem to be easier than shorter ones.