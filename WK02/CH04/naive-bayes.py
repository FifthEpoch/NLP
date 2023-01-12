import numpy as np
from nltk.tokenize import word_tokenize
import math

C = ['pos', 'neg']
D = [{'good': 3, 'poor': 0, 'great': 3, 'class': 'pos'},
     {'good': 0, 'poor': 1, 'great': 2, 'class': 'pos'},
     {'good': 1, 'poor': 3, 'great': 0, 'class': 'neg'},
     {'good': 1, 'poor': 5, 'great': 2, 'class': 'neg'},
     {'good': 0, 'poor': 2, 'great': 0, 'class': 'neg'}]

def generate_V(_D):
    V = []
    for item in _D[0]:
        if item != 'class': V.append(item)
    return V

def print_res(_mode, _logprior, _loglikelihood, _sums, _max_val_c):
    print(f'mode:                       {_mode}')
    print('-------------------------------------------------------')
    print(f'logprior for "pos":         {_logprior["pos"]}')
    print(f'logprior for "neg":         {_logprior["neg"]}')
    print(f'loglikelihood for "pos":    {_loglikelihood["pos"]}')
    print(f'loglikelihood for "neg":    {_loglikelihood["neg"]}')
    print(f'sum for "pos" class:        {_sums["pos"]}')
    print(f'sum for "neg" class:        {_sums["neg"]}')
    print(f'most likely class:          {_max_val_c}\n')

def test_naive_bayes(_d, _logprior, _loglikelihood, _C, _V):
    sums = {}
    max_val = -1000.0
    max_val_c = 'Not yet determined'

    for c in _C:

        sums.update({c: _logprior[c]})

        for w in _d:
            if w not in _V: continue
            sums[c] += _loglikelihood[c][w]

        if sums[c] > max_val:
            max_val = sums[c]
            max_val_c = c

    return max_val_c, sums

def train_naive_bayes(_C, _D, binary_mode=False):
    N_doc = len(_D)
    loglikelihood = {}
    logprior = {}
    bigdoc = {}

    V = generate_V(_D)

    for c in _C:
        N_c = 0
        bigdoc.update({c: {'good': 0, 'poor': 0, 'great': 0, 'total': 0}})

        for i in range(len(_D)):
            if _D[i]['class'] == c:
                N_c += 1
                for item in _D[i]:
                    if item != 'class':
                        if binary_mode:
                            if _D[i][item] > 0: bigdoc[c][item] += 1
                        else:
                            bigdoc[c][item] += _D[i][item]
                        bigdoc[c]['total'] += _D[i][item]

        logprior.update({c: math.log(N_c / N_doc, 10)})
        loglikelihood.update({c: {}})

        for item in bigdoc[c]:
            if item == 'total': continue
            loglikelihood[c].update(
                {item: math.log((bigdoc[c][item] + 1) / (bigdoc[c]['total'] + len(V)), 10)})

    return logprior, loglikelihood, V


if __name__ == "__main__":

    test_d = 'A good, good plot and great characters, but poor acting.'
    test_d = word_tokenize(test_d)
    print(f"tokens:                 {test_d}\n")

    logprior, loglikelihood, V = train_naive_bayes(C, D, binary_mode=False)
    max_val_c, sums = test_naive_bayes(test_d, logprior, loglikelihood, C, V)
    print_res("multinomial", logprior, loglikelihood, sums, max_val_c)

    logprior, loglikelihood, V = train_naive_bayes(C, D, binary_mode=True)
    max_val_c, sums = test_naive_bayes(test_d, logprior, loglikelihood, C, V)
    print_res("binary", logprior, loglikelihood, sums, max_val_c)