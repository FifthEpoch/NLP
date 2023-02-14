# Chapter 23: Words Senses and WordNet

__23.1__ Collect a small corpus of example sentences of varying lengths from any
newspaper or magazine. Using WordNet or any standard dictionary, determine how many senses there are for each of the open-class words in each sentence. How many distinct combinations of senses are there for each sentence? How does this number seem to vary with sentence length?

The longer a sentence, the more likely it will have a larger number of unique combination of senses. See ```wordnet.py``` for calculation. 

*Corpus collected from [Quanta Magazine](https://www.quantamagazine.org/researchers-discover-a-more-flexible-approach-to-machine-learning-20230207/)

__23.2__ Using WordNet or a standard reference dictionary, tag each open-class word in your corpus with its correct tag. Was choosing the correct sense always a straightforward task? Report on any difficulties you encountered.

Here are a sentences from ```small-corpus.txt``` which I have tagged by hand. 

"Researchers Discover a More Flexible Approach to Machine Learning"

```
Researchers:   a scientist who devotes himself to doing research
Discover:      discover or determine the existence, presence, or fact of
a:             none of the definitions were correct for this usage of "a"
More:          used to form the comparative of some adjectives and adverbs
Flexible:      able to adjust readily to different conditions
Approach:      ideas or actions intended to deal with a problem or situation
to:            returned nothing from WordNet
Machine:       any mechanical or electrical device that transmits or modifies energy to perform or assist in the performance of human tasks
Leanring:      gain knowledge or skills
```

There are several difficulties in disambiguating word senses by hand.
1. More than one sense can be applied to a particular use case since some of the senses only differ slightly. For example, all 3 of the senses of the word "Discovers" can be applied to this specific use case and they are all correct:
    * Synset('detect.v.01'): discover or determine the existence, presence, or fact of
    * Synset('discover.v.03'): make a discovery, make a new finding
    * Synset('discover.v.04'): make a discovery
2. There is a chance that none of the senses returned from WordNet for a word is correctly for how the word is used in the use case. For example, the word "a" returns an array of senses where a is used as a noun, for example:
   * Synset('angstrom.n.01'): a metric unit of length equal to one ten billionth of a meter (or 0.0001 micron); used to specify wavelengths of electromagnetic radiation
   * Synset('adenine.n.01'): (biochemistry) purine base found in DNA and RNA; pairs with thymine in DNA and with uracil in RNA
   * Synset('a.n.06'): the 1st letter of the Roman alphabet
   None of these corresponds to our use case where "a" is used as a determinant.
3. There is a chance that nothing will return even given a valid word. This is the case for the word "to" in our example sentence. This could be due to 2 reasons:
   * The word belongs to a word class is neither noun, verb, or adverb/adjective, which are the only classes covered by WordNet
   * The word belongs to the classes covered by WordNet but was not documented by it
   We will have to come up with some way to differentiate between the two possibilities for a given word to process it further.

__23.3__ Using your favorite dictionary, simulate the original Lesk word overlap disambiguation algorithm described on page 469 on the phrase Time flies like an arrow. Assume that the words are to be disambiguated one at a time, from left to right, and that the results from earlier decisions are used later in the process.


/// WIP



__23.4__ 

See ```wordnet.py``` for calculation. 

Here shows the result of lesk algorithm on "Time flies like an arrow".
```
Time flies like an arrow

Time:          adjust so that a force is applied and an action occurs at the desired time
flies:         hit a fly
like:          equal in amount or value
an:            an associate degree in nursing
arrow:         a projectile with a straight thin shaft and an arrowhead on one end and stabilizing vanes on the other; intended to be shot from a bow
```

Below shows the result of the lesk algorithm for the same sentence used in __23.2__:
```
Researchers Discover a More Flexible Approach to Machine Learning

Researchers:   a scientist who devotes himself to doing research
Discover:      discover or determine the existence, presence, or fact of
a:             the blood group whose red cells carry the A antigen
More:          English statesman who opposed Henry VIII's divorce from Catherine of Aragon and was imprisoned and beheaded; recalled for his concept of Utopia, the ideal state
Flexible:      capable of being changed
Approach:      ideas or actions intended to deal with a problem or situation
to:            word sense not found
Machine:       any mechanical or electrical device that transmits or modifies energy to perform or assist in the performance of human tasks
Learning:      the cognitive process of acquiring skill or knowledge
```