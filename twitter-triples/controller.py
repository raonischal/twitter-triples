import sys

from extract_entities import Extract_entities
from map_url import Wiki_Mapper
from sparql_endpoint_interface import SPARQL_Endpoint_Interface

if __name__ == "__main__":
    # TODO: Invoke tweet_extractor here
    entityExtractor = Extract_entities()
    entityExtractor.tag_tweets("tweets.txt")
    proper_nouns = entityExtractor.get_proper_nouns()
    common_nouns = entityExtractor.get_common_nouns()
    proper_noun_entities = entityExtractor.get_named_entity_clusters(proper_nouns,True)
    common_noun_entities = entityExtractor.get_named_entity_clusters(common_nouns,False)
    wiki_mapper=Wiki_Mapper(proper_noun_entities,common_noun_entities)
    entity_url=wiki_mapper.map_urls()
    sparql_endpoint_interface = SPARQL_Endpoint_Interface()
    dbPediaURIs = {}
    print("\n\n DBPedia URIs: ")
    for keyword in entity_url:
        if entity_url[keyword] != None:
            uri = sparql_endpoint_interface.getDBPediaURI(entity_url[keyword])
            dbPediaURIs[keyword] = uri
            print(keyword + ": " + uri)
