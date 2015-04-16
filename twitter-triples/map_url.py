#
# given a list of relevant entities
# maps each one to its wikipedia url
# returns a list of urls
#

import re
import wikipedia
import time
from smith_waterman import Smith_Waterman
import operator

class Wiki_Mapper:
    entityUrls={}    
    proper_entities=[]
    noun_entities=[]    
    
    def __init__(self,proper_nouns,common_nouns):
        self.proper_entities=proper_nouns
        self.noun_entities=common_nouns
        self.comparer=Smith_Waterman(0.5)

    def map_urls(self):
        Entities={}
        for word in self.proper_entities:
            if word[1]<5: continue  
            formatted_words=[]
            for substring in word[0]:
                if substring[0]=='#' or substring[0]=='@':
                    substring=self.FormatWord(substring)
                substring=substring.lower()
                formatted_words.append(substring)
            keyword=self.select_most_relevant(formatted_words)
            #wikiUrls=wikipedia.search(keyword)
            #print("Word is : "+keyword)
            #print(wikiUrls)
            #Entities[keyword]=self.SelectUrl(word[0],wikiUrls)

        return Entities

    def FormatWord(self,word):
        word =  re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', word)
        word = word[1:]
        word=word.strip()   
        return word

    def SelectUrl(self,words,wikiUrls):
        words_present={}
        for url in wikiUrls:
            try:
                page = wikipedia.page(url)
                content=page.content
                countOfEntities=0
                for collection in self.noun_entities,self.proper_entities:
                    for word in collection:
                        if word[1]<5:continue
                        keyword=self.select_shortest(word[0])
                        regexp = re.compile(keyword)
                        if regexp.search(content) is not None: 
                            #print(word[0])                                
                            #print(keyword)
                            countOfEntities+=1
                title=page.title.lower()
                best_word=self.select_most_relevant(words).lower()
                similarity=getSimilarity(best_word,title)
                #print("Word, title, similarity: "+best_word+" : "+title+" : "+str(similarity))
                # ignore this page if title not matching
                if similarity<0.9: continue
                words_present[page.url]=countOfEntities
            except wikipedia.exceptions.DisambiguationError:
                continue
            except wikipedia.exceptions.PageError:
                continue
            except wikipedia.exceptions.HTTPTimeoutError:
                time.sleep(60*20)
                #print("Url is : "+url)    
               
        maxcount=-1
        bestUrl=None
        for url,count in words_present.items():
            if(count>maxcount):
                maxcount=count
                bestUrl=url
        print("Best URL: "  + str(bestUrl))
        return bestUrl

    def select_shortest(self,words):
        #toDo: change this to most relevant words?, instead of shortest words??
        min_length=0
        min_word=words[0]
        for string in words:
                min_word=string
                min_length=len(string)
        return min_word
    
    def select_most_relevant(self,words):
        print(words)        
        count_similar_words={}
        for word in words:
            score=0
            for string in words:
               value=self.comparer.getSimilarity(word,string)
               if value>0.95: score+=1
            count_similar_words[word]=score
        sorted_words = sorted(count_similar_words.items(), key=operator.itemgetter(1),reverse=True)
        print(sorted_words)

if __name__=="__main__":
    proper_nouns=['#TheDazedAndConfusedTour','chicago','#UKWantsJakeMiller']
    common_nouns=['penthouse','song','epic','tour','today','party','ghost','city']
    mapper=Wiki_Mapper(proper_nouns,common_nouns)
    entities=mapper.map_urls()
    for key,val in entities.items():
        print(key+" : "+val)
