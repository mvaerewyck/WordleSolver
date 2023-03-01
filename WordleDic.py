# constructor for WordleSolver.py
# This code will:
#
# find the 5-letter words from pydictionary and store them
# deal with interface from WordleSolver and cut dworlown the stored list

# import statements
import re, requests
import numpy as np

# Construct Method
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

        # get list of words by grabbing regex captures of response
        # compile regex
        pattern = re.compile(r'<span itemprop="name">(\w+)</span>')

        # find all matches
        pattern_list = pattern.findall(wordlist_webpage.text)

        for result in pattern_list:
            wordlist.append(result)

        self.wordlist = wordlist

    #############################################################
    ## uses feedback from the webpage via regular expression to
    # limit what words remain
    #############################################################

    def wordleFeedback(self, userGuess, wordleReturn_input):

        # use feedback from wordle to remove potential words from
        # the list

        # find the locations of green, yellow, and black letters
        # save letters in lists

        for i, ch in enumerate(wordleReturn_input):
            if ch == 'g':
                self.g_list[i] = userGuess[i]
            elif ch == 'y':
                self.y_list.append([i, userGuess[i]])
            else:
                self.x_list.append(userGuess[i])

        # The following will build the regular expression to go through the word list and:
        # skip if the 'g' is not a ?
        # any yellows detected should be added to a 'not in that spot'
        # any blacks in the word should be removed

        X_list = ''.join(self.x_list)
        regexStr = "" # clear the regex string

        for i, ch in enumerate(self.g_list):
            if ch != '?':
                regexStr +="[{}]".format(ch)
            else:
                regexStr +="[^{}{}]".format(X_list,''.join([y[1] for y in self.y_list if y[0] == i]))

        # search wordlist with new constraints (not black, yellow not in those positions, green in those positions
        pattern = re.compile(regexStr) #
        pattern_list = list(filter(lambda x: re.match(pattern, x), self.wordlist))

        ## NEED TO FIGURE OUT THIS PART
        y_chars = [y[1] for y in self.y_list]
        yellow_list = []

        check = len(y_chars)
        yellow_list = word for word in pattern_list if all(y_chars in word)
                # yellow_list.append(word)

        #
        # if all(word in pattern_list for word in y_chars):
        #     yellow_list.append(word)

        self.wordlist = yellow_list