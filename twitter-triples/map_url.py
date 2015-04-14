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
            if word[1]<5: continue  
            print("Word is : "+str(word[0]))
            keyword=" ".join(word[0])
            if keyword[0]=='#' or keyword[0]=='@':
                keyword=self.FormatWord(keyword)
            keyword=keyword.lower()
            wikiUrls=wikipedia.search(keyword)
            print(wikiUrls)
            #Entities[formatted_word]=self.SelectUrl(keyword,wikiUrls)
            
                    

        return Entities

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
                        if word[1]<5:continue
                        regexp = re.compile(word)
                        if regexp.search(content) is not None: 
                            print(word)
                            countOfEntities+=1
                    words_present[page.url]=countOfEntities
                    for word in self.proper_entities:
                        if word[1]<5:continue
                        regexp = re.compile(word)
                        if regexp.search(content) is not None: 
                            print(word)
                            countOfEntities+=1
                    words_present[page.url]=countOfEntities
                    time.sleep(5) 
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
    proper_nouns=['#TheDazedAndConfusedTour','chicago','#UKWantsJakeMiller']
    common_nouns=['penthouse','song','epic','tour','today','party','ghost','city']
    mapper=Wiki_Mapper(proper_nouns,common_nouns)
    entities=mapper.map_urls()
    for key,val in entities.items():
        print(key+" : "+val)
