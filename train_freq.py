import FileManager as fm
import LexicalSimplifier as ls
import time
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

path_full_dataset = 'dataset/full'
path_word_frequency_tsv = 'model/word_frequency/word_freq_new.tsv'

def clean_word_model():
    word_freq = fm.load_word_freq(path_word_frequency_tsv)
    word_to_delete = []
    for key, val in word_freq.items():
        # Remove if less than 5 due to typos
        if val < 100:
            word_to_delete.append(key)
    for word in word_to_delete:
        del word_freq[word]
    fm.save_word_freq(word_freq, path_word_frequency_tsv)
    print(sorted(word_freq.values()))

if __name__ == "__main__":
    # plt.hist(sorted(fm.load_word_freq(path_word_frequency_tsv).values()), bins=4000)
    # plt.gca().set(title='Frequency Histogram', ylabel='Frequency');
    # plt.show()
    # exit()
    # clean_word_model()
    word_freq = fm.load_word_freq(path_word_frequency_tsv)
    print(max(word_freq.values()))
    print(max(word_freq.values())/2)
    summage = 0
    for key,val in word_freq.items():
        if val < 110:
            summage += 1
            print(key)
    print(summage, "words is under median. Total actual words:", len(word_freq.keys()))
    exit("Delete Complete")
    # parser = argparse.ArgumentParser("Text Simplifier")
    # parser.add_argument("string", metavar="data_path", help="Path letak dataset untuk training", type=str)
    # # parser.add_argument("--dir", help="Directory file yang ingin disederhanakan", type=str)
    # args = parser.parse_args()
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
        fm.save_word_freq(word_freq_temp, path_word_frequency_tsv)
    time_stop = time.perf_counter()
    print("Counting Complete, time elapsed", time_stop-time_start, 'seconds')