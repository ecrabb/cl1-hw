# Author: Erin Smith Crabb
# Date: Sep 21, 2013

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize


class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        #Initialize the list of possible syllable counts
        self.possSyllList=[]

        #initialize dictionary default value, in case the word isn't found
        defaultSyllables = 1

        #take word input and use it as the dictionary key to get the phones
        self.wordPhones = self._pronunciations.get(word, defaultSyllables)

        #look and see if there are phones or a default value.  If not, continue
        if self.wordPhones != 1:

            #loop through each list of possible phones
            for self.eachPronunciation in self.wordPhones:

                #prepare a variable to count syllables
                self.syllableCount=0

                #if a stress value occurs in a phone, add one to the syllable count
                for self.eachSyllable in self.eachPronunciation:
                    if '0' in self.eachSyllable:
                        self.syllableCount+=1
                    if '1' in self.eachSyllable:
                        self.syllableCount+=1
                    if '2' in self.eachSyllable:
                        self.syllableCount+=1

                #append the total syllable count to the empty list of possibilities
                self.possSyllList.append(self.syllableCount)

            #figure out what to return - if only one option, return that
            if len(self.possSyllList)==1:
                return self.possSyllList[0]

            #if more than one option, take the minimum
            if len(self.possSyllList)>=2:
                return min(self.possSyllList)

        #otherwise return 1
        else:
            return 1

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        #take each input and use it as the dictionary key to get the phones
        self.pronunA = self._pronunciations[a]
        self.pronunB = self._pronunciations[b]

        #vowels will be used to determine the rhyme pattern
        self.vowelList=['A','I','E','O','U']

        #reverse each set of pronunciations so that the last syllables are first
        for self.eachOptionA in self.pronunA:
            self.eachOptionA.reverse()

        for self.eachOptionB in self.pronunB:
            self.eachOptionB.reverse()

        #create a list that we will fill with indexes of vowels
        self.finalSyllInd =[]

        #look at each possible pronunciation
        for self.eachOptionA in self.pronunA:
            #look at each syllable in the pronunciation
            for self.eachSyllableA in self.eachOptionA:
                #if it's a vowel syllable, add the index to the list
                if self.eachSyllableA[0] in self.vowelList:
                    self.finalSyllInd.append(self.eachOptionA.index(self.eachSyllableA))
            #choose the minimum vowel index
            self.vowelIndex=min(self.finalSyllInd)

            #compare each possible pronunciation set up to the first vowel
            for self.eachOptionB in self.pronunB:
                #if the syllables match, return true
                if self.eachOptionA[:self.vowelIndex+1]==self.eachOptionB[:self.vowelIndex+1]:
                    return True
                
        #otherwise, return false
        else:
            return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """

        #split the text by newline
        self.textLines = text.split('\n')

        #create empty list for last words from lines
        self.lastWords = []

        #pull out words at the end of the lines
        for self.eachLine in self.textLines:
            #extract the last word from each line and append it to the empty list
            tokenizedline=word_tokenize(self.eachLine)
            #if the tokenized line has text, append it to the last words string
            if tokenizedline!=[]:
                lastWord=tokenizedline[-1]
                if ',' in lastWord:
                    lastWord=lastWord[:-1]
                self.lastWords.append(lastWord)

        #check the length of the list
        if len(self.lastWords)==5:
            self.truthtest=[]
            #Check if the last words in lines 1 and 5 rhyme (indexes 0 and 4)
            if LimerickDetector.rhymes(self,self.lastWords[0], self.lastWords[4])==True:
                #check if the last words on lines 3 and 4 rhyme (indexes 2 and 3)
                if LimerickDetector.rhymes(self,self.lastWords[2],self.lastWords[3])==True:
                    return True
                #if lines 3 and 4 (last words 2 and 3) don't rhyme, return false
                else:
                    return False
            #if lines 1 and 5 don't rhyme, return false
            else:
                return False
        #if there are not 5 last words, return false
        else:
            return False

    def apostrophe_tokenize(self, text):
        """
        This function takes a text, tokenizes it and then re-joins words that were split so
        that they may be looked up in the CMU Pronunciation Dictionary. 
        It then returns the altered list.
        """

        #tokenize the text using the pre-existing function in NLTK
        self.tokenizedLines=word_tokenize(self.text)

        #if an apostrophe is in tokenizedLines, get its index
        if '\'' in self.tokenizedLines:
            self.apostInd = self.tokenizedLines.index('\'')
            
            #recreate the word by concatenating the strings around the apostrophe
            self.replaceWord = self.tokenizedLines[self.apostInd-1]+self.tokenizedLines[self.apostInd+1]

            #put the word where the apostrophe used to be
            self.tokenizedLines[apostInd]= self.replaceWord

            #remove the word fragments, second part first
            del self.tokenizedLines[apostInd+1]
            del self.tokenizedLines[apostInd-1]

        return self.tokenizedLines

    def guess_syllables(self, unknownWord):
        """
        This function takes a word and makes guesses as to its length, if it
        is not in the CMU Pronunciation Dictionary.
        """

        #make lists of consonants and vowels
        self.consonants=['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','x','z']
        self.vowels=['a','e','i','o','u','y']

        #start the syllable counter
        self.syllablecount=0

        #start the CV string map
        self.cvMap = []
        #start the index counter for counting syllables later on
        self.wordPosition=0
        
        #check and make sure the word is not in the CMU Dictionary
        if self.unknownWord in self._pronunciations:
            #if it is, get the syllable count from the other function
            LimerickDetector.num_syllables(self.unknownWord)

        #if it is not, create a C and V representation of the string
        else:
            for self.eachletter in self.unknownWord:
                if self.eachletter in self.vowels:
                    self.cvMap.append('v')
                if self.eachletter in self.consonants:
                    self.cvMap.append('c')
                if self.eachletter not in self.vowels and self.eachletter not in self.consonants:
                    pass

            #if the CV representation list starts with a C
            if self.cvMap[0]=='c':

                #start a counter for the while loop
                self.indexCount = len(self.cvMap)-1

                #while a valid index in the list, if you find a 'c' followed by a 'v'
                #add 1 to the syllable count
                while self.indexCount > 0:
                    if self.cvMap[self.wordPosition] =='c' and self.cvMap[self.wordPosition+1]=='v':
                        self.syllablecount+=1
                    else:
                        pass
                    #subtract one from the while loop
                    self.indexCount-=1
                    #add one to the word index count
                    self.wordPosition+=1

            #if the CV representation list starts with a V
            if self.cvMap[0]=='v':

                #immediately add 1 as it begins with an open syllable
                self.syllablecount+=1

                #start the while loop counter again
                self.indexCount = len(self.cvMap)-1

                #while a valid index in the list, if you find a 'c' followed by a 'v'
                #add 1 to the syllable count
                while self.indexCount > 0:
                    if self.cvMap[self.wordPosition] =='c' and self.cvMap[self.wordPosition+1]=='v':
                        self.syllablecount+=1
                    else:
                        pass
                    #subtract one from the while loop
                    self.indexCount-=1
                    #add one to the word index count
                    self.wordPosition+=1

            #return the syllable count
            return self.syllablecount
                    
                    
