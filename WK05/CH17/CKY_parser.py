import re

def convert_to_CNF_grammar(_filename):
    """
    1. Copy all conforming rules to the new grammar unchanged.
    2. Convert terminals within rules to dummy non-terminals.
    3. Convert unit productions.
    4. Make all rules binary and add them to new grammar.

    :param _filename: path to Context-Free Grammar (CFG) file to be parsed
    :return: dictionary of CFG in Chomsky Normal Form (CNF)
    """
    grammar = {}
    new_sym_index = 0
    for line in open(_filename, 'r').readlines():

        line = line.strip()
        words = re.split(' -> |\s', line)
        print(words)

        # save the original grammar first before dealing with
        # the LHS restrictions in CNF conversion
        if len(words) > 3:
            temp_list = []
            for i in range(1, len(words)):
                temp_list.append(words[i])
            if words[0] in grammar:
                grammar[words[0]].append(temp_list)
            else:
                grammar.update({words[0]: [temp_list]})

        # substitute with new symbol until there are
        # less than 3 things on the RHS
        while len(words) > 3:
            matched = False
            key = 'NULL'
            for LHS, RHS in grammar.items():
                for item in RHS:
                    if item == [words[1], words[2]]:
                        matched = True
                        key = LHS

            if not matched:
                key = f'X{new_sym_index}'
                grammar.update({key: [[words[1], words[2]]]})
                new_sym_index+=1

            del words[1]
            words[1] = key

        # save the grammar that either has 1 or 2 item(s) on the RHS
        temp_list = [words[1], words[2]] if len(words) == 3 else [words[1]]
        if words[0] in grammar:
            grammar[words[0]].append(temp_list)
        else:
            grammar.update({words[0]: [temp_list]})

        # new we search for any derivative

    return grammar

def CKY_parse(_text, _grammar):
    # QUESTION: do we pass the text in as
    # <s> Book a flight to Boston
    # OR
    # Book a flight to Boston
    table = [[[] for i in range(len(_text)+1)] for j in range(len(_text)+1)]
    for j in range(1, len(_text)):
        for LHS, RHS in _grammar.items():
            if RHS == _text[j]:
                table[j-1][j].append(LHS)
        for i in reversed(range(j-3)):   # from j-2 down to 0
            if i < 0: continue # skip if out of bound
            for k in (i+1, j-2):
                # loop through all possible POS collected for current cell[j-1, j]
                for m in range(len(table[j-1][j])):
                    key = table[j-1][j][m]
                    if key in _grammar:
                        for item in _grammar[key]:
                            if len(item) > 1:
                                if item[0] in table[i][k] and item[1] in table[k][j]:
                                    table[i][j].append(key)
    return table














filename = "L1_grammar.txt"
grammar_CNF = convert_to_CNF_grammar(filename)
print(grammar_CNF)