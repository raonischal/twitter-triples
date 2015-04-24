import sys

from tweet_extractor import Tweet_extractor
from extract_entities import Extract_entities
from map_url import Wiki_Mapper
from sparql_endpoint_interface import SPARQL_Endpoint_Interface
from extract_triples import Relation_Extractor
from generate_sentence import Sentence_generator


import rdflib

if __name__ == "__main__":
    # 1. Get tweets
    #extractor=Tweet_extractor()
    #tweets=extractor.get_tweets()
    #extractor.write_to_file()

    # 2. Extract entities
    entityExtractor = Extract_entities()
    entityExtractor.tag_tweets("tweets.txt")
    proper_nouns = entityExtractor.get_proper_nouns()
    common_nouns = entityExtractor.get_common_nouns()
    proper_noun_entities = entityExtractor.get_named_entity_clusters([x[0] for x in proper_nouns],False)
    common_noun_entities = entityExtractor.get_named_entity_clusters([x[0] for x in common_nouns],True)

    # 3. Map urls
    wiki_mapper=Wiki_Mapper(proper_noun_entities,common_noun_entities)
    entities=wiki_mapper.map_urls()

    # 4.replace key word with url?

    # 5. get relationships between entities
    triple_store = rdflib.Graph()
    relationship_extractor = Relation_Extractor(entityExtractor.tagged_tweets, entities, triple_store)
    relationship_extractor.extract_relationships()

    triplesCountMap = {}
    for triple in relationship_extractor.triples:
        if triple not in triplesCountMap:
            triplesCountMap[triple] = 0
        triplesCountMap[triple] += 1
    sortedTriples = sorted(triplesCountMap.items(), key=operator.itemgetter(1), reverse=True)
    for triple in sortedTriples:
        print(triple)

    # 6. generate summary
    sentence_generator=Sentence_generator(sortedTriples)
    summary=sentence_generator.get_sentences()

