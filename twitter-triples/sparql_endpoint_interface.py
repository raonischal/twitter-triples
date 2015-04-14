import sys
from SPARQLWrapper import SPARQLWrapper2

class SPARQL_Endpoint_Interface:
    def __init__(self):
        self.dbPediaEndpoint = "http://live.dbpedia.org/sparql"
        #self.wordnetEndpoint = ""

    def getDBPediaURI(self, wikipediaURL):
        queryString = """select distinct ?uri WHERE {
            ?uri foaf:isPrimaryTopicOf <""" + wikipediaURL + """> .
        }"""
        sparql = SPARQLWrapper2(self.dbPediaEndpoint)
        sparql.setQuery(queryString)
        ret = sparql.query()
        result = ""
        for binding in ret.bindings :
            result = binding[u"uri"].value
        return result

if __name__ == "__main__":
    interface = SPARQL_Endpoint_Interface()
    interface.getDBPediaURI("http://en.wikipedia.org/wiki/Ronnie_Price")
