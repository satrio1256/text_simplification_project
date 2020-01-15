# Lexical and Syntactic Simplification for Indonesian Text
This repository contains the used source code that is used on the paper titled above.

## Installation
The project is implemented in Python 3 with the Sensegram source code released on 

https://github.com/uhh-lt/sensegram/tree/master

To start, put the downloaded (Sensegram) source code above into the root directory. 
Then, download the pretrained model from https://drive.google.com/open?id=1A6_oaR7Cc_pZoRn2f0PkuSrb0bOj-pgN and put the files in the respective directory as detailed below.

```
[root/model]
all_indo_man_tag_corpus_model.crf.tagger

[root/word_frequency]
word_freq.tsv

[root/sensegram/model]
idwiki-latest.cbow1-size300-window5-iter5-mincount10-bigramsFalse.word_vectors
idwiki-latest.n200.clusters.minsize5-1000-sum-score-20.sense_vectors

[root/dataset/syntactic_rules]
rule_syntactic.tsv
```

After that, install the missing required library and you're good to go

## Run
To run the simplifier, run this command in the terminal

```
python simplifier.py --text "String to simplify"
```

## References
Will be added later
