import re
import math

import nltk
nltk.download('brown')

from nltk.corpus import brown
def generate_dict(_samples):
    # create a tag dictionary that captures
    # the count of each (word, tag) combo
    dictionary = {}
    for sample in _samples:
        if sample[0] not in dictionary:
            dictionary.update({sample[0]: [{'tag': sample[1], 'count': 1}]})
        else:
            matched = False
            for item in dictionary[sample[0]]:
                if item['tag'] == sample[1]:
                    item['count'] += 1
                    matched = True
                    break
            if not matched: dictionary[sample[0]].append({'tag': sample[1], 'count': 1})

    def get_tag_counts(subitem):
        return subitem['count']

    for item in dictionary:
        sorted(dictionary[item], key=get_tag_counts, reverse=True)

    return dictionary

def predict_tag(_test_set, _tag_dict):
    accuracy = 0
    for item in _test_set:
        word = item[0]
        true_tag = item[1]
        if word in _tag_dict:
            # assign tag with the highest count
            # if there are more than 1 tag for a given word
            # return the only tag if there is just 1 tag
            prediction = _tag_dict[word][0]['tag']
        else:
            # assign noun tag to unknown words
            prediction = 'NN'
        if prediction == true_tag: accuracy += 1
    accuracy /= len(_test_set)
    print(f"Assuming that all unknown words are NN")
    print(f">> accuracy: {accuracy}")
    return accuracy

def predict_tag_with_improvements(_test_set, _tag_dict):
    accuracy = 0
    for item in _test_set:
        word = item[0]
        true_tag = item[1]
        if word in _tag_dict:
            prediction = _tag_dict[word][0]['tag']
        else:
            prediction = 'NN'
            # additional rules to analyze unknown words
            if re.match('.*ing$', word):
                prediction = 'VBG'
            elif re.match(".*'s$", word):
                prediction = 'NP$'
            elif re.match('.*s$', word):
                prediction = 'NNS'
            elif re.match('.+ly$', word):
                prediction = 'RB'
            elif re.match('.+ed$', word):
                prediction = 'VBN'
            elif re.match('.+(ble|ish|ful|can|ky|dy|ic|ous|ern)$', word):
                prediction = 'JJ'
            elif re.match('\d+(,)?\d*(\.\d+)?$', word):
                prediction = 'CD'
            elif re.match('[A-Z][a-z]+', word):
                prediction = 'NP'

        if prediction == true_tag: accuracy += 1
    accuracy /= len(_test_set)
    print(f"With additional rules for unknown words")
    print(f">> accuracy: {accuracy}")
    return accuracy

if __name__ == "__main__":

    CORPUS = brown.tagged_words(categories='news')
    CORPUS_SIZE = len(brown.tagged_words(categories='news'))

    CUT_OFF = math.floor(CORPUS_SIZE * 0.75)

    # section off training and testing lists from corpus
    training_list = CORPUS[:CUT_OFF]
    testing_list = CORPUS[CUT_OFF:]

    # duplicates are ignored in sets
    training_set = set(training_list)
    testing_set = set(testing_list)
    intersection = training_set.intersection(testing_set)

    print(f"length of training set:     {len(training_list)}")
    print(f"length of testing set:      {len(testing_list)}")

    # uncommetn to see how much the training set and testing set overlap
    # print(f"intersection:               {len(intersection)}")

    # uncomment to survey tagged corpus
    # print(training_set)

    tag_dict = generate_dict(training_list)
    accurary_base = predict_tag(testing_list, tag_dict)
    accurary_impr =predict_tag_with_improvements(testing_list, tag_dict)
    delta = math.floor((accurary_impr - accurary_base) * len(testing_list))
    print(f"{delta} more words got correctly classified.")










