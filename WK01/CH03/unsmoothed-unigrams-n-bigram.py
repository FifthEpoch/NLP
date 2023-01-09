#import nltk
from nltk.tokenize import word_tokenize
import re
import os

def tokenize_file(_file_path):
    if os.path.exists(_file_path):
        with open(_file_path, 'r') as f:
            usr_input = f.read()
        f.close()
        return word_tokenize(usr_input)
    else:
        print("File does not exist. Please make sure that the file path you provide is valid. For testing, enter 'mid-size-corpus.txt'.")
        new_file_path = input('Enter a file path: ')
        return tokenize_file(new_file_path)

def remove_punctuation_tokens(_tokens):
    for i in range(len(_tokens)):
        if re.match(r"^(``|''|,|\.|—|-|;|:|'|\"|’)$", _tokens[i]):
            _tokens[i] = '</s>'
            _tokens.insert(i+1, '<s>')
    _tokens.insert(0, '<s>')
    _tokens.insert(len(_tokens) - 1, '</s>')
    return _tokens

def extract_cnt(_item):
    return _item['count']

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
    for item in unigram:
        print(f"{item['word']}:     {item['count']}")

def generate_bigram(_tokens):
    bigram = []
    _tokens = remove_punctuation_tokens(_tokens)
    for i in range(len(_tokens)-1):
        matched = False
        for item in bigram:
            if _tokens[i] == item['w1'] and _tokens[i+1] == item['w2']:
                matched = True
                item['count'] += 1
        if not matched:
            bigram.append({'w1': _tokens[i], 'w2': _tokens[i+1], 'count':1})

    bigram.sort(key=extract_cnt, reverse=True)
    for item in bigram:
        print(f"{item['w1']} {item['w2']}:          {item['count']}")


if __name__ == "__main__":
    file_path = input('Enter a file path: ')
    tokens = tokenize_file(file_path)
    print(f"token: {tokens}")
    generate_unigram(tokens)
    print('\n\n')
    generate_bigram(tokens)