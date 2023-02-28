# constructor for WordleSolver.py
# This code will:
#
# find the 5-letter words from pydictionary and store them
# deal with interface from WordleSolver and cut dworlown the stored list

# import statements
import re, requests

# Construct Method
class wordleSolve():

    g_list = []
    y_list = []
    x_list = []

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

        #initialize positional lists of good letters
        g_pos = []
        y_pos = []
        x_pos = []

        # find the locations of green, yellow, and black letters
        # save letters in lists

        for i, ch in enumerate(wordleReturn_input):
            if ch == 'g':
                g_pos.append(i)
                self.g_list.append(ch)
            elif ch == 'y':
                y_pos.append(i)
                self.y_list.append(ch)
            else:
                x_pos.append(i)
                self.x_list.append(ch)

## Debugging test point
#        print("g is at locations: {}".format(g_pos))
#        print("y is at locations: {}".format(y_pos))
#        print(". is at locations: {}".format(x_pos))

    def wordsThatRemain(self):
    ## use feedback to reduce the overall dictionary to
    ## make a list of words make a suggestion

        pass
        



    #this is to show julie how this works!!