#
#    accepts a list of keywords
#    reduces it to a list of unique keywords
#
import jellyfish

class String_Matcher:
    entities=[]
    unique_entities=[]    

    def __init__(self):
        self.entities=['carter','carters','CARTAH','CARTAR','crater','cater'] 
        #self.entities=['miliman','milliman']       
       

    def get_unique_entities(self):
        for entity in self.entities:
            entity_found=False
            for word in self.unique_entities:
                #if jellyfish.metaphone(word) == jellyfish.metaphone(entity):
                #if (jellyfish.jaro_distance(word)-jellyfish.jaro_distance(entity) >0.98) or (jellyfish.jaro_distance(word)-jellyfish.jaro_distance(entity) < -0.98)
                if jellyfish.soundex(word) == jellyfish.soundex(entity):
                    entity_found=True
                    break
            if entity_found==False:self.unique_entities.append(entity)

        return self.unique_entities


if __name__=="__main__":
    matcher=String_Matcher()
    unique_entities=matcher.get_unique_entities()
    for entity in unique_entities:
        print(entity)

    
