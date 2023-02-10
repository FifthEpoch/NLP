import re
import pprint

def convert_to_CNF_grammar(_grammar_filename, _lexicon_filename):
    """
    1. Copy all conforming rules to the new grammar unchanged.
    2. Convert terminals within rules to dummy non-terminals.
    3. Convert unit productions.
    4. Make all rules binary and add them to new grammar.

    :param _grammar_filename: path to Context-Free Grammar (CFG) file to be parsed
    :return: dictionary of CFG in Chomsky Normal Form (CNF)
    """
    grammar = {}
    new_sym_index = 0
    for line in open(_grammar_filename, 'r').readlines():

        line = line.strip()
        words = re.split(' -> |\s', line)

        # save the original grammar first before dealing with
        # the LHS restrictions in CNF conversion
        if len(words) > 3:

            temp_list = words[1:]

            if words[0] in grammar:
                grammar[words[0]].append(temp_list)
            else:
                grammar.update({words[0]: [temp_list]})

        # substitute with new symbol until there are
        # less than 3 things on the RHS
        while len(words) > 3:

            matched = False
            key = ''

            for LHS, RHS in grammar.items():
                for item in RHS:
                    if item == [words[1], words[2]]:
                        matched = True
                        key = LHS

            if not matched:
                key = f'X{new_sym_index}'
                grammar.update({key: [[words[1], words[2]]]})
                new_sym_index += 1

            del words[1]
            words[1] = key

        # save the grammar that either has 1 or 2 item(s) on the RHS
        temp_list = words[1:]
        if words[0] in grammar:
            grammar[words[0]].append(temp_list)
        else:
            grammar.update({words[0]: [temp_list]})

    # retrieve lexicon
    lexicon = {}
    for line in open(_lexicon_filename, 'r').readlines():
        line = line.strip()
        words = re.split(' -> | / ', line)
        lexicon.update({words[0]: [[words[1]]]})
        grammar.update({words[0]: [[words[1]]]})
        for l in range(2, len(words)):
            lexicon[words[0]].append([words[l]])
            grammar[words[0]].append([words[l]])

    # get rid of unit productions
    for key in grammar.copy():

        for i in range(len(grammar[key])):

            # find all unit production
            if len(grammar[key][i]) == 1:

                # extracting the RHS string of the unit production
                current_RHS = grammar[key][i][0]

                if not current_RHS.isupper() \
                        or current_RHS not in grammar:

                    search_LHS = key
                    matched = True
                    while matched:
                        matched = False
                        for k, v in grammar.items():
                            for n in range(len(v)):
                                if len(v[n]) == 1 and v[n][0] == search_LHS:
                                    matched = True
                                    search_LHS = k
                                    if [current_RHS] not in grammar[search_LHS]:
                                        grammar[search_LHS].append([current_RHS])
                    continue

                # loop through all LHS matches for the current RHS string
                for j in range(len(grammar[current_RHS])):

                    temp_list = grammar[current_RHS][j].copy()

                    while len(temp_list) > 2:

                        temp_key = f'X{new_sym_index}'
                        grammar.update({temp_key: [temp_list[:2]]})
                        new_sym_index += 1

                        del temp_list[0]
                        temp_list[0] = temp_key

                    if len(temp_list) == 2:
                        if temp_list not in grammar[key]:
                            grammar[key].append(temp_list)
                    elif len(temp_list) == 1: # another unit production

                        search_RHS = current_RHS
                        while search_RHS not in lexicon.keys() and search_RHS in grammar:
                            for k in range(len(grammar[search_RHS])):
                                if len(grammar[search_RHS][k]) == 1:
                                    search_RHS = grammar[search_RHS][k][0]
                                    break

    return grammar


def retrieve_lexicon(_filename):
    lexicon = {}
    for line in open(_filename, 'r').readlines():
        line = line.strip()
        words = re.split(' -> | \| ', line)
        lexicon.update({words[0]: words[1:]})
    return lexicon

def CKY_parse(_text, _grammar):

    table = [[[] for i in range(len(_text)+1)] for j in range(len(_text)+1)]

    for j in range(1, len(_text)):

        print(f'j: {j}')

        for LHS, RHS in _grammar.items():
            for m in range(len(RHS)):
                if RHS[m][0] == _text[j]:
                    table[j-1][j].append(LHS)

        for i in reversed(range(j-1)):   # from j-2 down to 0
            print(f'i: {i}')
            # if i < 0: continue; skip if out of bound
            for k in (i+1, j-2):
                print(f'k: {k}')
                # loop through all possible POS collected for current cell[j-1, j]
                B = table[i][k]
                C = table[k][j]
                print(f'B: {B}, C: {C}')

                for LHS, RHS in _grammar.items():
                    for item in RHS:
                        for m in range(len(B)):
                            for n in range(len(C)):
                                print(f'item: {item}, B[m], C[n]: {[B[m], C[n]]}')
                                if item == [B[m], C[n]]:
                                    print('matched!')
                                    if LHS not in table[i][j]:
                                        table[i][j].append(LHS)

    return table

def computer_PARSEVAL():
    return 0

grammar_filename = "L1_grammar.txt"
lexicon_filename = "lexicon.txt"
grammar_CNF = convert_to_CNF_grammar(grammar_filename, lexicon_filename)
print('Chomsky Normal Form Grammar:')
pprint_var = pprint.pprint(grammar_CNF)

text = ['S', 'book', 'the', 'flight', 'through', 'Houston']
grammar_table = CKY_parse(text, grammar_CNF)

print('\ngrammar_table: ')
for row in range(len(grammar_table)):
    print(grammar_table[row])

# uncomment to store lexicon in dictionary
# lexicon = retrieve_lexicon(lexicon_filename)