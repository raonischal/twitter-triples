import sys

from tweet_extractor import Tweet_extractor
from extract_entities import Extract_entities
from map_url import Wiki_Mapper
from sparql_endpoint_interface import SPARQL_Endpoint_Interface

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
    proper_noun_entities = entityExtractor.get_named_entity_clusters(proper_nouns,True)
    common_noun_entities = entityExtractor.get_named_entity_clusters(common_nouns,False)

    # 3. Map urls
    wiki_mapper=Wiki_Mapper(proper_entities,common_entities)
    entity_url=wiki_mapper.map_urls()
    
    # 4.replace key word with url?

    # 5. get relationships between entities

