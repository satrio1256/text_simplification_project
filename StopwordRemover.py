from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def remove_stopword(strings):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    return stopword.remove(str.lower(strings))

def start_stemming(strings):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(str.lower(strings))