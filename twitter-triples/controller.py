import sys, operator, rdflib

from pattern.en import conjugate

from tweet_extractor import Tweet_extractor
from extract_entities import Extract_entities
from map_url import Wiki_Mapper
from sparql_endpoint_interface import SPARQL_Endpoint_Interface
from extract_triples import Relation_Extractor
from generate_sentence import Sentence_generator


import rdflib

if __name__ == "__main__":
    # 1. Get tweets
    if sys.argv[1] == None:
        print("Error: Please provide the filename to twitter's API keys")
    query = raw_input("Please enter the query: ")
    extractor=Tweet_extractor(sys.argv[1])
    tweets=extractor.get_tweets(query)
    extractor.write_to_file()

    # 2. Extract entities
    entityExtractor = Extract_entities()
    entityExtractor.tag_tweets("tweets.txt")
    proper_nouns = entityExtractor.get_proper_nouns()
    common_nouns = entityExtractor.get_common_nouns()
    proper_noun_entities = entityExtractor.get_named_entity_clusters([x[0] for x in proper_nouns],False)
    common_noun_entities = entityExtractor.get_named_entity_clusters([x[0] for x in common_nouns],True)

    # 3. Map urls
    wiki_mapper=Wiki_Mapper(proper_noun_entities,common_noun_entities)
    entity_url=wiki_mapper.map_urls()

    sparql_endpoint = SPARQL_Endpoint_Interface()
    entities = {}
    for entity in entity_url:
        for keyword in entity[0]:
            if keyword not in entities and entity[1]!= None:
                entities[keyword] = sparql_endpoint.getDBPediaURI(entity[1])

    # 4.replace key word with url?

    # 5. get relationships between entities
    triple_store = rdflib.Graph()
    relationship_extractor = Relation_Extractor(entityExtractor.tagged_tweets, entities, triple_store)
    relationship_extractor.extract_relationships()

    #print(relationship_extractor.triples)
    triplesCountMap = {}
    for triple in relationship_extractor.triples:
        if triple not in triplesCountMap:
            triplesCountMap[triple] = 0
            parts = triple.split(" ", 2)
            subject = rdflib.URIRef(parts[0])
            conjugatedForm = conjugate(parts[1])
            verbURI = sparql_endpoint.getWordnetURI(conjugatedForm)
            predicate = rdflib.URIRef(verbURI)
            if " " in parts[2]:
                obj = rdflib.Literal(parts[2])
            else:
                conjugatedForm = conjugate(parts[2])
                uri = sparql_endpoint.getWordnetURI(conjugatedForm)
                if uri == None:
                    obj = rdflib.Literal(parts[2])
                else:
                    obj = rdflib.URIRef(uri)
            triple_store.add((subject, predicate, obj))
        triplesCountMap[triple] += 1
    sortedTriples = sorted(triplesCountMap.items(), key=operator.itemgetter(1), reverse=True)

    # 6. generate summary
    sentence_generator=Sentence_generator(sortedTriples)
    summary=sentence_generator.get_sentences()

    triple_store.serialize(destination='triples.ttl', format='turtle')

