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
