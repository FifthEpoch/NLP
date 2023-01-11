# Chapter 3

__3.1__ Write out the equation for trigram probability estimation (modifying Eq. 3.11). Now write out all the non-zero trigram probabilities for the I am Sam corpus on page 33.

$$ P(w_n | w_{n-2}w_{n-1}) = \frac{C(w_{n-2}w_{n-1}w_n)}{\sum_w C(w_{n-2}w_{n-1}w)} $$

---

__3.2__ Calculate the probability of the sentence i want chinese food. Give two probabilities, one using Fig. 3.2 and the ‘useful probabilities’ just below it on page 35, and another using the add-1 smoothed table in Fig. 3.7. Assume the additional add-1 smoothed probabilities 
P ( i | `<s>` ) = 0.19 and P ( `</s>` | food ) = 0.40.<br><br>

$P$(`<s>i want Chinese food</s>`)

  $= P$( i | `<s>` ) $P$( want | i ) $P$( chinese | want ) $P$( food | chinese ) $P$( `</s>` | food )
  
  $= (0.25)(0.33)(0.0065)(0.52)(0.68)$
  
  $= 0.000189618$

$P*$(`<s>I want Chinese food</s>`)

  $= P*$( i | `<s>` ) $P*$( want | i ) $P*$( chinese | want ) $P*$( food | chinese ) $P*$( `</s>` | food )
  
  $= (0.19)(0.21)(0.0029)(0.052)(0.40)$
  
  $= 0.00000240676$

---

__3.3__ Which of the two probabilities you computed in the previous exercise is higher, unsmoothed or smoothed? Explain why.<br><br>

The unsmoothed is higher. The add-one smoothing raises the probability of bigrams with an original probability of 0 while reduces the bigrams whose probability is larger than 0. Since all bigrams that appear in our sequence had a probability of larger than 0 to begin with, the overall probability of the sequence is lower after smoothing.

---

__3.4__ We are given the following corpus, modified from the one in the chapter: 
```
  <s> I am Sam </s>
  <s> Sam I am </s>
  <s> I am Sam </s>
  <s> I do not like green eggs and Sam </s>
```
Using a bigram language model with add-one smoothing, what is P( Sam | am )? Include `<s>` and `</s>` in your counts just like any other token.<br><br>

We have:

$C( Sam | am ) = 2$

$C(am) = 3$

$V$(representing total word types including `<s>` and `</s>`) $= 11$

Using Eq 3.23 on page 44:

$P_{Laplace}( Sam | am )$

  $= \frac{C(w_{n-1} w_{n}) + 1}{C(w_{n-1}) + V}$
  
  $= \frac{2+1}{3+11}$
  
  $= \frac{3}{14}$
  
---  

__3.5__ Suppose we didn’t use the end-symbol . Train an unsmoothed bigram grammar on the following training corpus without using the end-symbol: 

```
  <s> a b 
  <s> b b 
  <s> b a 
  <s> a a 
```

Demonstrate that your bigram model does not assign a single probability distribution across all sentence lengths by showing that the sum of the probability of the four possible 2 word sentences over the alphabet {a,b} is 1.0, and the sum of the probability of all possible 3 word sentences over the alphabet {a,b} is also 1.0.<br><br>

$P( a ) = \frac{1}{2}$

$P( b ) = \frac{1}{2}$

$P( b | a ) = \frac{1}{2}$

$P( a | b ) = \frac{1}{2}$

$P( a | a ) = \frac{1}{2}$

$P( b | b ) = \frac{1}{2}$

$P(ab) + P(bb) + P(ba) + P(aa)$

  $= P( a ) \cdot P( b | a ) + P( b ) \cdot P( a | b )  + P( a ) \cdot P( a | a ) + P( b ) \cdot P( b | b )$
  
  $= (\frac{1}{2} \cdot \frac{1}{2}) + (\frac{1}{2} \cdot \frac{1}{2}) + (\frac{1}{2} \cdot \frac{1}{2}) + (\frac{1}{2} \cdot \frac{1}{2})$
  
  $= \frac{1}{4} + \frac{1}{4} + \frac{1}{4} + \frac{1}{4}$
  
  $= 1$

$P(aba) + P(abb) + P(bba) + P(bbb) + P(baa) + P(bab) + P(aaa) + P(aab)$

  $= P(a) \cdot P( b | a ) \cdot  P( a | b ) + P(a) \cdot P( b | a ) \cdot P( b | b ) + P(b) \cdot P( b | b ) \cdot P( a | b ) + …$
  
  $= (\frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{2}) \cdot 8$
  
  $= \frac{1}{8} \cdot 8$
  
  $= 1$

---
  
__3.6__ Suppose we train a trigram language model with add-one smoothing on a given corpus. The corpus contains V word types. Express a formula for estimating $P( w_3 | w_1,w_2 )$, where w3 is a word which follows the bigram ( $w_1,w_2$ ), in terms of various n-gram counts and $V$. Use the notation $c( w_1,w_2,w_3 )$ to denote the number of times that trigram ( $w_1,w_2,w_3$ ) occurs in the corpus, and so on for bigrams and unigrams.<br><br>

$P( w_3 | w_1,w_2 ) = \frac{C(w_1,w_2,w_3) + 1}{C(w_1,w_2) + V}$

---
  
__3.7__ We are given the following corpus, modified from the one in the chapter: 

```
  <s> I am Sam </s>
  <s> Sam I am </s>
  <s> I am Sam </s>
  <s> I do not like green eggs and Sam </s>
```

If we use linear interpolation smoothing between a maximum-likelihood bigram model and a maximum-likelihood unigram model with $\Lambda_1 = \frac{1}{2}$ and $\Lambda_2 = \frac{1}{2}$, what is $P( Sam | am )$? Include `<s>` and `</s>` in your counts just like any other token.<br><br>

$P_{Linear Interpolation}( Sam | am )$

$= \Lambda_1 P( Sam ) + \Lambda_2 P( Sam | am )$

$= \frac{1}{2} \cdot \frac{4}{25} + \frac{1}{2} \cdot \frac{2}{4}$

$= 0.33$
 
---
  
__3.8__ Write a program to compute unsmoothed unigrams and bigrams.

See unsmoothed-unigram-n-bigram.py
  
---
  
__3.9__ Run your n-gram program on two different small corpora of your choice (you might use email text or newsgroups). Now compare the statistics of the two corpora. What are the differences in the most common unigrams between the two? How about interesting differences in bigrams?<br><br>
  
The unigram for both small corpus are consist of start of sentence mark `<s>` and end of sentence mark `</s>`, and conjunctions and prepositions. 

The highest frequency word pair in the bigrams of the news article and the bigram of the email is `</s>` `<s>`, this is because the end of a sentence is usually followed by the beginning of another sentence. 

Other than that, the two bigrams differ quite a bit. We observe that there is a significant difference in vocabularies (primarily in adjectives and nouns) between the two corpus.

--- 

__3.10__ Add an option to your program to generate random sentences.
  
See generate-sentence-from-corpus.py

Sample generated using corpora/email.txt:
 
`<s> This is what we mean by educational materials that support faculty and learning in improving access the sciences </s>`

--- 

__3.11__ Add an option to your program to compute the perplexity of a test set.

See generate-sentence-from-corpus.py

--- 

__3.12__ You are given a training set of 100 numbers that consists of 91 zeros and 1 each of the other digits 1-9. Now we see the following test set: 0 0 0 0 0 3 0 0 0 0. What is the unigram perplexity?<br><br>
  
We’ll use Eq 3.15 to calculate perplexity. In our case: 

$N = 10$ for this test set

$P(0) = \frac{91}{100}$

$P(3) = \frac{1}{100}$
  
We first calculate the product of all probabilities inside of the root. We will inverse it after finding the product. Let this product be S. 

$S = P(0) * P(00) * P(000) * P(0000) * P(00000) * P(000003) * P(0000030) * P(00000300) * P(000003000) * P(0000030000)$
  
  $= (\frac{91}{100}) \cdot (\frac{91}{100})^2 \cdot (\frac{91}{100})^3 \cdot (\frac{91}{100})^4 \cdot (\frac{91}{100})^5 \cdot (\frac{91}{100})^5 (\frac{1}{100}) \cdot (\frac{91}{100})^6 (\frac{1}{100}) \cdot (\frac{91}{100})^7 (\frac{1}{100}) \cdot (\frac{91}{100})^8 (1/100) \cdot (\frac{91}{100})^9 (\frac{1}{100})$
   
   $= (\frac{91}{100})^{50} (\frac{1}{100})^5$
   
   $= 8.955083\times10^{13}$

$PP(0000030000)$
   
   $= (\frac{1}{S})^{-\frac{1}{N}}$

   $= \frac{1}{8.955083\times10^{13}}^{-\frac{1}{10}}$

   $= 0.0624032145$

   $≈ 0.062$
