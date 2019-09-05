import FileManager as fm
import POSTagger as pt
import LexicalSimplifier as ls
import os
import csv
import time

path_full_dataset = 'dataset/full'
path_simp_dataset = 'dataset/simplified'
path_postag_dataset = 'dataset/POSTag/Indonesian_Manually_Tagged_Corpus_ID.tsv'
path_tag_model = 'model/all_indo_man_tag_corpus_model.crf.tagger'
path_word_frequency_tsv = 'word_frequency/word_freq.tsv'

def trainLexical():
    files = fm.get_dataset(path_full_dataset, path_simp_dataset)
    i = 0
    time_start = time.perf_counter()
    for f in files:
        word_freq_temp = {}
        if os.path.exists(path_word_frequency_tsv):
            with open(path_word_frequency_tsv) as csv_file:
                for row in csv_file:
                    (key, val) = row.split()
                    word_freq_temp[str(key)] = int(val)
        i += 1
        print("Processing", i, 'of', len(files), 'dataset')
        word_freq_temp = ls.count_word_frequency(fm.read_raw_dataset(f), word_freq_temp)
        fm.save_word_freq(word_freq_temp)
    time_stop = time.perf_counter()
    print("Counting Complete, time elapsed", time_stop-time_start, 'seconds')

if __name__ == "__main__":
    # Run to count word frequency
    trainLexical()

    #
    # pt.train_pos_tag(path_postag_dataset, path_tag_model)
    # print(pt.tag_strings(path_tag_model, tokenized_string=['']))
    # XXX
    # parser = argparse.ArgumentParser("Text Simplifier")
    # parser.add_argument("--txt", help="String yang akan disederhanakan", type=str)
    # parser.add_argument("--dir", help="Directory file yang ingin disederhanakan", type=str)
    # args = parser.parse_args()
    # print(args)