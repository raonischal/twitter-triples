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
            if word[1]<10: continue  
            formatted_words=set()
            for substring in word[0]:
                substring=self.FormatWord(substring)
                if substring is None: continue
                substring=substring.lower()
                formatted_words.add(substring)
            formatted_words = list(formatted_words)
            #print(formatted_words)
            #keywords=self.select_most_relevant(formatted_words)
            wikiUrls=[]
            for word in formatted_words:
                wikiUrls.extend(wikipedia.search(word))
            wikiUrls=self.prune_search_space(formatted_words, wikiUrls)
            #print(" ")
            print(wikiUrls)
            Entities[formatted_words[0]]=self.SelectUrl(formatted_words[0],wikiUrls)

        return Entities

    def prune_search_space(self, formatted_words, wikiUrls):
        target_urls = set()
        for url in wikiUrls:
            similarity = 0
            for word in formatted_words:
                similarity += self.comparer.getSimilarity(word, url.encode("utf-8").lower())
            similarity = similarity / (len(formatted_words))
            #print(url + " => "+ str(similarity))
            if similarity >= 0.8:
                target_urls.add(url)
        return target_urls

    def FormatWord(self,word):
        try:
            word=word.encode("utf-8")
            word=word.replace("-"," ")
            word=word.replace("."," ")
            word=word.replace(","," ")
            word=word.replace(":"," ")
            word=word.replace(";"," ")
            word=word.replace("/"," ")
            word=word.replace("\\"," ")
            if word[0]=='#' or word[0]=='@':
                word =  re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', word)
                word = word[1:]
                word=word.strip()   
            return word
        except UnicodeEncodeError:
            return None

    def SelectUrl(self,searchTerm,wikiUrls):
        words_present={}
        #print("Search term is "+searchTerm)
        for url in wikiUrls:
            #print("url is : "+url)
            try:
                page = wikipedia.page(url)
                content=page.content
                title=page.title.lower()
                #similarity=self.comparer.getSimilarity(searchTerm,title.encode("utf-8"))
                #print("Word, title, similarity: "+searchTerm+" : "+title.encode("utf-8")+" : "+str(similarity))
                #if similarity<0.9: continue
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
                #best_word=self.select_most_relevant(words)[0][0].lower()
                #print(str(url))
                #print(countOfEntities)    
                words_present[page.url]=countOfEntities
                #ip=input("Enter")
            except wikipedia.exceptions.DisambiguationError:
                continue
            except wikipedia.exceptions.PageError:
                continue
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

    def select_shortest(self,words):
        #toDo: change this to most relevant words?, instead of shortest words??
        min_length=0
        min_word=words[0]
        for string in words:
                min_word=string
                min_length=len(string)
        return min_word
    
    def select_most_relevant(self,words):
        #print(words)        
        count_similar_words={}
        for word in words:
            score=0
            for string in words:
               value=self.comparer.getSimilarity(word,string)
               if value>0.95: score+=1
            count_similar_words[word]=score
        sorted_words = sorted(count_similar_words.items(), key=operator.itemgetter(1),reverse=True)
        sorted_words= [i[0] for i in sorted_words]
        size=len(sorted_words)/2
        if size<2:  return sorted_words
        return sorted_words[:size]

if __name__=="__main__":
    proper_nouns=['#TheDazedAndConfusedTour','chicago','#UKWantsJakeMiller']
    common_nouns=['penthouse','song','epic','tour','today','party','ghost','city']
    mapper=Wiki_Mapper(proper_nouns,common_nouns)
    entities=mapper.map_urls()
    for key,val in entities.items():
        print(key+" : "+val)
