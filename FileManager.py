import csv
import os
import re
import string
from pathlib import Path
import StopwordRemover as sr

def get_dataset(path_full_dataset):
    files = []
    # r = root, d = directories, f = files
    for r, d, f in os.walk(path_full_dataset):
        for file in f:
            files.append(os.path.join(r, file))
    return files

def clean_strings(strings):
    # Remove Wiki Tags
    strings = re.sub('<[^>]*>', '', strings)
    # Remove hyphen and long hyphen by regex to prevent unexpected merged word after punctuation removal
    strings = re.sub(r'\b-\b', ' ', strings)
    strings = re.sub('—', ' ', strings)
    # Remove Punctuations
    strings = strings.translate(str.maketrans('', '', string.punctuation))
    # Remove Digits
    strings = strings.translate(str.maketrans('', '', string.digits))
    # print(strings)
    # Remove Unicode Character
    strings = (strings.encode('ascii', 'ignore')).decode("utf-8")
    # Remove StopWords
    strings = sr.remove_stopword(strings)
    # Stemming
    strings = sr.start_stemming(strings)
    return strings

def read_raw_dataset(file, clean=True):
    f = open(Path(file), "r", encoding='utf-8')
    # Read the content
    contents = f.read()
    # Remove HTML tag
    if clean:
        contents = clean_strings(contents)
    return contents

def save_word_freq(word_freq, word_model):
    if not os.path.exists('model/word_frequency'):
        os.makedirs("word_frequency")
    with open(word_model, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for key in sorted(word_freq):
            writer.writerow([key, word_freq[key]])

def load_word_freq(model_path):
    if not os.path.isfile(model_path):
        message = "Model not found, is path correct? (Current Settings: "+model_path+")"
        raise FileNotFoundError(message)
    else:
        word_freq_temp = {}
        with open(model_path) as csv_file:
            for row in csv_file:
                (key, val) = row.split()
                word_freq_temp[str(key)] = int(val)
    return word_freq_temp
