import sys, subprocess, operator, time

import rdflib

import nltk

class Relation_Extractor:
    def __init__(self, tweets, entities, triple_store):
        self.tweets = tweets
        self.entities = entities
        self.blank_nodes_map = {}
        self.triple_store = triple_store
        self.triples = []

    def add_to_triple_store(self, tup, isLiteral=True):
        subject = rdflib.URIRef(tup[0])
        predicate = rdflib.URIRef(tup[1])
        if isLiteral == True:
            obj = rdflib.Literal(tup[2])
        else:
            obj = rdflib.URIRef(tup[2])
        self.triple_store.add((subject, predicate, obj))
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
            ENTITY: {<\^>+}
            NP: {<D|Z>?<A>*<N|ENTITY>+}
            VP: {<V>+<P>?}
            REL: {<NP><VP><NP>}
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
        verbEntity = None
        prevEntity = None
        entity = None
        for node in parent:
            if type(node) is nltk.Tree:
                if node.label() == "NP":
                    prevEntity = entity
                    entity = self.process_noun_phrase(node)
                    if verbEntity != None and prevEntity != None and entity != None:
                        self.add_to_triple_store((prevEntity, verbEntity, entity))
                        self.triples.append("<"+prevEntity + "> <" + verbEntity + "> <" + entity + "> . ")
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
                entity += leaf[0] + " "
        return entity.strip().replace(" ", "_")

    def process_noun_phrase(self, parent):
        adjectives = []
        entityUri = None
        composite = False
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
                            self.add_to_triple_store((entityUri, "http://example.com/is", adjective))
                            self.triples.append( "<" + entityUri + "> " + "<http://example.com/is>" + " \"" + adjective + "\" . ")
                        adjectives = []
            else:
                if node[1] == "Z":
                    entity = node[0].rstrip("'s")
                    entityUri = self.get_entity_uri(entity)
                    if len(adjectives) > 0 and entityUri != None:
                        for adjective in adjectives:
                            self.add_to_triple_store((entityUri, "http://example.com/is", adjective))
                            self.triples.append("<"+entityUri + "> " + "<http://example.com/is>" + " \"" + adjective + "\" . ")
                        adjectives = []
                elif node[1] == "A":
                    adjectives.append(node[0])
                elif node[1] == "N" or node[1] == "D" : 
                    composite = True
        if composite == True:
            label = ""
            for leaf in parent.leaves():
                label += leaf[0] + " "
            label = label.strip().lower()
            if label not in self.blank_nodes_map and entityUri != None:
                self.blank_nodes_map[label] = rdflib.BNode()
                self.add_to_triple_store((self.blank_nodes_map[label], "rdf:about", entityUri), False)
                self.triples.append("<http://dummy/" + label.replace(" ", "_") + "> " + "rdf:about" + " <" + entityUri + "> . ")
                self.add_to_triple_store((self.blank_nodes_map[label], "rdfs:label", label))
                self.triples.append("<http://dummy/" + label.replace(" ", "_") + "> " + "rdfs:label" + " \"" + label + "\" . ")
            return "http://dummy/" + label.replace(" ", "_") + ""
        else:
            return entityUri

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

    #entities={'pakistan': u'http://dbpedia.org/resource/Pakistan', 'hurriatt': u'http://dbpedia.org/resource/All_Parties_Hurriyat_Conference', 'pakistanzindabad #srinagarispakistan': u'http://dbpedia.org/resource/Srinagar', 'masarat al': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'kashmiri muslims': u'http://dbpedia.org/resource/Kashmir', 'masarat alam\xe2\x80\x99s': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'india': u'http://dbpedia.org/resource/India', 'masarat alam bhakt': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'masarat alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'bjp': u'http://dbpedia.org/resource/BJP_ST_Morcha', 'ind': u'http://dbpedia.org/resource/India', 'modi pakistan': u'http://dbpedia.org/resource/Microsoft_Office_Document_Imaging', 'narendra modi\xe2\x80\x99s': u'http://dbpedia.org/resource/Narendra_Modi', 'anti indians': u'http://dbpedia.org/resource/India', 'jk congress': u'http://dbpedia.org/resource/United_States_Congress', 'indian express': u'http://dbpedia.org/resource/India', 'bing pakistan': u'http://dbpedia.org/resource/Pakistan', 'indians': u'http://dbpedia.org/resource/India', 'masarat #alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'modi #pakistan': u'http://dbpedia.org/resource/Microsoft_Office_Document_Imaging', 'masarat alam lioks': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'masarat alam saahab': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'india\xe2\x80\x99s': u'http://dbpedia.org/resource/India', 'indian': u'http://dbpedia.org/resource/India', 'hurriyat': u'http://dbpedia.org/resource/All_Parties_Hurriyat_Conference', 'anti india': u'http://dbpedia.org/resource/India', 'balochistan': u'http://dbpedia.org/resource/Balochistan,_Pakistan', 'srinagar': u'http://dbpedia.org/resource/Srinagar', 'singh': u'http://dbpedia.org/resource/Digvijaya_Singh', 'pakistani': u'http://dbpedia.org/resource/Pakistan', 'ji masarat alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'narendra modi\xe2\x80\x99s kashmir': u'http://dbpedia.org/resource/Narendra_Modi', 'kashmiris': u'http://dbpedia.org/resource/Kashmir', 'bjps': u'http://dbpedia.org/resource/BJP_ST_Morcha', 'paki': u'http://dbpedia.org/resource/Pakistan', 'congress': u'http://dbpedia.org/resource/United_States_Congress', 'narendra modis kashmir': u'http://dbpedia.org/resource/Narendra_Modi', 'baluchistan': u'http://dbpedia.org/resource/Balochistan,_Pakistan', 'digvijaya singh': u'http://dbpedia.org/resource/Digvijaya_Singh', 'firstpost modi pakistan': u'http://dbpedia.org/resource/Microsoft_Office_Document_Imaging', 'masarat alam #jodhpur': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'pm modi #pakistan': u'http://dbpedia.org/resource/Pakistan', 'firstpost': u'http://dbpedia.org/resource/The_First_Post', 'masarat alam etc': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'bjp pdp': u'http://dbpedia.org/resource/BJP_ST_Morcha', 'masarat alam bhat': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'pak': u'http://dbpedia.org/resource/Pakistan', 'kashmir\xe2\x80\x99s': u'http://dbpedia.org/resource/Kashmir', 'kashmiri': u'http://dbpedia.org/resource/Kashmir', 'azadi': u'http://dbpedia.org/resource/Azadi_Tower', 'pro masarat alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'say modi pakistan': u'http://dbpedia.org/resource/Pakistan', 'firstpostpm mod': u'http://dbpedia.org/resource/The_First_Post', 'modis pak': u'http://dbpedia.org/resource/Microsoft_Office_Document_Imaging', 'modi\xe2\x80\x99s pakistan': u'http://dbpedia.org/resource/Pakistan', 'pm modi pakistan': u'http://dbpedia.org/resource/Pakistan', 'kashmir': u'http://dbpedia.org/resource/Kashmir', 'pakistanis': u'http://dbpedia.org/resource/Pakistan', 'whymasarat alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 's': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'kashmirstreet': u'http://dbpedia.org/resource/Kashmir', 'pakis': u'http://dbpedia.org/resource/Pakistan', 'pro pakistan': u'http://dbpedia.org/resource/Pakistan', 'pro  #pakistan': u'http://dbpedia.org/resource/Pakistan', 'modi': u'http://dbpedia.org/resource/Microsoft_Office_Document_Imaging', 'masarat alam islamic': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'pm\xe2\x80\x99s modi\xe2\x80\x99s pakistan': u'http://dbpedia.org/resource/Pakistan', 'narendra modi': u'http://dbpedia.org/resource/Narendra_Modi', 'digvijaysingh': u'http://dbpedia.org/resource/Digvijaya_Singh', 'lumpen masarat alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat', 'masarat  alam': u'http://dbpedia.org/resource/Masarat_Alam_Bhat'}

    url_clusters={}
    url_clusters['http://en.wikipedia.org/wiki/Masarat_Alam_Bhat']=['masarat alam', 'masarat alam', 'masarat alam\xe2\x80\x99s', 'masarat', 'masarat alam #rearrestmasarat', 'masarat alam', 'masarat alam saahab', 'masara', 'masarat alam nda govt', 'alam', 'masarat alam bhat', 'masarat alam', 'masarat alam', 'masarat alam arstng', 'masarat alam saab', 'lumpen masarat alam', 'masarat', 'superman masarat alam', 'masarat #alam', 'masarat sah']
    url_clusters['http://en.wikipedia.org/wiki/Kashmir']=['kashmiri', 'kashmir', 'kashmiri pandits', 'kashmir', 'kashmiri pandit', 'kasmiri', 'kashmir occupied india', 'kashmir', "kashmir's\xe2\x80\xa6"]
    url_clusters['http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani']=['geelani', 'syed ali geelani', 'syed ali #geelani', 'syed ali shah geelani', 'geelani', 'mr  geelani', 'syed geelani']
    
    entities = {}
    for entity in url_clusters:
        listData = url_clusters[entity]
        for item in listData:
            entities[item] = entity

    tweets = tag_tweets("tweets5.txt")
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
