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
    
    def __init__(self,proper_nouns,common_nouns):
        self.proper_entities=proper_nouns
        self.noun_entities=common_nouns

    def map_urls(self):
        Entities={}
        for word in self.proper_entities:
            print("Word is : "+word)
            if word[0]=='#' or word[0]=='@':
                word=self.FormatWord(word)
            wikiUrls=wikipedia.search(word, suggestion=True)
            print(wikiUrls)
            Entities[word]=self.SelectUrl(word,wikiUrls[0])
            
                    

        return Entities

    def FormatWord(self,word):
        word =  re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', word)
        word = word[1:]
        word=word.strip() 
        word=word.lower()  
        return word

    def SelectUrl(self,word,wikiUrls):
        words_present={}
        for url in wikiUrls:
            try:
                try:
                    page = wikipedia.page(url)
                except wikipedia.exceptions.DisambiguationError:
                    continue
                except wikipedia.exceptions.PageError:
                    continue
                print("Url is : "+url)    
                content=page.content
                countOfEntities=0
                for word in self.noun_entities:
                    #print(word)
                    regexp = re.compile(re.escape(word))
                    if regexp.search(content) is not None: 
                        print(word)
                        countOfEntities+=1
                words_present[page.url]=countOfEntities
                #time.sleep(5)  
            except wikipedia.exceptions.HTTPTimeoutError:
                time.sleep(60*20)
        maxcount=-1
        bestUrl=None
        for url,count in words_present.items():
            if(count>maxcount):
                maxcount=count
                bestUrl=url
        print("Best URL: "  + str(bestUrl))
        return bestUrl

if __name__=="__main__":
    proper_nouns=['#TheDazedAndConfusedTour','chicago','#UKWantsJakeMiller']
    common_nouns=['penthouse','song','epic','tour','today','party','ghost','city']
    mapper=Wiki_Mapper(proper_nouns,common_nouns)
    entities=mapper.map_urls()
    for key,val in entities.items():
        print(key+" : "+val)
