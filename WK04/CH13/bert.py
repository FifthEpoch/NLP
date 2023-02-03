from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import torch
import math
from scipy.spatial.distance import cosine

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
    denominator = math.sqrt(np.sum(_u ** 2)) * math.sqrt(np.sum(_v ** 2))
    return np.dot(_u, _v) / denominator

def align_sentences():
    return 0

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

# loading the pre-trained BERT model
model = BertModel.from_pretrained('bert-base-uncased',output_hidden_states = True)
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
    print(f'TARGET: {text1}')
    for text2, embed2 in zip(texts, target_word_embeddings):

        cos_dist = 1 - cosine(embed1, embed2)
        list_of_distances.append([text1, text2, cos_dist])
        print(f'CANDIDATE: {text2}, dist={cos_dist}')

distances_df = pd.DataFrame(list_of_distances, columns=['text1', 'text2', 'distance'])