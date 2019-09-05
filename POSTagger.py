from nltk.tag import CRFTagger
import re

def train_pos_tag(dataset_dir, output_path):
    jumSample = 500000
    namaFile = dataset_dir
    with open(namaFile, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    pasangan = []
    allPasangan = []

    for line in lines[: min(jumSample, len(lines))]:
        # Remove Wiki Tags
        line = re.sub('<[^>]*>', '', line)
        if line == '':
            if len(pasangan) != 0:
                allPasangan.append(pasangan)
            pasangan = []
        else:
            kata, tag = line.split('\t')
            p = (kata, tag)
            pasangan.append(p)

    ct = CRFTagger()
    print("Training Tagger...")
    ct.train(allPasangan, output_path)
    print("Training Complete")

def tag_strings(path_to_model, tokenized_string):
    ct = CRFTagger()
    ct.set_model_file(path_to_model)
    tagged_strings = ct.tag_sents([['Saya', 'bekerja', 'di', 'Bandung'], ['Nama', 'saya', 'Yudi']])
    return tagged_strings
