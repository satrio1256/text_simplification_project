import re
import nltk
import POSTagger as pt
import os
import time

def tokenize_strings(strings):
    return nltk.tokenize.word_tokenize(strings)

def detokenize_strings(tagged_tokenized):
    sentences = ""
    for idx, val in enumerate(tagged_tokenized):
        next_token = None
        
        if idx+1 < len(tagged_tokenized):
            next_token = tagged_tokenized[idx+1]

        if next_token is None or next_token[0] is "." or next_token[0] is ",":
            sentences += val[0]
        else:
            sentences += val[0] + " "
    return sentences

def load_rule(rule_path):
    if not os.path.isfile(rule_path):
        message = "Model not found, is path correct? (Current Settings: " + rule_path + ")"
        raise FileNotFoundError(message)
    else:
        rules = {}
        with open(rule_path) as csv_file:
            for row in csv_file:
                (conjunction, before, after) = row.split()
                if conjunction in rules.keys():
                    if before is "NULL":
                        before = ""
                    if after is "NULL":
                        after = ""
                    rules[str(conjunction)].append([before.split(","), after.split(",")])
                else:
                    if before is "NULL":
                        before = ""
                    if after is "NULL":
                        after = ""
                    rules[str(conjunction)] = [[before.split(","), after.split(",")]]
    return rules

def simplify_sentence(sentence, sentence_idx, conj_idx):
    # print("Old Sentence", sentence)
    is_question = False
    for word in sentence:
        # If is question sentence or punctuation is "?"
        if word[1] == "WH" or re.match("\\?+", word[0]):
            is_question = True
    if not is_question:
        before_conj = sentence[0:conj_idx-sentence_idx[0]]
        after_conj = sentence[conj_idx-sentence_idx[0]+1:len(sentence)]
        # Add Punctuation on before_conj to split sentences
        before_conj.append(('.', 'Z'))
        # Fix Capitalization on after_conj
        after_conj[0] = (str(after_conj[0][0]).title(), after_conj[0][1])
        return before_conj + after_conj

def get_sentence_idx(tokenized_sentences, conj_idx):
    begin_of_sentence = None
    end_of_sentence = None
    for idx in reversed(range(0, conj_idx)):
        if re.match("\\.+", tokenized_sentences[idx][0]):
            begin_of_sentence = idx+1
            break
        # If reach beginning of sentences
        elif idx == 0:
            begin_of_sentence = 0
            break
    for idx in range(conj_idx+1, len(tokenized_sentences)):
        # If current tag is a dot(.)
        if re.match("\\.+", tokenized_sentences[idx][0]):
            end_of_sentence = idx
            break
        # If reach end of sentences
        elif idx == len(tokenized_sentences)-1:
            end_of_sentence = len(tokenized_sentences)
            break
    return begin_of_sentence, end_of_sentence

def break_sentence(tokenized_sentences, sentence_idx):
    # +1 Due to python slice notation list[start:stop] and stop value is stop-1 by default.
    sentence_to_process = tokenized_sentences[sentence_idx[0]:sentence_idx[1]+1]
    return sentence_to_process

def rule_reader(conjunction, rules):
    return 0

def syntactic_simplify(raw_sentences, tagger_model, rules):
    # Select [0] to remove multiple array from POS Tagger
    tokenized_sentences = pt.tag_strings(tagger_model, tokenize_strings(raw_sentences))[0]
    old_tokenized = tokenized_sentences
    conjunctions = []
    for index, word in enumerate(tokenized_sentences):
        if str(word[1]).upper() == 'CC' or str(word[1]).upper() == 'SC':
            conjunctions.append((index, word))
    for conjunction in conjunctions:
        # print(conjunction)
        try:
            for rule in rules[str(conjunction[1][0]).lower()]:
                match_before = False
                match_after = False
                # Compare if word before conjunction is matching rule
                for r in rule[0]:
                    try:
                        # If word tag before this conjunction is match rule
                        # print("Before Tag:", tokenized_sentences[conjunction[0] - 1][1], "compare to", r)
                        if tokenized_sentences[conjunction[0]-1][1] == r:
                            match_before = True
                            break
                    except IndexError:
                        break
                # Compare if word after conjunction is matching rule
                for r in rule[1]:
                    try:
                        # If word tag after this conjunction is match rule
                        # print("After Tag:", tokenized_sentences[conjunction[0] + 1][1], "compare to", r)
                        if tokenized_sentences[conjunction[0]+1][1] == r:
                            match_after = True
                            break
                    except IndexError:
                        break
                if match_before and match_after:
                    # print("Rule Found!")
                    break
                else:
                    continue
                    # print("Rule Not Match for word:", conjunction[1][0])
                    # print("Retrying...")
        except KeyError:
            # Meaning word is not exist in rule
            print()

        sentence_idx = (get_sentence_idx(tokenized_sentences, conjunction[0]))
        sentence_to_process = break_sentence(tokenized_sentences, sentence_idx)

        tokenized_sentences = tokenized_sentences[0:sentence_idx[0]] + \
                        simplify_sentence(sentence=sentence_to_process, sentence_idx=sentence_idx, conj_idx=conjunction[0]) + \
                        tokenized_sentences[sentence_idx[1]+1:len(tokenized_sentences)]

        # print("For conjunction:", conjunction[1][0])
        # print("Old:", detokenize_strings(old_tokenized))
        # print("=====================")
        # print("New:", detokenize_strings(tokenized_sentences))
        # print()

    return detokenize_strings(tokenized_sentences)