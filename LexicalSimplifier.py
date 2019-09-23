import nltk
import re
import FileManager as fm
from sensegram import sensegram
from sensegram.wsd import WSD
nltk.download('punkt')

def tokenize_strings(strings):
    return nltk.tokenize.word_tokenize(strings)

def preprocess_tokenized(tokenized_string):
    return 0

def get_word_freq(word, word_freq_model):
    if word in word_freq_model:
        return word_freq_model[word]
    else:
        return 0

def count_word_frequency(strings, word_freq_model = None):
    if word_freq_model == None:
        word_freq = {}
    else:
        word_freq = word_freq_model
    strings = strings.split()
    word_count = len(strings)
    # Include first word but do not count
    i = 0
    word_freq[str.lower(strings[0])] = 0
    # ([str.lower(strings[0]), 0])
    for word in strings:
        i += 1
        # print("Processing", i, "out of", word_count, 'string count')
        if str.lower(word) in word_freq.keys():
            word_freq[str.lower(word)] += 1
        else:
            word_freq[str.lower(word)] = 1
    # print(word_freq)
    return word_freq


def lexical_simplify(sv_model, wv_model, word_freq_model, raw_sentences, min_threshold):
    # Load Word Frequencies
    word_freq = fm.load_word_freq(model_path=word_freq_model)

    # Clean Sentences
    sentences = fm.clean_strings(raw_sentences)

    # Tokenize
    sentences = tokenize_strings(sentences)

    # Check Frequencies
    complex_words = {}
    for word in sentences:
        if str.lower(word) in word_freq.keys() and word_freq[str.lower(word)] < min_threshold:
            complex_words[word] = word_freq[str.lower(word)]

    print(complex_words)

    replaced_words = {}
    for c_word, freq_val in complex_words.items():
        print("Probabilities of the senses:\n{}\n\n".format(sv_model.get_senses(str(c_word), ignore_case=True)))

        for sense_id, prob in sv_model.get_senses(str(c_word), ignore_case=True):
            print(sense_id)
            print("=" * 20)
            # rsense_id --> bentuknya kata_asal#no_id
            # sim --> persentase similarity dalam range 0-1

            for rsense_id, sim in sv_model.wv.most_similar(sense_id):
                print("{} {:f}".format(rsense_id, sim))
            print("\n")

        # Disambiguate a word in a context
        wsd_model = WSD(sv_model, wv_model, window=5, max_context_words=3, method='sim', ignore_case=True)
        print(wsd_model.disambiguate(raw_sentences, str(c_word)))

        replaced_words[str.lower(c_word)] = sv_model.wv.most_similar(wsd_model.disambiguate(raw_sentences, str(c_word))[0])

    for key, val in replaced_words.items():
        # (before #, '#', after '#')
        replacement, sep, tail = replaced_words[key][0][0].partition('#')
        if get_word_freq(replacement, word_freq) > get_word_freq(key, word_freq):
            # Select Highest
            replaced_words[key] = replacement
        # for new_word in replaced_words[key]:
        #     # (before #, '#', after '#')
        #     replacement, sep, tail = new_word[0].partition('#')
        #     # print(replaced_words[key])
        #     print(replacement, ls.get_word_freq(replacement, word_freq))

        print(replaced_words)

    for old_word, new_word in replaced_words.items():
        raw_sentences = re.sub(old_word, new_word, raw_sentences)

    return raw_sentences
