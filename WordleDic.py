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

        for i in [0,1,2,3,4]:
            if wordleReturn_input[i] == 'g':
                g_pos = g_pos + [i]
                self.g_list.append(wordleReturn_input[i])
            elif wordleReturn_input[i] == 'y':
                y_pos = y_pos + [i]#.append(i)
                self.y_list.append(wordleReturn_input[i])
            else:
                x_pos = x_pos + [i]
                self.x_list.append(wordleReturn_input[i])

        print("g is at locations: {}".format(g_pos))
        print("y is at locations: {}".format(y_pos))
        print(". is at locations: {}".format(x_pos))



#        for letter in wordleReturn_input:
#            pattern = re.compile('')

    
    def wordsThatRemain(self):
    ## use feedback to reduce the overall dictionary to
    ## make a list of words make a suggestion

        pass
        



    #this is to show julie how this works!!