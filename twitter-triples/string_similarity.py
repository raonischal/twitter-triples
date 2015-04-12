#
#    accepts a list of keywords
#    reduces it to a list of unique keywords
#
import jellyfish
import sys

class String_Matcher:
    entities=[]
    unique_entities=[]    

    def match_strings(self, string1, string2):
        wordList1=string1.split()
        wordList2=string2.split()
        for entity in wordList1:
            for word in wordList2:
                if jellyfish.soundex(entity) == jellyfish.soundex(word):return True
        return False
                

if __name__=="__main__":
    matcher=String_Matcher()
    #return matcher.match_strings()
   

    
