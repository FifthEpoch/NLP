import math
from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import torch
from scipy.spatial.distance import cosine

import nltk
nltk.download('comtrans')
from nltk.corpus import comtrans
words = comtrans.words('alignment-en-fr.txt')
als = comtrans.aligned_sents('alignment-en-fr.txt')
for word in words[:6]:
    print(word)
print(als[1])
print(als[1].alignment)


def compute_softmax(_arr):
    softmax = np.array(len(_arr))
    sum = 0.0
    for i in range(np.shape(_arr)[0]):
        for j in range(np.shape(_arr)[1]):
            val = math.exp(_arr[i][j])
            sum += math.exp(val)
            softmax[i] = math.exp(val)
    softmax /= sum
    return softmax

def self_attention(_Q, _K, _V, _d, _bidir=False):
    # make masked QK^T first
    # upper triangle entries are set to -infinity
    QK = np.dot(_Q, _K)
    if not _bidir:
        for row in range(np.shape(QK)[0]):
            for col in reversed(range(row, np.shape(QK)[1])):
                QK[row][col] = float('-inf')
    QK /= math.sqrt(_d)
    softmax = compute_softmax(QK)
    # Y = np.dot(softmax, _V)
    return np.dot(softmax, _V)

def layer_norm(_X, _alpha=1.0, _beta=0.0):
    """

    :param _X:      input matrix, each row represent vec(x)_i
    :param _alpha:  learned gain value
    :param _beta:   learned offset value
    :return: new _X with normalized entries
    """

    mean = np.mean(_X, axis=1)
    std = np.std(_X, axis=1)
    return _alpha * ((_X - mean) / std) + _beta

def activation(_input):
    return math.tanh(_input)

# X are tokens of the input sequence into a single matrix
# each row of X is the embedding of ONE token of the input
X = np.zeros((3,2))
W_Q = np.zeros((3,2))
W_K = np.zeros((3,2))
W_V = np.zeros((3,2))
# Query
Q = np.dot(np.transpose(X), W_Q)
# Key
K = np.dot(np.transpose(X), W_K)
# Value
V = np.dot(np.transpose(X), W_V)

