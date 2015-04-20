import operator
import hierarchical_clustering

class Relationship_Extractor:

    def __init__(self,url_clusters):
        with open("tweets.txt",'r') as inputFile:
            self.lines=inputFile.readlines()
        self.url_clusters=url_clusters
       
    def replace_words(self):
        new_lines=[]
        for line in self.lines: 
            line=line.lower()
            for url,entities in self.url_clusters.items(): 
                entities.sort()
                for entity in entities:
                    line=line.replace('#'+entity,url+" ")
                    line=line.replace('@'+entity,url+" ")
                    line=line.replace(entity,url+" ")
            new_lines.append(line)
        self.lines=new_lines
                    
    
    def get_relationships(self):
        url_tweets={}
        for url in self.url_clusters.keys():
            for line in self.lines:
                if url in line:
                    if url not in url_tweets:  url_tweets[url]=[]
                    tweet_list=url_tweets[url]       
                    tweet_list.append(line)
                    url_tweets[url]=tweet_list
        for url in self.url_clusters.keys():
            for new_url in self.url_clusters.keys():
                if new_url==url: continue
                common_tweets=set(url_tweets[url])&set(url_tweets[new_url])
                bag_words=self.tf(common_tweets)
                print(url)
                print(new_url)
                ip=input("Enter word: ")
                print(bag_words)
                ip=input("Enter word: ")

        return 



    def tf(self,tweets):
            bag_words={}
            for tweet in tweets:
                words=tweet.split()
                for word in words:
                    if word not in bag_words: bag_words[word]=0
                    bag_words[word]+=1
            sorted_words = sorted(bag_words.items(), key=operator.itemgetter(1), reverse=True)
            return sorted_words

    '''
        for new_url in self.url_clusters.keys():
            tweet_list=""
            if url==new_url: continue
            for line in self.lines:
                if all(word in line for word in [url,new_url]) :
                    print(url)
                    print(new_url)
                    tweet_list+=line+" "
                    print(line)
                if url==new_url: common_tweets[url+" "+newurl]
       '''         
                   
     
        

if __name__=="__main__":
    # Sample results of top entitites
    url_clusters={}
    url_clusters['http://en.wikipedia.org/wiki/Masarat_Alam_Bhat']=['masarat alam', 'masarat alam', 'masarat alam\xe2\x80\x99s', 'masarat', 'masarat alam #rearrestmasarat', 'masarat alam', 'masarat alam saahab', 'masara', 'masarat alam nda govt', 'alam', 'masarat alam bhat', 'masarat alam', 'masarat alam', 'masarat alam arstng', 'masarat alam saab', 'lumpen masarat alam', 'masarat', 'superman masarat alam', 'masarat #alam', 'masarat sah']
    url_clusters['http://en.wikipedia.org/wiki/Kashmir']=['kashmiri', 'kashmir', 'kashmiri pandits', 'kashmir', 'kashmiri pandit', 'kasmiri', 'kashmir occupied india', 'kashmir', "kashmir's\xe2\x80\xa6"]
    url_clusters['Best URL: http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani']=['geelani', 'syed ali geelani', 'syed ali #geelani', 'syed ali shah geelani', 'geelani', 'mr  geelani', 'syed geelani']

    extractor=Relationship_Extractor(url_clusters)
    extractor.replace_words()
    extractor.get_relationships()
