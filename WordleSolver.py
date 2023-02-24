## Wordle Solver
# Matthew Vaerewyck
# Started: 24 Feb 2023

from WordleDic import wordleSolve

# handles user input and reports back and forth to WordleDic.py

userGuess = "slate"     # user's next guess, initialized as "slate"
availWords = {""}     # dictionary list of available words
wordleReturn = "....."  # this will be the user's feedback from wordle

print('-- Fetching word list -- ')
Wordle = wordleSolve.getWordList

print("You guessed first: ", userGuess)
wordleReturn = input("Please input the response from Wordle (using yg.) :")


wordleSolve.wordleFeedback(userGuess,wordleReturn)




