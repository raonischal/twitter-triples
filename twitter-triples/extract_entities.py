import sys, subprocess, operator

import hierarchical_clustering

from map_url import Wiki_Mapper

class Extract_entities:
    def __init__(self):
        self.ark_path = "ark-tweet-nlp-0.3.2/"
        self.word_count={} 
        return

    def tag_tweets(self, file_name):
        output = subprocess.Popen([self.ark_path + "runTagger.sh", file_name], 
            stdout = subprocess.PIPE).communicate()
        decoded_output = output[0].decode('utf-8')
        result = decoded_output.split("\n")
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
        self.proper_noun_count = {}
        for tweet in self.tagged_tweets:
            is_prev = False
            previous_token = ""
            for token in tweet:
                if token.endswith(("/^", "/Z")):
                    token = token[:-2]
                    if token.endswith("'s"):
                        token = token[:-2]
                    if is_prev == True:
                        previous_token = previous_token + " " + token
                    else:
                        is_prev = True
                        previous_token = token
                else:
                    if is_prev == True:
                        if previous_token in self.proper_noun_count:
                            self.proper_noun_count[previous_token] += 1
                        else:
                            self.proper_noun_count[previous_token] = 1
                        if previous_token not in proper_nouns:
                            proper_nouns.append(previous_token)
                    is_prev = False
        sorted_proper_nouns = sorted(self.proper_noun_count.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_proper_nouns

    def get_common_nouns(self):
        common_nouns = []
        self.common_noun_count = {}
        for tweet in self.tagged_tweets:
            is_prev = False
            previous_token = ""
            for token in tweet:
                if token.endswith(("/N", "/S")):
                    token = token[:-2]
                    if token.endswith("'s"):
                        token = token[:-2]
                    if is_prev == True:
                        previous_token = previous_token + " " + token
                    else:
                        is_prev = True
                        previous_token = token
                else:
                    if is_prev == True:
                        if previous_token in self.common_noun_count:
                            self.common_noun_count[previous_token] += 1
                        else:
                            self.common_noun_count[previous_token] = 1
                        if previous_token not in common_nouns:
                            common_nouns.append(previous_token)
                    is_prev = False
        sorted_common_nouns = sorted(self.common_noun_count.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_common_nouns


    def get_named_entity_clusters(self, nouns, IsCommonNoun):
        clusters = hierarchical_clustering.buildClusters(nouns)
        clusters_with_count = []
        for cluster in clusters:
            #print(cluster)
            count = 0
            for string in cluster:
                if IsCommonNoun is True:    count += self.common_noun_count[string]
                else:   count += self.proper_noun_count[string]
            clusters_with_count.append((cluster, count))
        clusters_with_count = sorted(clusters_with_count, key=lambda cluster: cluster[1], reverse=True)
        return clusters_with_count


if __name__ == "__main__":
    entityExtractor = Extract_entities()
    entityExtractor.tag_tweets("tweets.txt")
    proper_nouns = entityExtractor.get_proper_nouns()
    common_nouns = entityExtractor.get_common_nouns()
    common_entities = entityExtractor.get_named_entity_clusters([x[0] for x in common_nouns],True)
    proper_entities = entityExtractor.get_named_entity_clusters([x[0] for x in proper_nouns],False)
    #print("Proper entities")    
    #print(proper_entities)
    #print("Common entities")
    #print(common_entities)
        
    #ToDo: should be moved to a controller class
    wiki_mapper=Wiki_Mapper(proper_entities,common_entities)
    entity_url=wiki_mapper.map_urls()

