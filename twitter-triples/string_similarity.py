#
#    accepts a list of keywords
#    reduces it to a list of unique keywords
#
import jellyfish
import sys

class String_Matcher:
    entities=[]
    unique_entities=[]    

    def get_unique_entities(self):
        args=sys.argv
        wordList1=args[2].split()
        wordList2=args[3].split()
        for entity in wordList1:
            for word in wordList2:
                if jellyfish.soundex(entity) == jellyfish.soundex(word):return True
        return False
                

if __name__=="__main__":
    matcher=String_Matcher()
    return matcher.match_strings()
   

    
