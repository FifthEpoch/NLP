# Chapter 8

__8.1__ Find one tagging error in each of the following sentences that are tagged with the Penn Treebank tagset:

1. ```I/PRP need/VBP a/DT flight/NN from/IN Atlanta/NN```


    ```Atlanta/NN``` -> ```Atlanta/NNP```


2. ```Does/VBZ this/DT flight/NN serve/VB dinner/NNS```


    ```dinner/NNS``` -> ```dinner/NN```


3. ```I/PRP have/VB a/DT friend/NN living/VBG in/IN Denver/NNP```


    ```have/VB``` -> ```have\VBP```


4. ```Can/VBP you/PRP list/VB the/DT nonstop/JJ afternoon/NN flights/NNS```


    ```afternoon/NN``` -> ```afternoon/JJ```



__8.2__ Use the Penn Treebank tagset to tag each word in the following sentences from Damon Runyon’s short stories. You may ignore punctuation. Some of these are quite difficult; do your best.

1. It is a nice night.


    ```It/PRP is/VBZ a/DT nice/JJ night/NN```


2. This crap game is over a garage in Fifty-second Street. . .


    ```This/DT crap/JJ game/NN is/VBZ over/RP a/DT garage/NN in/IN (Fifty-second Street)/NNP```


3. . . . Nobody ever takes the newspapers she sells . . .


    ```Nobody/PRP ever/RB takes/VBZ the/DT newspapers/NNS she/PRP sells/VBZ```


4. He is a tall, skinny guy with a long, sad, mean-looking kisser, and a mournful voice.


    ```He/PRP is/VBZ a/DT tall/JJ skinny/JJ guy/NN with/IN a/DT long/JJ sad/JJ mean-looking/JJ kisser/NN and/CC a/DT mournful/JJ voice/NN```


5. . . . I am sitting in Mindy’s restaurant putting on the gefillte fish, which is a dish I am very fond of, . . .


    ```I/PRP am/VB sitting/VBG in/IN Mindy/NNP 's/POS restaurant/NN putting/VBG on/RP the/DT (gefillte fish)/NNP which/WDT is/VBZ a/DT dish/NN I/PRP am/VB very/RB fond/JJ of/IN```


6. When a guy and a doll get to taking peeks back and forth at each other, why there you are indeed.


    ```When/WP a/DT guy/NN and/CC a/DT doll/NN get/VBP to/TO taking/VBG peeks/NNS back/RB and/CC forth/RB at/RP (each other)/PRP why/UH there/EX you/PRP are/VBP indeed/RB```


__8.3__ Now compare your tags from the previous exercise with one or two friend’s answers. On which words did you disagree the most? Why?

I have no friends.

__8.4__ Implement the “most likely tag” baseline. Find a POS-tagged training set, and use it to compute for each word the tag that maximizes $p(t|w)$. You will need to implement a simple tokenizer to deal with sentence boundaries. Start by assuming that all unknown words are NN and compute your error rate on known and unknown words. Now write at least five rules to do a better job of tagging unknown words, and show the difference in error rates.

See ```most-frequent-class-baseline.py```

```
Assuming that all unknown words are NN
>> accuracy: 0.8184096423883209
With additional rules for unknown words
>> accuracy: 0.8638370659135208
1142 more words got correctly classified.
```

__8.5__ Build a bigram HMM tagger. You will need a part-of-speech-tagged corpus. First split the corpus into a training set and test set. From the labeled training set, train the transition and observation probabilities of the HMM tagger directly on the hand-tagged data. Then implement the Viterbi algorithm so you can decode a test sentence. Now run your algorithm on the test set. Report its error rate and compare its performance to the most frequent tag baseline.

See ```viterbi.py```

Bigram HMM tagger predicted tags with a 0.9175782648474482 accuracy, outperforming the “most likely tag” baseline method.

__8.6__ Do an error analysis of your tagger. Build a confusion matrix and investigate the most frequent errors. Propose some features for improving the performance of your tagger on these errors.

```
Tag with the most false positives is: NOUN with 819 counts.
Tag with the most false negative is:  ADJ with 588 counts.

model got 23067 samples correct out of 25139
accuracy: 0.9175782648474482
```

__8.7__ Develop a set of regular expressions to recognize the character shape features described on page 176.

X. X. X. (e.g. I.M.F.) -> ```/([A-Z]\.( )?)+/```

XXdd-dd (e.g. DC10-30) -> ```/[A-Z]{1, 6}[0-9][0-9](-|_)[0-9][0-9]/```


__8.8__ The BIO and other labeling schemes given in this chapter aren’t the only possible one. For example, the B tag can be reserved only for those situations where an ambiguity exists between adjacent entities. Propose a new set of BIO tags for use with your NER system. Experiment with it and compare its performance with the schemes presented in this chapter.

| tag      | meaning|
|----------|--------|
| S-PER    |Start of a person's name|
| I-PER    |Part of a person's name or end of a person's name|
| B-PER    |Start of a person's name but the named entity also appears under a different named entity category|


__8.9__ Names of works of art (books, movies, video games, etc.) are quite different from the kinds of named entities we’ve discussed in this chapter. Collect a list of names of works of art from a particular category from a Web-based source (e.g., gutenberg.org, amazon.com, imdb.com, etc.). Analyze your list and give examples of ways that the names in it are likely to be problematic for the techniques described in this chapter.

For this assignment I collected the top 1000 movie titles from IMDB. There are several details related to the movie title named entity that might be ambiguous for a named entity tagging task: 

1. A lot of movies are based on novels, such as The Wolf of Wall Street, V for Vendetta, Gone Girl, and Harry Potter and the Deathly Hallows. 
2. Movies about a famous person is often titled with just the person's name (e.g. Hamilton, Andrei Rublev, Ip Man, JFK). Similarly, some movies are titled after the main fictional character it portrays (e.g. Forrest Gump, Joker, Princess Mononoke, Amélie)
3. Other ambiguity might be 1917 which is a movie but also a year; the movie Central Station where the title is also a location; the movie Bohemian Rhapsody which is also the title to a very popular song; the movie Brazil which is a location and a geo-political entity.

__8.10__ Develop an NER system specific to the category of names that you collected in the last exercise. Evaluate your system on a collection of text likely to contain instances of these named entities.

See ```NER-movie-titles.py```


### Additional Question in the Chapter

__Q1__ Use the sample probabilities in Fig. 8.8a (with $\Pi(\text{hot}, \text{cold}, \text{warm}) = [0.1,0.7,0.2]$)
to compute the probability of each of the following sequences:

$P(\text{hot}|\text{hot}) = 0.6$; $P(\text{cold}|\text{hot}) = 0.1$; $P(\text{warm}|\text{hot}) = 0.3$;

$P(\text{hot}|\text{cold}) = 0.1$; $P(\text{cold}|\text{cold}) = 0.8$; $P(\text{warm}|\text{cold}) = 0.1$;

$P(\text{hot}|\text{warm}) = 0.3$; $P(\text{cold}|\text{warm}) = 0.1$; $P(\text{warm}|\text{warm}) = 0.6$;

(8.4) hot hot hot hot

$\text{Probability} = 0.1 \times 0.6 \times 0.6 \times 0.6 = 0.0216$

(8.5) cold hot cold hot

$\text{Probability} = 0.7 \times 0.1 \times 0.1 \times 0.1 = 0.0007$


__Q2__ What does the difference in these probabilities tell you about a real-world weather
fact encoded in Fig. 8.8a?

It is more likely for a particular temperature to persist than to swing to the other extreme. 




