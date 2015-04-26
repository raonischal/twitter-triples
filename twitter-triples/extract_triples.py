import sys, subprocess, operator, time
import rdflib
import nltk

from pattern.en import conjugate
from sparql_endpoint_interface import SPARQL_Endpoint_Interface

class Relation_Extractor:
    def __init__(self, tweets, entities, triple_store):
        self.tweets = tweets
        self.entities = entities
        self.blank_nodes_map = {}
        #self.sparqlEndpoint = SPARQL_Endpoint_Interface()
        #self.uriForIs = self.sparqlEndpoint.getWordnetURI("be")
        self.uriForIs = "is"
        self.triple_store = triple_store
        self.triples = []

    def add_to_triple_store(self, tup, isLiteral=True):
        #subject = rdflib.URIRef(tup[0])
        #predicate = rdflib.URIRef(tup[1])
        #if isLiteral == True:
        #    obj = rdflib.Literal(tup[2])
        #else:
        #    obj = rdflib.URIRef(tup[2])
        #self.triple_store.add((subject, predicate, obj))
        return

    def preprocess_tweets(self):
        processed_tweets = []
        for tweet in self.tweets:
            processed_tweet = []
            for word in tweet:
                pair = word.rsplit("/", 1)
                processed_tweet.append((pair[0], pair[1]))
            processed_tweets.append(processed_tweet)
        return processed_tweets

    def extract_relationships(self):
        processed_tweets = self.preprocess_tweets()
        grammar = r"""
            ENTITY: {<\^|@|\#>+}
            NP: {<D|Z>?<A>*<N|ENTITY>+}
            VP: {<V>+}
            REL: {<NP><VP><P>*<NP>}
                 {<NP>}
        """
        cp = nltk.RegexpParser(grammar)
        for tweet in processed_tweets:
            tree = cp.parse(tweet)
            self.get_nodes(tree)
        return

    def get_nodes(self, parent):
        for node in parent:
            if type(node) is nltk.Tree:
                if node.label() == "REL":
                    self.process_relationship(node)
                else:
                    self.get_nodes(node)

    def process_relationship(self, parent):
        #print(parent)
        verbEntity = None
        prevEntity = None
        entity = None
        for node in parent:
            if type(node) is nltk.Tree:
                if node.label() == "NP":
                    prevEntity = entity
                    entity = self.process_noun_phrase(node)
                    if verbEntity != None and prevEntity != None and entity != None:
                        if prevEntity.startswith("BN:") != True:
                            if entity.startswith("BN:") == True:
                                entity = entity[3:]
                            self.add_to_triple_store((prevEntity, verbEntity, entity))
                            self.triples.append(prevEntity + " " + verbEntity + " " + entity)
                elif node.label() == "VP":
                    if entity == None:
                        time.sleep(0.001) # TODO handle when entity is not present
                        #print(parent)
                    else:
                        verbEntity = self.process_verb_phrase(node)
    
    def process_verb_phrase(self, parent):
        entity = ""
        for leaf in parent.leaves():
            if leaf[1] == "V":
                entity = leaf[0]
        #conjugatedVerb = conjugate(entity.strip())
        #return self.sparqlEndpoint.getWordnetURI(conjugatedVerb)
        return entity.strip().lower()

    def process_noun_phrase(self, parent):
        adjectives = []
        entityUri = None
        possessiveUri = None
        is_noun = False
        noun = ""
        is_possessive = False
        for node in parent:
            if type(node) is nltk.Tree:
                if node.label() == "ENTITY":
                    entity = ""
                    for leaf in node.leaves():
                        entity += leaf[0] + " "
                    entity = entity.strip()
                    entityUri = self.get_entity_uri(entity)
                    if len(adjectives) > 0 and entityUri != None:
                        for adjective in adjectives:
                            self.add_to_triple_store((entityUri, self.uriForIs, adjective))
                            self.triples.append(entityUri + " " +self.uriForIs +" " + adjective.lower())
                        adjectives = []
                        if is_possessive == True:
                            self.add_to_triple_store((entityUri, self.uriForIs, adjective))
                            self.triples.append(possessiveUri + " has " + entityUri)
            else:
                if node[1] == "Z":
                    entity = node[0].rstrip("'s")
                    possessiveUri = self.get_entity_uri(entity)
                    #if len(adjectives) > 0 and entityUri != None:
                    #    for adjective in adjectives:
                    #        self.add_to_triple_store((entityUri, self.uriForIs, adjective))
                    #        self.triples.append(entityUri + " " +self.uriForIs + " " + adjective.lower())
                    is_possessive = True
                    #    adjectives = []
                elif node[1] == "A":
                    adjectives.append(node[0])
                elif node[1] == "N" : 
                    noun += " " + node[0]
                    is_noun = True
        if is_noun == True:
            #label = ""
            #for leaf in parent.leaves():
            #    label += leaf[0] + " "
            #label = label.strip().lower()
            if entityUri == None or possessiveUri == None:
                return "BN:" + noun.strip().lower()
            else:
                if entityUri != None:
                    return entityUri
                else:
                    return possessiveUri
        else:
            if entityUri != None:
                return entityUri
            else:
                return possessiveUri

    def get_entity_uri(self, name):
        if name.lower() in self.entities:
            return self.entities[name.lower()]
        else:
            return None

def tag_tweets(file_name):
    output = subprocess.Popen(["ark-tweet-nlp-0.3.2/" + "runTagger.sh", file_name], 
        stdout = subprocess.PIPE).communicate()
    decoded_output = output[0].decode('utf-8')
    result = decoded_output.split("\n")
    result = result[:-1]
    tagged_tweets = []
    for line in result:
        parts = line.split('\t')
        tokens = parts[0].split()
        tags = parts[1].split()
        pairs = ["%s/%s" % (tok, tag) for tok,tag in zip(tokens,tags)]
        tagged_tweets.append(pairs)
    return tagged_tweets

if __name__ == "__main__":
    url_clusters={}
    url_clusters['http://en.wikipedia.org/wiki/Masarat_Alam_Bhat']=['masarat alam', 'masarat alam', 'masarat alam\xe2\x80\x99s', 'masarat', 'masarat alam #rearrestmasarat', 'masarat alam', 'masarat alam saahab', 'masara', 'masarat alam nda govt', 'alam', 'masarat alam bhat', 'masarat alam', 'masarat alam', 'masarat alam arstng', 'masarat alam saab', 'lumpen masarat alam', 'masarat', 'superman masarat alam', 'masarat #alam', 'masarat sah']
    url_clusters['http://en.wikipedia.org/wiki/Kashmir']=['kashmiri', 'kashmir', 'kashmiri pandits', 'kashmir', 'kashmiri pandit', 'kasmiri', 'kashmir occupied india', 'kashmir', "kashmir's\xe2\x80\xa6"]
    url_clusters['http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani']=['geelani', 'syed ali geelani', 'syed ali #geelani', 'syed ali shah geelani', 'geelani', 'mr  geelani', 'syed geelani']
    
    entities = {}
    for entity in url_clusters:
        listData = url_clusters[entity]
        for item in listData:
            entities[item] = entity

    tweets = tag_tweets("tweets.txt")
    triple_store = rdflib.Graph()
    relation_extractor = Relation_Extractor(tweets, entities, triple_store)
    relation_extractor.extract_relationships()

    triplesCountMap = {}
    for triple in relation_extractor.triples:
        if triple not in triplesCountMap:
            triplesCountMap[triple] = 0
        triplesCountMap[triple] += 1
    sortedTriples = sorted(triplesCountMap.items(), key=operator.itemgetter(1), reverse=True)
    for triple in sortedTriples:
        print(triple)
