#
# given a list of relevant entities
# maps each one to its wikipedia url
# returns a list of urls
#

import re
import wikipedia
import time

class Wiki_Mapper:
    entityUrls={}    
    proper_entities=[]
    noun_entities=[]
    
    def __init__(self):
        self.proper_entities=['#TheDazedAndConfusedTour','chicago','#UKWantsJakeMiller']
        self.noun_entities=['penthouse','song','epic','tour','today','party','ghost','city']

    def map_urls(self):
        Entities={}
        for word in self.proper_entities:
            print("Word is : "+word)
            if word[0]=='#' or word[0]=='@':
                word=self.FormatWord(word)
            wikiUrls=wikipedia.search(word)
            Entities[word]=self.SelectUrl(word,wikiUrls)
            
                    

        return None

    def FormatWord(self,word):
        word =  re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', word)
        word = word[1:]
        word=word.strip()   
        return word

    def SelectUrl(self,word,wikiUrls):
        try:
            words_present={}
            for url in wikiUrls:
                    print("Url is : "+url)
                    page = wikipedia.page(url)
                    content=page.content
                    countOfEntities=0
                    for word in self.noun_entities:
                        regexp = re.compile(word)
                        if regexp.search(content) is not None: 
                            print(word)
                            countOfEntities+=1
                    words_present[page.url]=countOfEntities
                    time.sleep(20) 
        except:
            time.sleep(60*20) 
        maxcount=-1
        bestUrl=None
        for url,count in words_present.items():
            if(count>maxcount):
                maxcount=count
                bestUrl=url
        return bestUrl

if __name__=="__main__":
    mapper=Wiki_Mapper()
    entities=mapper.map_urls()
    #for key,val in entities.items():
    #    print(key+" : "+val)
