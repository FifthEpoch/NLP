import numpy as np
import os
import math
import random

classes = ['pos', 'neg', 'neu']
training_set = {'pos': ['The film is GORGEOUS but I sure would have appreciated more about the planet and local wildlife and less warfare.',
                        'Great story Line. James Cameron did it again!',
                        'Movie was beautifully done and had a strong story',
                        'Too long, needed less weapon fighting, I think. Rest of show was beautiful and well done! Loved the baby and children scenes!'],
                'neg': ["I was bored. It wasn't realistic. How is a human military going to lose to bows and arrows?",
                        'I was in awe of the cinematography and animation but felt the story line was awful especially when the harpooned all the whales!! I had to walk out-very disappointed!',
                        'none of its characters feel whole, even after three full hours',
                        'Graphics of course were amazing but the story was blah, no surprises and it just dragged on WAY too long.'],
                'neu': ['The movie could have been alot shorter and still gotten the story in.',
                        'visually stunning but the film lacked soul.',
                        "Avatar is still Avatar. Nothing new and nothing worse to call it bad, is somewhere in the middle. The new movie is an expansion of the Pandora universe and shows how would these people live in water. Its visual effect is just as good as the first one. This means that more than 10 years later James Cameron has successfully delivered the same effect to the screen and didn't offer us anything new, while we watch similar technology become commonplace amongst other movies and game titles. This movie would be much appreciated if it came out much sooner after the first one. This is not to say that it is a bad movie, but I don't think it was worthy to watch when it should have been delivered a long time ago, and especially when it takes around 3 hours to finish."]}
test_set = {'pos': ["The movie Avatar was amazing and spiritual. It's was a perfect 10",
                    'It was an all around amazing experience:) The story and visuals were great. If you liked the original then this one is a must see!'],
            'neg': ['Astonishing! Enthralling! Exciting! Immersive! None of these words could sensibly be applied to the three-and-a-quarter-hour Wet Smurfahontas stodgeathon that is Avatar: The Way of Water.',
                    'Too much violence and they killed a whale during the movie. It was all unnecessary.'],
            'neu': ['Good movie but a little too long. I liked the first one better but the special effects were better in part 2.']}

def tokenize_file(_filename):
    tokens = []
    for line in open(_filename, 'r').readlines():
        words = [word.lower() for word in line.split() if len(word) >= 3]
        tokens.append(words)
    return tokens

def generate_features(_sample, _pos_lexicon, _neg_lexicon):
    pos_cnt = 0
    neg_cnt = 0
    has_no = False
    pron_cnt = 0
    has_exc = False

    for token in _sample:

        token = token.lower()

        for word in _pos_lexicon:
            if word == token: pos_cnt += 1

        for word in _neg_lexicon:
            if word == token: neg_cnt += 1

        if token == 'no': has_no = True
        if token == '!': has_exc = True
        if token == 'i' or token == 'me' or token == 'you': pron_cnt += 1

    return [pos_cnt, neg_cnt, has_no, pron_cnt, has_exc, math.log(len(_sample))]

def scaling_features(_X):
    # 0, 1, 3 are counts; 2, 4 are boolean
    # 5 is ln(len(sample)) -> scale as counts
    X = np.array(_X)
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)

    for vector in X:
        scale_index = [0, 1, 3, 5]
        for index in scale_index:
            vector[index] = (vector[index] - means[index]) / stds[index]

    return X

def softmax(_x, _w, _b):
    nominators = np.exp((_w * _x) + _b)
    denominator = np.sum(nominators)
    probabilities = nominators / denominator

    return probabilities



if __name__ == "__main__":

    pos_lexicon = tokenize_file('./lexicon/positive.txt')
    neg_lexicon = tokenize_file('./lexicon/negative.txt')

    CLASS_SIZE = len(classes)

    # create weight vector with He initialization
    w = [random.uniform(0, 1) * math.sqrt(2) for i in range(CLASS_SIZE)]
    # create bias vector
    b = [random.uniform(0, 1) * math.sqrt(2) for i in range(CLASS_SIZE)]







