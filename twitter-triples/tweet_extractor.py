import tweepy
import codecs

class Tweet_extractor:
    consumer_key=""
    secret_key=""
    access_token_key=""
    access_secret_key =""        

    def __init__(self):
        self.consumer_key=input("Enter OAUTH consumer key: ")
        self.secret_key=input("Enter OAUTH consumer secret key: ")
        self.access_token_key=input("Enter OAUTH consumer Access Token key: ")
        self.access_secret_key=input("Enter OAUTH consumer Access Token Secret key: ")
    

    def get_tweets(self):
        auth = tweepy.OAuthHandler(self.consumer_key , self.secret_key)
        auth.set_access_token(self.access_token_key, self.access_secret_key )
        api = tweepy.API(auth)
        try:
            count=0
            for tweet in tweepy.Cursor(api.search,
                           q="Ronnie Price",
                           count=100,
					include_entities=True,
					lang="en",
                    #result_type="recent"
                    ).items():
                count+=1
                if count>1000: break
                finaltweet=tweet.text.replace("\n"," ")
                if finaltweet!="":
                    with codecs.open("tweets.txt",mode='a',encoding='utf-8') as tweetfile:
                        tweetfile.write("\n"+finaltweet)
        except tweepy.TweepError:
            time.sleep(60*20)
            


    def write_to_file(self):
        return 0;
    

if __name__=="__main__":
    extractor=Tweet_extractor()
    tweets=extractor.get_tweets()
    extractor.write_to_file()
