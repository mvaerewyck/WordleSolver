## Wordle Solver
# Matthew Vaerewyck
# Started: 24 Feb 2023
import re

from WordleDic import wordleSolve

# handles user input and reports back and forth to WordleDic.py
Wordle = wordleSolve()

try:
    print('-- Fetching word list -- ')
    Wordle.getWordList()

except:
    print("Failure in retrieving list")

print ('-- World list obtained --')

while True:

    # Get user's guess
    while True:
        userGuess = input("\n\nPlease input user's guess:")
        if len(userGuess) == 5: # could do more testing here for proper form
            break
        else:
            print("Error! Guess can only be a 5-letter word")

    # Get feedback from wordle (via User)
    while True:
        wordleReturn_input = input("Please input the response from Wordle (using yg.) :")
        return_pattern = re.compile('[yg.]{5}')  # set up the wordle return feedback limits
        wordleReturn = re.search(return_pattern,wordleReturn_input)

        # ensure that the length of the feedback and the type of feedback is correct
        if len(wordleReturn_input)>5 or wordleReturn == None:
            print("Error, incorrect format - g for green, y for yellow, . for black:")
        else:
            break

    if wordleReturn_input == 'ggggg':
        print('Another succesful solve!')
        break
    elif len(Wordle.wordlist) == 1:
        print("The correct answer is {}".format(Wordle.wordlist))
        break
    elif Wordle.wordlist == []:
        print("Error! No more words to guess. Try again.")
        break
    else:
         Wordle.wordleFeedback(userGuess, wordleReturn_input)
         print("Number of words remain: {}".format(len(Wordle.wordlist)))
         counter = 0
         for word in Wordle.wordlist:
            print(word, end=', ')
            counter += 1
            if counter == 15:
                print("")
                counter = 0
