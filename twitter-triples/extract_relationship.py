import sys, subprocess, operator
import operator
import hierarchical_clustering

class Relationship_Extractor:

    def __init__(self,url_clusters,file_name):
        with open("tweets.txt",'r') as inputFile:
            self.lines=inputFile.readlines()
            self.lines=set(self.lines)
            self.lines=" ".join(self.lines)
            self.lines=self.lines.split('.')
        with open("temp-tweets.txt","w") as tempFile:
            for line in self.lines:
                tempFile.write(line)

        self.ark_path = "ark-tweet-nlp-0.3.2/"
        output = subprocess.Popen([self.ark_path + "runTagger.sh", "temp-tweets.txt"], 
            stdout = subprocess.PIPE).communicate()
        decoded_output = output[0].decode('utf-8')
        result = decoded_output.split("\n")
        result = result[:-1]
        self.tagged_tweets = []
        for line in result:
            new_line=""
            parts = line.split('\t')
            tokens = parts[0].split()
            tags = parts[1].split()
            pairs = ["%s/%s" % (tok, tag) for tok,tag in zip(tokens,tags)]
            for pair in pairs:
                new_line+=pair+" "
            #print(new_line)
            self.tagged_tweets.append(new_line)
            #ip=input("Enter data: ")
        #print(self.tagged_tweets)
        #with open("tweets.txt",'r') as inputFile:
        #    self.lines=inputFile.readlines()
        self.url_clusters=url_clusters
       
    def replace_words(self):
        new_lines=[]
        for line in self.tagged_tweets: 
            line=line.lower()
            line=line.encode('utf-8')
            for url,entities in self.url_clusters.items(): 
                entities.sort()
                for entity in entities:
                    line=line.replace('#'+entity,url)
                    line=line.replace('@'+entity,url)
                    line=line.replace(entity,url)
            new_lines.append(line)
        self.tagged_tweets=new_lines
                    
    
    def get_relationships(self):
        url_tweets={}
        for url in self.url_clusters.keys():
            for line in self.tagged_tweets:
                if url in line:
                    if url not in url_tweets:  url_tweets[url]=[]
                    tweet_list=url_tweets[url]       
                    tweet_list.append(line)
                    url_tweets[url]=tweet_list
        for url in self.url_clusters.keys():
            for other_url in self.url_clusters.keys():
                if other_url==url: continue
                common_tweets=set(url_tweets[url])&set(url_tweets[other_url])
                bag_words=self.tf(common_tweets,url,other_url)
                print(url)
                print(other_url)
                ip=input("Enter word: ")
                print(bag_words)
                ip=input("Enter word: ")

        return 



    def tf(self,tweets,url,other_url):
            bag_words={}
            for tweet in tweets:
                words=tweet.split()
                for word in words:
                    if url in word or other_url in word: continue
                    pos=word.split('/')
                    if pos[-1]!='n' and pos[-1]!='a' and pos[-1]!='v' and pos[-1]!='^' and pos[-1]!='@' and pos[-1]!='#' and pos[-1]!='r' and pos[-1]!='u': continue
                    if word not in bag_words: bag_words[word]=0
                    bag_words[word]+=1
            sorted_words = sorted(bag_words.items(), key=operator.itemgetter(1), reverse=True)
            return sorted_words

     
if __name__=="__main__":
    # Sample results of top entitites
    url_clusters={}
    url_clusters['http://en.wikipedia.org/wiki/Masarat_Alam_Bhat']=['masarat alam', 'masarat alam', 'masarat alam\xe2\x80\x99s', 'masarat', 'masarat alam #rearrestmasarat', 'masarat alam', 'masarat alam saahab', 'masara', 'masarat alam nda govt', 'alam', 'masarat alam bhat', 'masarat alam', 'masarat alam', 'masarat alam arstng', 'masarat alam saab', 'lumpen masarat alam', 'masarat', 'superman masarat alam', 'masarat #alam', 'masarat sah']
    url_clusters['http://en.wikipedia.org/wiki/Kashmir']=['kashmiri', 'kashmir', 'kashmiri pandits', 'kashmir', 'kashmiri pandit', 'kasmiri', 'kashmir occupied india', 'kashmir', "kashmir's\xe2\x80\xa6"]
    url_clusters['http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani']=['geelani', 'syed ali geelani', 'syed ali #geelani', 'syed ali shah geelani', 'geelani', 'mr  geelani', 'syed geelani']

    extractor=Relationship_Extractor(url_clusters,"tweets.txt")
    extractor.replace_words()
    extractor.get_relationships()
