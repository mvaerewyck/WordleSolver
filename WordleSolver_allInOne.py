## Wordle Solver
# Matthew Vaerewyck
# Started: 24 Feb 2023
import re, requests

class wordleSolve():

    g_list = ['?' for _ in range(5)] # initialize as wild cards for purposes of re
    y_list = [] # 2D List for yellows and their positions
    x_list = [] # list of letters not in word

    def getWordList(self):

        #############################################################
        ## pulls a list of 5 letter words from the web
        #############################################################
        wordlist = []
        # Get 5-letter words

        # get list of five-letter words from meaningpedia.com
        # https://en.wikipedia.org/wiki/Lists_of_English_words#External_links
        wordlist_webpage = requests.get('https://meaningpedia.com/5-letter-words?show=all')

        # get list of words by finding words inside html headers
        pattern = re.compile(r'<span itemprop="name">(\w+)</span>')

        # find all matches by scraping the webpage
        pattern_list = pattern.findall(wordlist_webpage.text)

        for result in pattern_list:
            wordlist.append(result)

        self.wordlist = wordlist

    def wordleFeedback(self, userGuess, wordleReturn_input):
        #############################################################
        # uses feedback from the webpage via regular expression to
        # limit what words remain
        #############################################################

        for i, ch in enumerate(wordleReturn_input):
            if ch == 'g':
                self.g_list[i] = userGuess[i]
            elif ch == 'y':
                self.y_list.append([i, userGuess[i]])
            else:
                self.x_list.append(userGuess[i])

        # The following will build the regular expression to go through the word list and:
        # ensure a 'g' letter is placed in that spot
        # any yellows detected should be added to a 'not in that spot'
        # any blacks in the word should be removed

        X_list = ''.join(self.x_list) # make a list of the letters not in the word
        regexStr = ""                 # clear the regex string

        for i, ch in enumerate(self.g_list):
            if ch != '?':
                regexStr +="[{}]".format(ch)
            else:
                regexStr +="[^{}{}]".format(X_list,''.join([y[1] for y in self.y_list if y[0] == i]))

        # search wordlist with new constraints (not black, yellow not in those positions, green in those positions
        pattern = re.compile(regexStr) #
        pattern_list = list(filter(lambda x: re.match(pattern, x), self.wordlist))

        ## I feel like there should be a more 'pythonic' way to do this::
        y_chars = [y[1] for y in self.y_list] #make a list of known yellow chars
        yellow_list = []

        # Go through the list of words, ensure that each word in the list contains at least the
        # yellow letters in the word
        for word in pattern_list:
            i=0
            for ch in y_chars:
                if ch in word:
                    i += 1
                if i == len(y_chars): # if the word contains all the yellow letters, append
                    yellow_list.append(word)

        self.wordlist = yellow_list


def main():
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
                    
if __name__ == "__main__":
    main()