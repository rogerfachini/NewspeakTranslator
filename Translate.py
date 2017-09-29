#Newspeak translation / censoring engine

import logging, re

#import nltk
#nltk.download('wordnet')
#from nltk.corpus import wordnet as wn
#from itertools import chain

TRANS_IDX = {'think': ['thought'],
             'knife': ['cut'],
             'speedful':['rapid'],
             'speedwise':['quickly'],
             'goodwise':['well'],
             'uncold':['warm', 'hot', 'sunny'],
             'plus-':['very'],
             'doubleplus-':['extremely', 'incredibly'],
             'ungood':['bad', 'terrible'],
             'good':['positive', 'plus', 'right'],
             'dark':['unlight'],
             'thinked':['thought'],
             'mans':['men'],
             'lifes':['lives'],
             'goodthink':['orthodoxy'],
             'thinkpol':['thought police'],
             'crimethink':['thoughtcrime'],
             'ingsoc':['english socialism'],
             'BB':['big brother'],
             'thoughtcrime':['honor', 'justice', 'free', 'morality', 'internationalism', 'freedom'],
             'oldthink':['democracy', 'religon', 'science', 'god', 'liberty', 'equality', 'noble', 'nobility'],
             'goodsex':['chastity'],
             'sexcrime':['adultery', 'reproduction', 'intercourse', 'sex', 'homosexual'],
             'prolefeed':['entertainment'],
             'joycamp':['labor camp', 'forced labor camp'],
             'recdep':['records department'],
             'ficdep':['fiction department'],
             'teledep':['teleprograms department'],
             'comintern':['communist international'],
             'minitrue':['ministry of truth'],
             'miniluv':['ministry of love'],
             'minipax':['ministry of peace'],
             'miniplen':['ministry of plenty'],
             '-':['a ', 'an ', 'the', 'in ', ]}


PUNCTUATION = [' ', '.', '!', '?', ',', '\n', ';', '']
             

class Translator:
    def __init__(self):
        #self.generateBannedWords()
        self.NS_DICT = {}
        self.NS_DICT_BY_SIZE = {}
        for nsw, osws in TRANS_IDX.iteritems():
            for osw in osws:
                self.NS_DICT.update({osw:nsw})

        for osw, nsw in self.NS_DICT.iteritems():
            spaces = osw.count(' ')
            if not spaces in self.NS_DICT_BY_SIZE.keys(): self.NS_DICT_BY_SIZE.update({spaces:{}})
            self.NS_DICT_BY_SIZE[spaces].update({osw:nsw})
                    
        pass

    def translateSentence(self, inputText):
        whitespaceSplit = inputText.strip()
        cleanInputText = inputText.strip().replace(',', ' ').replace('.', ' ').replace('?', ' ').replace('!', ' ')
        lowerInputText = whitespaceSplit.lower()
        activeText = str(whitespaceSplit)

        sizes =  self.NS_DICT_BY_SIZE.keys()
        sizes.sort()
        sizes.reverse()

        for s in sizes:
            ACTIVE_NS_DICT = self.NS_DICT_BY_SIZE[s]
            for punc in PUNCTUATION:
                for osw, nsw in ACTIVE_NS_DICT.iteritems():
                    if nsw[-1] == '-': 
                        repNsw = nsw[:-1]
                    else:
                        repNsw = nsw + punc
                    strLoc = lowerInputText.find(osw)
                    if strLoc == -1: continue


                    pattern  = re.compile(re.escape(osw + punc), re.IGNORECASE)
                    activeText =  pattern.sub(repNsw, activeText)
        return activeText.replace('  ', ' ')

    def getCaseMap(self, string):
        return [x[0].isupper() for x in string.strip().split()]


if __name__ == '__main__':
    exampletext = """
I had an extremely bad day at the Ministry of Truth, working in the Records Department. 
Big Brother is very bad. He enforces orthodoxy. 
I endorse science, adultery, and freedom. I thought I was doing the right thing
I place the lives of men above the Party, above Big Brother, and above all the principles of English Socialism. 
These extremely positive messages denouncing the party will surely be read by the Thought Police, who will send me to the Ministry of Love and to a forced labor camp. 
The weather is very sunny today. 
"""
    translator = Translator()
    #output = translator.translateSentence(exampletext)
    #print "%s \n \n%s" %(exampletext, output)

    while True:
        a = raw_input(":")
        output = translator.translateSentence(a)
        print output + '\n'

