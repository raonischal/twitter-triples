def filter_verb(word):
    word=word.replace('>','')
    word=word.replace('<','')
    words=word.split('/')
    name=words[-1].split('_')
    name=" ".join(name)
    return name

def filter_noun(word):
    word=word.replace('"','')
    word=word.replace('>','')
    word=word.replace('<','')
    words=word.split('/')
    name=words[-1].split('_')
    name=" ".join(name)
    return name

class Sentence_generator:
    def __init__(self, tuples):
        self.tuples=tuples
        
    def get_sentences(self):
        sentences=[]
        for triple_touple in self.tuples:
            triple=triple_touple[0]
            words=triple.split(" ", 2)  
            subject_name=filter_noun(words[0]).title()
            object_name=filter_noun(words[2])    
            #verb_past=en.verb.present(filter_verb(words[1]))
            verb_past=filter_verb(words[1])
            sentences.append((str(subject_name)+" "+str(verb_past)+" "+str(object_name)+"."))
        sentences=set(sentences)
        sentences=" ".join(sentences)
        print(sentences)
        return sentences
            
        
        

if __name__=="__main__":
    tuples=[(u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <charged> <http://dummy/sedition> . ', 105), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <http://example.com/is> "separatist" . ', 104), (u'<http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani> <http://example.com/is> "defiant" . ', 74), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <http://example.com/is> "Separatist" . ', 68), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <remanded> <http://dummy/7-day_police_custody> . ', 66), (u'<http://dummy/separatist_leader_masarat_alam> <remanded> <http://dummy/7-day_police_custody> . ', 41), (u'<http://dummy/mufti_mohammad> <Sayeed> <http://dummy/government> . ', 34), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <sent> <http://dummy/seven-day_police_custody> . ', 31), (u'<http://dummy/anger> <rises> <http://dummy/the_valley> . ', 22), (u'<http://dummy/police> <add> <http://dummy/sedition_charge> . ', 15), (u'<http://dummy/congress_leader> <believes> <http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> . ', 14), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <will_go> <http://dummy/jail> . ', 14), (u'<http://dummy/mobster_masarat_alam> <charged> <http://dummy/sedition> . ', 14), (u'<http://dummy/the_45-year-old_hardliner> <was_arrested> <http://dummy/his_home> . ', 13), (u'<http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani> <calls> <http://dummy/shutdown> . ', 10), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <http://example.com/is> "terrorist" . ', 9), (u'<http://dummy/clashes> <erupt> <http://dummy/protesters> . ', 7), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <is> <http://dummy/a_guest> . ', 7), (u'<http://dummy/self> <proclaimed> <http://dummy/authority> . ', 6), (u'<http://dummy/mufti> <can_bring> <http://en.wikipedia.org/wiki/Kashmir> . ', 5), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <arrested> <http://dummy/sedition_charge> . ', 4), (u'<http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani> <calls> <http://dummy/bandh> . ', 4), (u'<http://dummy/separatist_leader_masarat_alam> <sent> <http://dummy/seven-day_police_custody> . ', 3), (u'<http://dummy/power> <brings> <http://dummy/violence> . ', 3), (u'<http://en.wikipedia.org/wiki/Kashmir> <http://example.com/is> "Greater" . ', 3), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <raising> <http://dummy/pro_pak_slogan> . ', 2), (u'<http://en.wikipedia.org/wiki/Syed_Ali_Shah_Geelani> <put> <http://dummy/house_arrest> . ', 2), (u'<http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> <may_be> <http://dummy/part> . ', 2), (u'<http://dummy/every_kashmiri> <is> <http://en.wikipedia.org/wiki/Masarat_Alam_Bhat> . ', 2), (u"<http://dummy/#propak_slogans> <wasn't> <http://dummy/sensational_enough> . ", 2)]

    generator = Sentence_generator(tuples)
    generator.get_sentences()
