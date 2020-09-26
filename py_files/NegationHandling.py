from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

neg_words = ["no", "not", "n't", "wont", "never", "none", "nobody", "nothing", "neither", "nor", "nowhere", "without"]# "rather",
class AntonymReplacer(object):
    def replace(self, word):
        antonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.append(antonym.name())
        if len(antonyms) >= 1:
            return antonyms[0]
        else :
            return None
        
    def negreplacer(self, string):
        i=0
        sent = word_tokenize(string)
        len_sent = len(sent)
        words = ''
        ant1 = ''
        ant = ''
        while i < len_sent :
            word = sent[i]
            if word in neg_words and i+1 < len_sent :
                ant = self.replace(sent[i+1])
                if i+2 < len_sent :
                    ant1 = self.replace(sent[i+2])
#                   print("woo")
                if ant1:
                    words += ant1+ ' '
                    i += 3
                    continue
                elif ant :
                    words += ant + ' '
                    i += 2
                    continue
            words += word + ' '
            i += 1
        return words
            

class WordReplacer(object):
    def __init__(self, word_map):
        self.word_map = word_map
        
    def replace(self, word):
        return self.word_map.get(word, word)
                    
    
rep = AntonymReplacer()

# print(word_tokenize(rep.negreplacer("not bad and Wonderful.")))
# print(word_tokenize("He nobody"))