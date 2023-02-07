from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import torch
import math

def bert_text_preprocessing(_text, _tokenizer):
    # adds bert-specific tokens
    tagged_text = "[CLS] " + _text + " [SEP]"
    # tokenize text
    tokenized_text = tokenizer.tokenize(tagged_text)
    # token to ids and token to segment ids
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = np.array([1] * len(indexed_tokens))
    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    # print(f'tokens_tensor: {tokens_tensor}')
    segments_tensors = torch.tensor([segments_ids])
    # print(f'segments_tensors: {segments_tensors}')

    return tokenized_text, tokens_tensor, segments_tensors


def get_bert_embeddings(_tokens_tensor, _segments_tensors, _model):
    # Gradient calculation id disabled
    # Model is in inference mode
    with torch.no_grad():
        outputs = _model(_tokens_tensor, _segments_tensors)
        print(f'outputs: \n{outputs}')
        # Removing the first hidden state
        # The first state is the input state
        hidden_states = outputs[2][1:]

    # Getting embeddings from the final BERT layer
    token_embeddings = hidden_states[-1]
    # Collapsing the tensor into 1-dimension
    token_embeddings = torch.squeeze(token_embeddings, dim=0)
    # Converting torchtensors to lists
    list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]

    return list_token_embeddings

def compute_cosine_similarity(_u, _v):
    denominator = math.sqrt(np.sum(np.array(_u) ** 2)) * math.sqrt(np.sum(np.array(_v) ** 2))
    return np.dot(_u, _v) / denominator

def align_sentences():
    return 0

"""
In this program, we are analyzing the use of the word "set"
in different sentences. The goal is to compare the usage of the word 
in the sentences using BERT embedding, and for each sentence, find 
a sample sentence where the usage of "set" is the closest. 
"""

texts = ["set",
         "On your mark, get set, go!",
         "This set of numbers has an interesting property.",
         "When I got to the party, I realized that it was all a set up.",
         "I had set the temperature higher this morning.",
         "These beautiful bowls come as a set of four.",
         "Who set the house on fire?",
         "The story is set in 1960's Paris.",
         'The word "set" has several different meanings.']

target_word_embeddings = []

# loading the pre-trained BERT model (other models: bert-base-multilingual-cased, bert-base-uncased)
model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states=True)
# loading bert tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

for text in texts:
    tokenized_text, tokens_tensor, segments_tensors = bert_text_preprocessing(text, tokenizer)
    list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model)

    # Find the position 'set' in list of tokens
    word_index = tokenized_text.index('set')
    # Get the embedding for bank
    word_embedding = list_token_embeddings[word_index]
    target_word_embeddings.append(word_embedding)

list_of_distances = []
for text1, embed1 in zip(texts, target_word_embeddings):
    print(f'\nTARGET: {text1}')
    cos_dists = np.array([])
    for text2, embed2 in zip(texts, target_word_embeddings):
        cos_dist = compute_cosine_similarity(embed1, embed2)
        list_of_distances.append([text1, text2, cos_dist])
        if text2 == text1:
            cos_dists = np.append(cos_dists, 0)
        else:
            cos_dists = np.append(cos_dists, cos_dist)
            print(f'dist: {round(cos_dist, 4)}, text: {text2}')
    print(f'best match: {texts[np.argmax(cos_dists)]}')