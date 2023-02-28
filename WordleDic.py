# constructor for WordleSolver.py
# This code will:
#
# find the 5-letter words from pydictionary and store them
# deal with interface from WordleSolver and cut dworlown the stored list

# import statements
import re, requests

# Construct Method
class wordleSolve():

    g_list = ['\\w' for _ in range(5)] # initialize as wild cards for purposes of re
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

    def wordsThatRemain(self):
    ## use feedback to reduce the overall dictionary to
    ## make a list of words make a suggestion

        # since wordleFeeback updated where the greens are, we're good

        # y_list should update the regex to include that letter but NOT in
        #   the position where it was discovered

        #remove any instance of a word that has
        X_list = ''.join(self.x_list)

        regexStr0 = r'([^{}{}][{}])'.format(X_list,''.join([y[1] for y in self.y_list if y[0] == 0]),self.g_list[0])+'{1}'
        regexStr1 = "([^{}{}][{}])".format(X_list,''.join([y[1] for y in self.y_list if y[0] == 1]),self.g_list[1])+'{1}'
        regexStr2 = "([^{}{}][{}])".format(X_list,''.join([y[1] for y in self.y_list if y[0] == 2]),self.g_list[2])+'{1}'
        regexStr3 = "([^{}{}][{}])".format(X_list,''.join([y[1] for y in self.y_list if y[0] == 3]),self.g_list[3])+'{1}'
        regexStr4 = "([^{}{}][{}])".format(X_list,''.join([y[1] for y in self.y_list if y[0] == 4]),self.g_list[4])+'{1}'

        regexStr = regexStr0 + regexStr1 + regexStr2 + regexStr3 + regexStr4

        # search wordlist with new constraints
        pattern = re.compile(regexStr) # if I change this to any of the indv. letter positions it works
        #pattern_list = pattern.findall(self.wordlist, re.MULTILINE)
        pattern_list = list(filter(lambda x: re.match(pattern, x), self.wordlist))

        ''' don't think I need to iterate through this...
        
        newWordlist = []
        for result in pattern_list:
            newWordlist.append(result)
        '''

        self.wordlist = pattern_list