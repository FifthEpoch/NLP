from nltk.tokenize import word_tokenize
import numpy as np
import re
import os

def compute_pp(_sentence, _unigram, _bigram, _word_types):

    N = len(_sentence)
    inside_root = 1.0
    for i in range(N - 1):

        count_unigram = 0
        for uni_item in _unigram:
            if uni_item['word'] == _sentence[i]:
                count_unigram = uni_item['count']

        matchedw1 = False
        for item in _bigram:
            if item['w1'] == _sentence[i]:
                matchedw1 = True
                matchedw2 = False

                for subitem in item['words']:
                    if subitem['w2'] == _sentence[i + 1]:
                        matchedw2 = True
                        count_bigram = subitem['count']
                        inside_root *= 1 / (count_bigram + 1 / count_unigram + _word_types) # Laplace smoothing

                if matchedw2 is not True:
                    inside_root *= 1 / (1 / count_unigram + _word_types)

        if matchedw1 is not True:
            inside_root *= 1 / (1 / count_unigram + _word_types)

    return inside_root ** (-1 / N)


def tokenize_file(_file_path):
    if os.path.exists(_file_path):
        with open(_file_path, 'r') as f:
            usr_input = f.read()
        f.close()

        return word_tokenize(usr_input)
    else:
        print("File does not exist. Please make sure that the file path you provide is valid. For testing, enter 'mid-size-corpus.txt'.")
        new_file_path = input('Enter a file path: ')
        tokenized_usr_input = tokenize_file(new_file_path)

        return tokenized_usr_input


def remove_punctuation_tokens(_tokens):

    for i in range(len(_tokens)):
        if re.match(r"^(``|''|,|\.|—|-|;|:|'|\")$", _tokens[i]):
            _tokens[i] = '</s>'
            _tokens.insert(i+1, '<s>')

    _tokens.insert(0, '<s>')
    _tokens.insert(len(_tokens) - 1, '</s>')

    return _tokens


def extract_cnt(_item):
    return _item['count']

def extract_highest_w2_count(_item):
    return _item['words'][0]['count']

def generate_unigram(_tokens):
    unigram = []
    _tokens = remove_punctuation_tokens(_tokens)
    for token in _tokens:
        found = False
        for items in unigram:
            if token == items['word']:
                items['count'] += 1
                found = True
                break
        if not found:
            unigram.append({'word':token, 'count':1})

    unigram.sort(key=extract_cnt, reverse=True)

    print('UNIGRAM')
    for item in unigram:
        print(f"{item['word']}:     {item['count']}")

    return unigram

def generate_bigram(_tokens):

    bigram = []
    _tokens = remove_punctuation_tokens(_tokens)
    for i in range(len(_tokens) - 1):
        matchedw1 = False
        for item in bigram:
            if _tokens[i] == item['w1']:
                matchedw1 = True
                matchedw2 = False
                for subitem in item['words']:
                    if _tokens[i+1] == subitem['w2']:
                        matchedw2 = True
                        subitem['count'] += 1
                if not matchedw2:
                    item['words'].append({'w2': _tokens[i+1], 'count': 1})
        if not matchedw1:
            bigram.append({'w1': _tokens[i], 'words': [{'w2': _tokens[i+1], 'count': 1}]})

    for item in bigram:
        item['words'].sort(key=extract_cnt, reverse=True)

    bigram.sort(key=extract_highest_w2_count, reverse=True)
    print('BIGRAM')
    for item in bigram:
        for subitem in item['words']:
            print(f"{item['w1']} {subitem['w2']}:          {subitem['count']}")

    return bigram


def generate_sentence(_bigram):

    sentence = ['<s>']
    while sentence[-1] != '</s>':
        probabiliy = []
        words = []
        for item in _bigram:
            if item['w1'] == sentence[-1]:
                probabiliy = np.array([item['words'][i]['count'] for i in range(len(item['words']))], dtype='float64')
                words = np.array([item['words'][i]['w2'] for i in range(len(item['words']))])
        probabiliy /= np.sum(probabiliy)
        next_word = np.random.choice(words, 1, p=probabiliy)[0]
        sentence.append(next_word)

    string = ''
    for word in sentence:
        string += (word + ' ')
    print(string)

    return sentence


# export this


