# Lose at Hangman

## now easier than ever before

Test out the guessing engine by running <code>python3 hangman.py {word}</code>, 
for instance, to test the word interpolation, run <code>python3 hangman.py interpolation</code>.

To run in interactive mode, run <code>python3 hangman.py --interactive</code>

Rules: Scrabble rules, basically. No proper nouns, no abbreviations, 
etc. Scrabble only has words up to 15 characters long, but most common words of greater length are also included, as well as some classics.

Currently seeking better datasets. If you have a free-as-in-freedom list of >100k English words with familiarity stats for each one, submit a PR. If you have a comparable list for any other language, submit a PR.
