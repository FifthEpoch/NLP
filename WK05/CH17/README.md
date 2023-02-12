# Chapter 17

__17.1__ Implement the algorithm to convert arbitrary context-free grammars to CNF. Apply your program to the L1 grammar.

See ```CKY_parser.py```

__17.2__ Implement the CKY algorithm and test it with your converted L1 grammar.

See ```CKY_parser.py```

__17.3__ Rewrite the CKY algorithm given in Fig. 17.12 on page 370 so that it can accept grammars that contain unit productions.

__17.4__ Discuss how to augment a parser to deal with input that may be incorrect, for example, containing spelling errors or mistakes arising from automatic speech recognition.

For words that cannot be matched in our lexicon, perhaps we can examine the smallest distance between the unknown word to the words in our lexicon to see how likely that it is a typo. 

__17.5__ Implement the PARSEVAL metrics described in Section 17.8. Next, use a parser and a treebank, compare your metrics against a standard implementation. Analyze the errors in your approach.
