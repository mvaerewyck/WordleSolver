## Wordle Solver
# Matthew Vaerewyck
# Started: 24 Feb 2023
import re

from WordleDic import wordleSolve

# handles user input and reports back and forth to WordleDic.py
userGuess = "slate"     # user's next guess, initialized as "slate"
return_pattern = re.compile('[yg.]{5}') #set up the wordle return feedback limits
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
        userGuess = input("Please input user's guess:")
        #userGuess = 'slate' #used for testing first go

        if len(userGuess) == 5:
            break
        else:
            print("Error, incorrect format - g for green, y for yellow, . for black:")

    # Get feedback from wordle (from User)
    while True:
        wordleReturn_input = input("Please input the response from Wordle (using yg.) :")
        # wordleReturn_input = '.g.yy' #used for testing
        wordleReturn = re.search(return_pattern,wordleReturn_input)

        if len(wordleReturn_input)>5 or wordleReturn == None:
            print("Error, incorrect format - g for green, y for yellow, . for black:")
        else:
            break

    if wordleReturn_input == 'ggggg':
        print('Another succesful solve!')
        break
    elif len(Wordle.wordlist) == []:
        print("Error! No more potential words remain!")
        break
    else:
         Wordle.wordleFeedback(userGuess, wordleReturn_input)
         print("Number of words remain: {}".format(len(Wordle.wordlist)))
         print(Wordle.wordlist)
