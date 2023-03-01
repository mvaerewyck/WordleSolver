# constructor for WordleSolver.py
# This code will:
#
# find the 5-letter words from a scraped list on the web and store them


# import statements
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