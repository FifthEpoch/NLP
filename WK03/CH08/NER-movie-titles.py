import re
import csv
def get_top_250_list():
    titles = []
    with open("./movie-titles/IMDB-top-250.txt") as file:
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
    with open("movie-titles/IMDB-top-397.csv", 'r') as file:
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
    with open("movie-titles/IMDB-top-1000.csv", 'r') as file:
        csvreader = csv.reader(file)
        collected_titles = []
        for row in csvreader:
            raw_title = row[1].strip()
            # so that no duplicates is collected
            if raw_title not in collected_titles:
                collected_titles.append(raw_title)
                print(raw_title)
    return collected_titles[1:]

if __name__ == "__main__":
    titles_top_250 = get_top_250_list()
    titles_top_397 = get_top_397_list()
    titles_top_1000 = get_top_1000_list()
