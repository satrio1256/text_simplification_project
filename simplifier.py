import FileManager as fm
import POSTagger as pt
import LexicalSimplifier as ls
import SyntacticSimplifier as ss
import os
import time
import nltk
from sensegram import sensegram
import argparse

# Prepare NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

path_rule_syntactic = 'dataset/syntactic_rules/rule_syntactic.tsv'
path_full_dataset = 'dataset/full'
path_postag_dataset = 'dataset/POSTag/Indonesian_Manually_Tagged_Corpus_ID.tsv'
path_tag_model = 'model/all_indo_man_tag_corpus_model.crf.tagger'
path_word_frequency_tsv = 'model/word_frequency/word_freq_new.tsv'
sense_vectors_fpath = 'sensegram/model/idwiki-latest.n200.clusters.minsize5-1000-sum-score-20.sense_vectors'
word_vectors_fpath = 'sensegram/model/idwiki-latest.cbow1-size300-window5-iter5-mincount10-bigramsFalse.word_vectors'

# Variables
freq_min_threshold = 750       # Dilihat distribusi frekuensi katanya? Plotter confusing :(

def trainLexical():
    files = fm.get_dataset(path_full_dataset)
    i = 0
    time_start = time.perf_counter()
    for f in files:
        word_freq_temp = {}
        if os.path.isfile(path_word_frequency_tsv):
            with open(path_word_frequency_tsv) as csv_file:
                for row in csv_file:
                    (key, val) = row.split()
                    word_freq_temp[str(key)] = int(val)
        i += 1
        print("Processing", i, 'of', len(files), 'dataset')
        word_freq_temp = ls.count_word_frequency(fm.read_raw_dataset(file=f), word_freq_temp)
        fm.save_word_freq(word_freq_temp)
    time_stop = time.perf_counter()
    print("Counting Complete, time elapsed", time_stop-time_start, 'seconds')

def loadSyntactic():
    print("Loading Syntactic Rules")
    return ss.load_rule(path_rule_syntactic)

def loadSense():
    # Load sense_vector
    print("Loading Sense Vector")
    return sensegram.SenseGram.load_word2vec_format(sense_vectors_fpath, binary=False)

def loadWord2Vec():
    # Load word_vector
    print("Loading Word2Vec")
    return sensegram.SenseGram.load_word2vec_format(word_vectors_fpath, binary=False, unicode_errors='ignore')

def calculate(sv, wv, sentences = ""):
    lexical_simplified = ls.lexical_simplify(sv_model=sv,
                                        wv_model=wv,
                                        word_freq_model=path_word_frequency_tsv,
                                        pos_tag_model=path_tag_model,
                                        raw_sentences=sentences,
                                        min_threshold=freq_min_threshold)

    rules = loadSyntactic()
    syntactic_simplified = ss.syntactic_simplify(lexical_simplified, path_tag_model, rules)
    print()
    print("=============== RESULT ===============")
    print()
    print("Old:", sentences)
    print()
    print("Lexical Simplified:", lexical_simplified)
    print()
    print("Syntactic Simplified:", syntactic_simplified)
    print()

def trainPOSTag():
    pt.train_pos_tag(path_postag_dataset, path_tag_model)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Text Simplifier")
    parser.add_argument("--text", help="String yang akan disederhanakan", type=str)
    args = parser.parse_args()
    if args.text == "":
        print("Text cannot be empty")
    else:
        sv = loadSense()
        wv = loadWord2Vec()
        calculate(sv, wv, args.text)