#
# given a list of relevant entities
# maps each one to its wikipedia url
# returns a list of urls
#

import re
import wikipedia

class Wiki_Mapper:
    entityUrls={}    
    proper_entities=[]
    noun_entities=[]
    
    def __init__(self):
        self.proper_entities=['#TheDazedAndConfusedTour','chicago','#UKWantsJakeMiller']
        self.noun_entities=['penthouse','song','epic','tour','today','party','ghost','city']

    def map_urls(self):
        for proper_noun in self.proper_entities:
            if proper_noun[0]=='#' or proper_noun[0]=='@':
                words =  re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', proper_noun)
                words = words[1:]
                words=words.strip()
                print(words)

        return None
                



if __name__=="__main__":
    mapper=Wiki_Mapper()
    entities=mapper.map_urls()
    #for key,val in entities.items():
    #    print(key+" : "+val)
