import re
import csv
import math
import nltk
nltk.download('brown')
nltk.download('movie_reviews')
from nltk.corpus import brown, movie_reviews
from nltk.tokenize import word_tokenize

def get_top_250_list():
    titles = []
    with open("./data/IMDB-top-250.txt") as file:
        for line in file:
            words = line.split()
            title = ""
            for i in range(len(words)):
                if re.match(r'[0-9]\.[0-9]', words[i]):
                    for j in range(i + 1, len(words) - 1):
                        title += words[j] + " "
                    break
            titles.append(title.strip())
    return titles

def get_top_397_list():
    with open("./data/IMDB-top-397.csv", 'r') as file:
        csvreader = csv.reader(file)
        collected_titles = []
        for row in csvreader:
            raw_title = row[1].split(" ")
            title = ""
            for i in range(1, len(raw_title) - 1):
                title += raw_title[i] + " "
            if title.strip() not in collected_titles:
                collected_titles.append(title.strip())
    return collected_titles[1:]

def get_top_1000_list():
    with open("./data/IMDB-top-1000.csv", 'r') as file:
        csvreader = csv.reader(file)
        collected_titles = []
        for row in csvreader:
            raw_title = row[1].strip()
            # so that no duplicates is collected
            if raw_title not in collected_titles:
                collected_titles.append(raw_title.split())
    return collected_titles[1:]

def get_data_from_file(_fn):
    with open(_fn, 'r') as file:
        data = file.read().replace('\n', ' ')
    return data

def label_BIO(_tokens, _NE):
    # MOV: movie title
    # beginning of a movie title is tagged with "B-MOV"
    # middle/end of a movie title is tagged "I-MOV"

    BIO_for_samples = []
    sample_size = len(_tokens)

    current_i = 0

    # search through each sample
    for i in range(sample_size):

        if i != current_i: continue

        # search each named entity for each sample
        has_match = False
        match_index = -1
        for j in range(len(_NE)):

            # if the first word is a match
            if _NE[j][0] == _tokens[i]:

                # if the matched movie title does not
                # exceed the length of the sample
                if i + len(_NE[j]) < sample_size:

                    # check if all other components match
                    no_match = False
                    for k in range(1, len(_NE[j])):
                        if _NE[j][k] != _tokens[i + k]:
                            no_match = True
                            break

                    # full match found
                    if not no_match:
                        has_match = True
                        match_index = j
                        break

        # Done searching through the Named Entity List
        if has_match:
            BIO_for_samples.append((_tokens[i], 'B-MOV'))
            for j in range(1, len(_NE[match_index])):
                BIO_for_samples.append((_tokens[i + j], 'I-MOV'))
            current_i += len(_NE[match_index])
        else:
            BIO_for_samples.append((_tokens[i], 'O'))
            current_i += 1

    return BIO_for_samples

def print_BIO_res(_BIO):
    for i in range(len(_BIO)):
        if _BIO[i][1] == 'B-MOV':
            for j in range(i - 7, i + 7):
                if _BIO[j][1] == 'O':
                    print(_BIO[j][0], end=" ")
                else:
                    print(_BIO[j], end=" ")
            print("")

if __name__ == "__main__":

    # all lists from IMDB
    titles_top_250 = get_top_250_list()
    titles_top_397 = get_top_397_list()
    titles_top_1000 = get_top_1000_list()

    # uncomment for movie reviews resources
    # review_file_ids = movie_reviews.fileids()
    # REVIEWS = movie_reviews.raw(review_file_ids[2])

    # get text data from a text file
    data = get_data_from_file("data/article-about-a-genre.txt")
    # tokenize text data
    tokens = word_tokenize(data)
    # tag with BIO using the IMDB top 1000 movie title list
    BIO = label_BIO(tokens, titles_top_1000)

    # B-MOV marks the beginning of a known movie title
    # I-MOV marks the middle/end of a known movie title
    # O for all other words
    print_BIO_res(BIO)
