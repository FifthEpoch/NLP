from nltk.tokenize import word_tokenize
import numpy as np
import os
import math
import random

def tokenize_file(_filename):
    tokens = []
    dearray_tokens = []
    for line in open(_filename, 'r').readlines():
        words = [word.lower() for word in line.split() if len(word) >= 2]
        tokens.append(words)
    for word in tokens:
        dearray_tokens.append(word[0])
    return dearray_tokens

def generate_features(_sample, _pos_lexicon, _neg_lexicon):
    pos_cnt = 0
    neg_cnt = 0
    has_no = False
    has_switch = False
    pron_cnt = 0
    has_exc = False

    for token in _sample:

        token = token.lower()

        for word in _pos_lexicon:
            if word == token: pos_cnt += 1

        for word in _neg_lexicon:
            if word == token: neg_cnt += 1

        if token == 'no': has_no = True
        if token == 'but' or token == 'though' or token == 'although' or token == 'however': has_switch = True
        if token == '!': has_exc = True
        if token == 'i' or token == 'me' or token == 'you': pron_cnt += 1

    return [pos_cnt, neg_cnt, has_no, has_switch, pron_cnt, has_exc, math.log(len(_sample))]

def scaling_features(_X):
    # 0, 1, 3 are counts; 2, 4 are boolean
    # 5 is ln(len(sample)) -> scale as counts
    X = np.array(_X)
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    print(f'\n\n\nX.shape: {X.shape}\nmeans.shape: {means.shape}\nstds.shape: {stds.shape}\n')
    print(f'means: {means}\nstds: {stds}\n\n\n')

    scale_index = [0, 1, 4, 6]
    for index in scale_index:
        for row in X:
            row[index] = (row[index] - means[index]) / (stds[index]+0.0001)

    return X

def softmax(_x, _W, _CLASSES):
    nominators = []
    denominator = 0
    for i in range(len(_CLASSES)):
        nominators.append(np.exp(np.dot(_W[i][:-1], _x) + _W[i][-1]))
        denominator += nominators[i]
    probabilities = np.array(nominators) / denominator

    return probabilities


def get_true_state(_true_class, _CLASSES):
    true_index = np.argwhere(_CLASSES == _true_class)
    y = np.zeros(len(_CLASSES))
    y[true_index] = 1

    return y


def get_theta_via_cross_entropy(_W, _Xp, _probabilities, _y, _theta, _LEARNING_RATE, _CLASS_SIZE):
    loss = -((_y * np.log(_probabilities)) + ((1 - _y) * np.log(1 - _probabilities)))
    difference = _probabilities - _y
    new_theta = []

    for i in range(_CLASS_SIZE):

        gradient = np.array([])
        for j in range(len(_Xp)):
            gradient = np.append(gradient, difference[i] * _Xp[j])

        gradient = np.append(gradient, difference[i])
        new_theta.append(_theta[i] - (_LEARNING_RATE * gradient))

    return loss, np.array(new_theta)


def regularization(_theta):
    return 0

if __name__ == "__main__":

    training_set = [{'review': 'The film is GORGEOUS but I sure would have appreciated more about the planet and local wildlife and less warfare.', 'class': 'pos'},
                    {'review': 'Great story Line. James Cameron did it again!', 'class': 'pos'},
                    {'review': 'Movie was beautifully done and had a strong story', 'class': 'pos'},
                    {'review': 'Too long, needed less weapon fighting, I think. Rest of show was beautiful and well done! Loved the baby and children scenes!', 'class': 'pos'},
                    {'review': 'Astonishing! Enthralling! Exciting! Immersive! None of these words could sensibly be applied to the three-and-a-quarter-hour Wet Smurfahontas stodgeathon that is Avatar: The Way of Water.', 'class': 'neg'},
                    {'review': 'I was in awe of the cinematography and animation but felt the story line was awful especially when the harpooned all the whales!! I had to walk out-very disappointed!', 'class': 'neg'},
                    {'review': 'none of its characters feel whole, even after three full hours', 'class': 'neg'},
                    {'review': 'Graphics of course were amazing but the story was blah, no surprises and it just dragged on WAY too long.', 'class': 'neg'},
                    {'review': 'The movie could have been alot shorter and still gotten the story in.', 'class': 'neu'},
                    {'review': 'visually stunning but the film lacked soul.', 'class': 'neu'},
                    {'review': "Avatar is still Avatar. Nothing new and nothing worse to call it bad, is somewhere in the middle. The new movie is an expansion of the Pandora universe and shows how would these people live in water. Its visual effect is just as good as the first one. This means that more than 10 years later James Cameron has successfully delivered the same effect to the screen and didn't offer us anything new, while we watch similar technology become commonplace amongst other movies and game titles. This movie would be much appreciated if it came out much sooner after the first one. This is not to say that it is a bad movie, but I don't think it was worthy to watch when it should have been delivered a long time ago, and especially when it takes around 3 hours to finish.", 'class': 'neu'}]

    test_set = [{'review': "The movie Avatar was amazing and spiritual. It's was a perfect 10", 'class': 'pos'},
                {'review': 'It was an all around amazing experience:) The story and visuals were great. If you liked the original then this one is a must see!', 'class': 'pos'},
                {'review': "I was bored. It wasn't realistic. How is a human military going to lose to bows and arrows?", 'class': 'neg'},
                {'review': 'Too much violence and they killed a whale during the movie. It was all unnecessary.', 'class': 'neg'},
                {'review': 'Good movie but a little too long. I liked the first one better but the special effects were better in part 2.', 'class': 'neu'}]

    pos_lexicon = tokenize_file('./lexicon/positive.txt')
    print(f'pos_lexicon: {pos_lexicon}')
    neg_lexicon = tokenize_file('./lexicon/negative.txt')
    print(f'neg_lexicon: {neg_lexicon}')

    # return [pos_cnt, neg_cnt, has_no, pron_cnt, has_exc, math.log(len(_sample))]
    FEATURE_DESCRIPTION = ['pos count', 'neg count', 'has no', 'has (but|although|though)', '1st & 2nd person pronounce count', 'has !', 'length of sample']
    CLASSES = np.array(['pos', 'neg', 'neu'])
    CLASS_SIZE = len(CLASSES)
    FEATURE_SIZE = len(FEATURE_DESCRIPTION)
    LEARNING_RATE = 1.0

    # create weight and bias vector with He initialization
    # each class has its own weights for each feature, and a scalar bias
    # W = np.array([[random.uniform(0, 1) * math.sqrt(2)] * (FEATURE_SIZE + 1) for i in range(CLASS_SIZE)])
    W = np.array([[0.2] * (FEATURE_SIZE + 1) for i in range(CLASS_SIZE)])
    theta = np.array([[0.0] * (FEATURE_SIZE + 1) for i in range(CLASS_SIZE)])
    X = []

    print("\nTRAINING...\n")
    for sample in training_set:
        sample_tokens = word_tokenize(sample['review'])
        print(f"Tokens:             {sample_tokens}")
        x = generate_features(sample_tokens, pos_lexicon, neg_lexicon)
        print(f"Features:           {x}")
        X.append(x)

    Xp = scaling_features(X)
    print(f"Features scaled:    {Xp}")
    current_sample = 0
    for sample in training_set:
        xp = Xp[current_sample]
        P = softmax(xp, W, CLASSES)
        print(f"after softmax:      {P}")
        y = get_true_state(sample['class'], CLASSES)
        print(f'true state:         {y}')
        loss, theta = get_theta_via_cross_entropy(W, xp, P, y, theta, LEARNING_RATE, CLASS_SIZE)
        print(f'loss:               {loss}')
        print(f'theta:              {theta}')
        current_sample += 1

    W = W + theta

    print("\nTESTING...\n")

    X = []
    accuracy = 0
    for sample in test_set:
        sample_tokens = word_tokenize(sample['review'])
        print(f"Tokens:             {sample_tokens}")
        x = generate_features(sample_tokens, pos_lexicon, neg_lexicon)
        print(f"Features:           {X}")
        X.append(x)

    Xp = scaling_features(X)
    print(f"Features scaled:    {Xp}")

    current_sample = 0
    for sample in test_set:

        xp = Xp[current_sample]
        P = softmax(xp, W, CLASSES)
        print(f"after softmax:      {P}")
        y_hat = np.argmax(P)
        y = get_true_state(sample['class'], CLASSES)

        if y[y_hat] == 1:
            print(f"correct:        class {sample['class']} classified as {CLASSES[y_hat]}")
            accuracy += 1
        else:
            print(f"wrong:          class {sample['class']} classified as {CLASSES[y_hat]}")

        current_sample += 1

    accuracy /= len(test_set)
    print(f'accuracy:               {accuracy}')
