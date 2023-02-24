# constructor for WordleSolver.py
# This code will:
#
# find the 5-letter words from pydictionary and store them
# deal with interface from WordleSolver and cut dworlown the stored list

# import statements


# stdlib
import re
import requests

#from PyDictionary import PyDictionary as pyDic

# Construct Method
class wordleSolve:
    def getWordList(self):
        wordlist = []
        # Get 5-letter words
                
        
        # get list of five-letter words from meaningpedia.com
        # https://en.wikipedia.org/wiki/Lists_of_English_words#External_links
        meaningpedia_resp = requests.get("https://meaningpedia.com/5-letter-words?show=all")

        # get list of words by grabbing regex captures of response
        # compile regex
        pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
        
        # find all matches
        pattern_list = pattern.findall(meaningpedia_resp.text) 

        
        for result in pattern_list:
            wordlist.append(result)

        self.word_list = wordlist.split
    
    def wordsThatRemain():
        # use feedback to reduce the overall dictionary to 
        # make a list of words make a suggestion

        pass
        
    def wordleFeedback(userGuess,wordleReturn):

        # use feedback from wordle to remove potential words from
        # the list
        
        pass


    #this is to show julie how this works!!