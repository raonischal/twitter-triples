import sys, subprocess

import hierarchical_clustering

class Extract_entities:
    def __init__(self):
        self.ark_path = "ark-tweet-nlp-0.3.2/"
        return

    def tag_tweets(self, file_name):
        output = subprocess.Popen([self.ark_path + "runTagger.sh", file_name], 
            stdout = subprocess.PIPE).communicate()
        result = output[0].split("\n")
        result = result[:-1]
        self.tagged_tweets = []
        for line in result:
            parts = line.split('\t')
            tokens = parts[0].split()
            tags = parts[1].split()
            pairs = ["%s/%s" % (tok, tag) for tok,tag in zip(tokens,tags)]
            self.tagged_tweets.append(pairs)
        return

    def get_proper_nouns(self):
        proper_nouns = []
        for tweet in self.tagged_tweets:
            is_prev = False
            previous_token = ""
            for token in tweet:
                if token.endswith(("/^", "/Z")):
                    token = token[:-2]
                    if token.endswith("'s"):
                        token = token[:-2]
                    if token not in proper_nouns:
                        proper_nouns.append(token)
                    if is_prev == True:
                        previous_token = previous_token + " " + token
                    else:
                        is_prev = True
                        previous_token = token
                else:
                    if is_prev == True:
                        if previous_token not in proper_nouns:
                            proper_nouns.append(previous_token)
                    is_prev = False
        return proper_nouns

    def get_named_entities(self, proper_nouns):
        clusters = hierarchical_clustering.buildClusters(proper_nouns)
        for cluster in clusters:
            print(cluster)
        return


if __name__ == "__main__":
    entityExtractor = Extract_entities()
    entityExtractor.tag_tweets("tweets.txt")
    proper_nouns = entityExtractor.get_proper_nouns()
    named_entities = entityExtractor.get_named_entities(proper_nouns)

