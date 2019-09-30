import FileManager as fm
import POSTagger as pt
import LexicalSimplifier as ls
import SyntacticSimplifier as ss
import os
import time
import nltk
from sensegram import sensegram

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

def calculate(sv, wv):
    # Word to process
    # LEXICAL ONLY SIMPLIFICATION
    # sentences = "Kandang adalah struktur atau bangunan tempat hewan ternak dipelihara. Kandang seringkali dikategorikan menurut jumlah hewan yang menempatinya; ada yang hanya berupa satu bangunan satu hewan, satu bangunan banyak hewan namun terpisah oleh sekat, dan satu bangunan diisi banyak hewan tanpa sekat."

    # SYNTACTIC ONLY SIMPLIFICATION
    sentences = "Rani anak orang kaya raya tetapi dia tidak sombong kepada orang lain. Heru menyeberang dengan sangat hati – hati di jalan raya lalu memesan taksi secara online."

    # sentences = "Setelah berbincang-bincang dan membujuk kakaknya, pada akhirnya Hendra sang kakak dengan ikhlas untuk memberikan uang celengannya saat itu kepada adik tercinta."

    # LEXICAL - SYNTACTIC SIMPLIFICATION
    sentences = "Pesta tersebut akhirnya ricuh dan Angel pun lari dan mengalami kecelakaan. Kecelakaan tersebut menyebabkan tak ada satu orang pun yang bisa menyelamatkan dirinya selain Hendra."

    # LONG SENTENCES
    # sentences = "Perhelatan bisa kacau tanpa kehadiran lelaki itu. Gulai Kambing akan terasa hambar lantaran racikan bumbu tak meresap ke dalam daging. Kuah Gulai Kentang dan Gulai Rebung bakal encer karena keliru menakar jumlah kelapa parut hingga setiap menu masakan kekurangan santan. Akibatnya, berseraklah gunjing dan cela yang mesti ditanggung tuan rumah, bukan karena kenduri kurang meriah, tidak pula karena pelaminan tempat bersandingnya pasangan pengantin tak sedap dipandang mata, tapi karena macam-macam hidangan yang tersuguh tak menggugah selera. Nasi banyak gulai melimpah, tapi helat tak bikin kenyang. Ini celakanya bila Makaji, juru masak handal itu tak dilibatkan."

    # sentences = "Keterbukaan batik banyuwangi terhadap perwajahan baru, warna dan motif, menunjukkan watak orang Banyuwangi yang sangat percaya diri meramu aneka pengaruh untuk kemudian diakui sebagai identitas diri. Tabrak budaya ini juga terlihat pada ramuan kulinernya, seperti rawon malang dicampur dengan pecel madiun menjadi rawon pecel. Orang Banyuwangi sangat terbuka menerima budaya luar untuk diolah menjadi budaya Banyuwangi. Sinkretisme budaya yang juga tampak di batik banyuwangi ini menjadi sesuatu yang mutlak terjadi karena Banyuwangi hingga kini memang dihuni oleh beragam suku. Kedatangan beragam suku bangsa untuk tinggal menetap di Banyuwangi antara lain dimulai pada penjajahan Belanda. Belanda mendatangkan buruh perkebunan dari Jawa dan Madura."

    # sentences = "Kalau beberapa tahun yang lalu Tuan datang ke kota  kelahiranku  dengan menumpang  bis, Tuan akan berhenti di dekat pasar. Melangkahlah menyusuri jalan raya arah ke barat maka kira-kira sekilometer dari  pasar akan sampailah Tuan di jalan kampungku. Pada simpang  kecil  ke kanan, beloklah  ke jalan sempit itu. Dan di  ujung  jalan itu nanti  Tuan  temukan sebuah  surau  tua. Di depannya  ada  kolam ikan  yang  airnya mengalir melalui empat buah pancuran mandi."

    # sentences = "Begitulah pentingnya Makaji. Tanpa campur tangannya, kenduri terasa hambar, sehambar Gulai Kambing dan Gulai Rebung karena bumbu-bumbu tak diracik oleh tangan dingin lelaki itu. Sejak dulu, Makaji tak pernah keberatan membantu keluarga mana saja yang hendak menggelar pesta, tak peduli apakah tuan rumah hajatan itu orang terpandang yang tamunya membludak atau orang biasa yang hanya sanggup menggelar syukuran seadanya. Makaji tak pilih kasih, meski ia satu-satunya juru masak yang masih tersisa di Lareh Panjang. Di usia senja, ia masih tangguh menahan kantuk, tangannya tetap gesit meracik bumbu, masih kuat ia berjaga semalam suntuk."

    # sentences = "Aldi sedang membaca buku di teras rumah ketika ibu memasak sayur"
    # sentences = "Bandi memancing ikan di sungai bersama ayahnya dan keduanya pulang ke rumah hingga larut malam."
    # sentences = "Irfan tidur saat pelajaran di kelas sedang berlangsung dan Toni membangunkannya."
    # sentences = "Gilang makan gorengan di teras rumah sore tadi kemudian ayah ikut memakannya."
    # sentences = "Heru menyeberang dengan sangat hati – hati di jalan raya lalu memesan taksi secara online"
    # sentences = "Ia tertabrak mobil karena ia kurang hati-hati"
    # sentences = "Jangan bercakap sembari makan"

    # print(pt.tag_strings(path_tag_model, ss.tokenize_strings(sentences)))
    # raise Exception

    lexical_simplified = ls.lexical_simplify(sv_model=sv,
                                        wv_model=wv,
                                        word_freq_model=path_word_frequency_tsv,
                                        pos_tag_model=path_tag_model,
                                        raw_sentences=sentences,
                                        min_threshold=freq_min_threshold)

    rules = loadSyntactic()
    syntactic_simplified = ss.syntactic_simplify(lexical_simplified, path_tag_model, rules)
    print("Old:", sentences)
    print()
    print("Lexical Simplified:", lexical_simplified)
    print()
    print("Syntactic Simplified:", syntactic_simplified)
    print()

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