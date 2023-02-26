import nltk
nltk.download('wordnet')

import nltk.data
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt


def get_sentences_from_corpus(_filename):
    sents = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for line in open(_filename, 'r').readlines():
        sent_list = sent_detector.tokenize(line.strip())
        for sent in sent_list: sents.append(sent)
    return sents


def compute_distinct_combo_per_sent(_sent, _print_senses=False):
    # tokenize a sentence to analyse each word's available senses
    tokens  = word_tokenize(_sent)
    distinct_combo = 1
    for token in tokens:
        senses = wn.synsets(token)
        if _print_senses:
            print(f'\n{token}:')
            for sense in senses:
                print(f'{sense}: {sense.definition()}')
            continue
        n_senses = len(senses)
        # if a word returns 0 sense, convert 0 to 1 since there is
        # at least one sense for this word according to this corpus
        n_senses = n_senses if n_senses != 0 else 1
        distinct_combo *= n_senses
    return len(tokens), distinct_combo


def simplified_lesk(_word, _sent, _gloss):
    best_sense = None
    overlaps = []
    max_overlap = -1
    context = _sent
    senses = wn.synsets(_word)
    signature = _gloss + " "
    for sense in senses:

        signature += sense.definition()

        if len(sense.examples()) > 0:

            signature += ' '
            examples = sense.examples()
            for i in range(len(examples)):
                signature += examples[i]

        # compute number of overlap
        overlap = 0
        tokenized_signature = word_tokenize(signature)

        for i in range(len(context)):
            for j in range(len(tokenized_signature)):
                if context[i] == tokenized_signature[j]:
                    overlap += 1

        # check if overlap is more than max_overlap
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

        overlaps.append(overlap)

    return best_sense, overlaps, senses


# Response to 23.1
# Using WordNet or any standard dictionary, determine how many
# senses there are for each of the open-class words in each sentence.
# How many distinct combinations of senses are there for each sentence?
# How does this number seem to vary with sentence length?
show_res = False
if show_res:
    length_of_sent = []
    dist_combos = []
    sentences = get_sentences_from_corpus('small-corpus.txt')
    for sentence in sentences:
        sent_len, dist_combo = compute_distinct_combo_per_sent(sentence)
        if sent_len > 55: continue
        length_of_sent.append(sent_len)
        dist_combos.append(dist_combo)
    plt.plot(length_of_sent, dist_combos, 'rx')
    plt.xlabel('Sentence Length')
    plt.ylabel('Unique Combination of Senses')
    plt.show()


# Response to 23.2
show_senses = False
if show_senses:
    sentences = get_sentences_from_corpus('small-corpus.txt')
    for sentence in sentences:
        sent_len, dist_combo = compute_distinct_combo_per_sent(sentence, True)


# Response to 23.3
run_lesk = True
if run_lesk:

    print('\nSimple Lesk')

    test_sent = "Time flies like an arrow"
    tokenized_sent = word_tokenize(test_sent)

    gloss = ""
    for word in tokenized_sent:
        best_sense, _, _ = simplified_lesk(word, test_sent, gloss)
        if best_sense is not None:
            print(f'{word}: {best_sense.definition()}')
            gloss += " " + best_sense.definition()
        else:
            print(f'{word}: word sense not found')

# not a response to any textbook exercise...
# just an experiment to see if collecting
# overlap bidirectionally helps with accuracy

# this bidirectional method seems to have
# the same performance as the simple version.

run_bidirectional_lesk = True
if run_bidirectional_lesk:

    print('\nBidirectional Lesk')

    test_sent = "Time flies like an arrow"
    tokenized_sent = word_tokenize(test_sent)
    overlap_count_dict = {}

    gloss = ""
    for word in tokenized_sent:
        best_sense, overlaps, senses = simplified_lesk(word, test_sent, gloss)
        overlap_count_dict.update({word: {}})
        for i in range(len(senses)):
            overlap_count_dict[word].update({senses[i]: overlaps[i]})

    gloss = ""
    for word in reversed(tokenized_sent):
        best_sense, overlaps, senses = simplified_lesk(word, test_sent, gloss)
        for i in range(len(senses)):
            overlap_count_dict[word][senses[i]] += overlaps[i]

    print(overlap_count_dict)
    for word in tokenized_sent:
        overlap_count_dict[word] = dict(
            sorted(overlap_count_dict[word].items(),
                   key=lambda item: item[1], reverse=True ))
        if len(list(overlap_count_dict[word].keys())) > 0:
            best_sense = \
                list(overlap_count_dict[word].keys())[0].definition()
        else:
            best_sense = 'NOT FOUND'
        print(f'{word}: {best_sense}')

# run simple lesk on the entire small_corpus.txt
run_lesk_on_small_corpus = False
if run_lesk_on_small_corpus:
    run_for_n_sent = 5
    sentences = get_sentences_from_corpus('small-corpus.txt')
    i = 0
    gloss = ""
    for sentence in sentences:
        print(f'\n{sentence}\n')
        tokenized_sent = word_tokenize(sentence)
        for word in tokenized_sent:
            best_sense, _, _ = simplified_lesk(word, sentence, gloss)
            if best_sense is not None:
                print(f'{word}: {best_sense.definition()}')
                gloss += " " + best_sense.definition()
            else: print(f'{word}: word sense not found')
        i += 1
        if i > run_for_n_sent: break