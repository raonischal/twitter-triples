import sys, rdflib
from SPARQLWrapper import SPARQLWrapper2

class SPARQL_Endpoint_Interface:
    def __init__(self):
        self.dbPediaEndpoint = "http://live.dbpedia.org/sparql"
        self.wordnetEndpoint = rdflib.Graph()
        self.wordnetEndpoint.parse("wordnet-wordtype.rdf", format="turtle")

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

    def getWordnetURI(self, word):
        lexicalFormURI = rdflib.URIRef("http://www.w3.org/2006/03/wn/wn20/schema/lexicalForm")
        wordLiteral = rdflib.Literal(word)
        for sub, pred, obj in self.wordnetEndpoint.triples((None, lexicalFormURI, wordLiteral)):
            return sub
        return None

if __name__ == "__main__":
    interface = SPARQL_Endpoint_Interface()
    #interface.getDBPediaURI("http://en.wikipedia.org/wiki/Ronnie_Price")
    print(interface.getWordnetURI("arrest"))
    print(interface.getWordnetURI("remand"))
    print(interface.getWordnetURI("is"))
