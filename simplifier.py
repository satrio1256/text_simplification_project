import FileManager as fm
import POSTagger as pt
import LexicalSimplifier as ls
import SyntacticSimplifier as ss
import os
import time
from sensegram import sensegram

path_full_dataset = 'dataset/full'
path_postag_dataset = 'dataset/POSTag/Indonesian_Manually_Tagged_Corpus_ID.tsv'
path_tag_model = 'model/all_indo_man_tag_corpus_model.crf.tagger'
path_word_frequency_tsv = 'model/word_frequency/word_freq.tsv.bak'
sense_vectors_fpath = 'sensegram/model/idwiki-latest.n200.clusters.minsize5-1000-sum-score-20.sense_vectors'
word_vectors_fpath = 'sensegram/model/idwiki-latest.cbow1-size300-window5-iter5-mincount10-bigramsFalse.word_vectors'

# Variables
freq_min_threshold = 1500       # Dilihat distribusi frekuensi katanya? Plotter confusing :(

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

def loadSense():
    # Load sense_vector
    print("Loading Sense Vector")
    return sensegram.SenseGram.load_word2vec_format(sense_vectors_fpath, binary=False)

def loadWord2Vec():
    # Load word_vector
    print("Loading Word2Vec")
    return sensegram.SenseGram.load_word2vec_format(word_vectors_fpath, binary=False, unicode_errors='ignore')

def calculate(sv, wv):
    # Word to process
    sentences = "Kandang adalah struktur atau bangunan tempat hewan ternak dipelihara. Kandang seringkali dikategorikan menurut jumlah hewan yang menempatinya; ada yang hanya berupa satu bangunan satu hewan, satu bangunan banyak hewan namun terpisah oleh sekat, dan satu bangunan diisi banyak hewan tanpa sekat."

    new_sentences = ls.lexical_simplify(sv_model=sv,
                                        wv_model=wv,
                                        word_freq_model=path_word_frequency_tsv,
                                        raw_sentences=sentences,
                                        min_threshold=freq_min_threshold)

    new_sentences = ss.syntactic_simplify()

    print(new_sentences)


def trainPOSTag():
    pt.train_pos_tag(path_postag_dataset, path_tag_model)


if __name__ == "__main__":
    exit(0)
    # Train Word Frequency
    # trainLexical()

    # Load Sense Vectors
    # loadSense()

    # Load Word2Vec
    # loadWord2Vec()

    # Run to count word frequency
    # trainLexical()

    # Train POS Tagger
    # trainPOSTag()

    # Word2Vec Get Similar
    # word = "asam"
    # print(wv.similar_by_word(word, 10))

    # Sensegram
    # words = ['asam']
    # context = "Asam deoksiribonukleat, lebih dikenal dengan singkatan DNA (bahasa Inggris: 'deoxyribonucleic acid'), adalah sejenis biomolekul yang menyimpan dan menyandi instruksi-instruksi genetika setiap organisme dan banyak jenis virus. Instruksi-instruksi genetika ini berperan penting dalam pertumbuhan, perkembangan, dan fungsi organisme dan virus. DNA merupakan asam nukleat; bersamaan dengan protein dan karbohidrat, asam nukleat adalah makromolekul esensial bagi seluruh makhluk hidup yang diketahui. Kebanyakan molekul DNA terdiri dari dua unting biopolimer yang berpilin satu sama lainnya membentuk heliks ganda. Dua unting DNA ini dikenal sebagai polinukleotida karena keduanya terdiri dari satuan-satuan molekul yang disebut nukleotida. Tiap-tiap nukleotida terdiri atas salah satu jenis basa nitrogen (guanina (G), adenina (A), timina (T), atau sitosina (C)), gula monosakarida yang disebut deoksiribosa, dan gugus fosfat. Nukleotida-nukelotida ini kemudian tersambung dalam satu rantai ikatan kovalen antara gula satu nukleotida dengan fosfat nukelotida lainnya. Hasilnya adalah rantai punggung gula-fosfat yang berselang-seling. Menurut kaidah pasangan basa (A dengan T dan C dengan G), ikatan hidrogen mengikat basa-basa dari kedua unting polinukleotida membentuk DNA unting ganda"

    # print("Probabilities of the senses:\n{}\n\n".format(sv.get_senses(word, ignore_case=True)))
    #
    # for sense_id, prob in sv.get_senses(word, ignore_case=True):
    #     print(sense_id)
    #     print("=" * 20)
    #     for rsense_id, sim in sv.wv.most_similar(sense_id):
    #         print("{} {:f}".format(rsense_id, sim))
    #     print("\n")
    #
    # # Disambiguate a word in a context
    # wsd_model = WSD(sv, wv, window=5, max_context_words=3, method='sim', ignore_case=True)
    # print(wsd_model.disambiguate(context, word))

    #
    # pt.train_pos_tag(path_postag_dataset, path_tag_model)
    # print(pt.tag_strings(path_tag_model, tokenized_string=['']))
    # XXX
    # parser = argparse.ArgumentParser("Text Simplifier")
    # parser.add_argument("--txt", help="String yang akan disederhanakan", type=str)
    # parser.add_argument("--dir", help="Directory file yang ingin disederhanakan", type=str)
    # args = parser.parse_args()
    # print(args)