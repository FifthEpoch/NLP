# Chapter 2

__2.1__ Write regular expressions for the following languages.

I. the set of all alphabetic strings; 

```
\w+/
```

II. the set of all lower case alphabetic strings ending in a b; 

```
[a-z]*b
```

III. the set of all strings from the alphabet a,b such that each a is immediately preceded by and immediately followed by a b;
```
(b[ab]b)+
```

---

__2.2__ Write regular expressions for the following languages. By “word”, we mean an alphabetic string separated from other words by whitespace, any relevant punctuation, line breaks, and so forth.

I. the set of all strings with two consecutive repeated words (e.g., “Humbert Humbert” and “the the” but not “the bug” or “the big bug”); 

```
(.*) \1
```

II. all strings that start at the beginning of the line with an integer and that end at the end of the line with a word; 

```
^(\d)+.*(\w)+$
```

III. all strings that have both the word grotto and the word raven in them (but not, e.g., words like grottos that merely contain the word grotto); 

```
(?:^|.*)([Gg]rotto|[Rr]aven).*(?! \1)(grotto|raven)
```

IV. write a pattern that places the first word of an English sentence in a register. Deal with punctuation.

```
^(\w)+(?= [\s\W])
```

---

__2.3__ Implement an ELIZA-like program, using substitutions such as those described
on page 11. You might want to choose a different domain than a Rogerian psychologist, although keep in mind that you would need a domain in which your
program can legitimately engage in a lot of simple repetition.

See ELIZA-esque.py

---

__2.4__ Compute the edit distance (using insertion cost 1, deletion cost 1, substitution cost 1) of “leda” to “deal”. Show your work (using the edit distance grid).

```
leda
deal
s di
```

Edit distance is 3 since s costs 1, i costs 1, and d costs 1.

---

__2.5__ Figure out whether drive is closer to brief or to divers and what the edit distance is to each. You may use any version of distance that you like.

Insertion cost 1, deletion cost 1, substitution cost 2.

```
drive
brief
s  di
```
Edit distance is 4.

```
drive
divers
 d  ii
```
Edit distance is 3.

---

__2.6__ Now implement a minimum edit distance algorithm and use your hand-computed
results to check your code.

See min-edit-distance.py


