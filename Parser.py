import pandas as pd
from tokenizer import Tokenizer
import treelib
df = pd.read_csv("Parsetable.csv", index_col=0).T
firfol = pd.read_csv('First Follows.csv', index_col='Nonterminal').T
firfol = firfol.fillna('none')
df = df.fillna('none')
# print(df.columns)
# print(firfol.head())
# code testing


############
for ind in firfol.columns:
    for fol in firfol[ind]['Follow'].split(","):
        fol = fol.replace(' ', '')
        if ind != 'none' and fol != 'none' and len(fol) != 0:
            if df[ind][fol] == 'none':
                df[ind][fol] = 'synch'
                #print(ind, fol)


def errorprinter(dat, inp):
    lis = []
    for col in df.index:
        if df[dat][col] != 'none' and df[dat][col] != 'synch':
            lis.append(col)
    st = ''
    for l in lis:
        st += (', '+l)
    st = st[2:]
    print('Expected one among :' + st + ' encountered '+inp)

def printTree(tree):
    print("--------------------TREE--------------------")
    print()

    for key in tree.keys():
        print(key, " : ", tree[key])

    # plot_tree = treelib.Tree()
    # plot_tree.create_node("S", 0)
    # for key in tree.keys():
    #     print("key = ", key)
    #     if key[0] == 0:
    #         continue
    #     for child in tree[key]:
    #         plot_tree.create_node(child[1], child[0], parent=key[0])

    # plot_tree.show()

    print()
    print("--------------------------------------------")



my_tokenizer = Tokenizer('input.txt')
stack = []
finalinp = 0
nont = ['id', 'integer_literal', 'string_literal', 'float_literal', 'true', 'false', 'relop_eq', 'relop_eq',
        'relop_le', 'relop_lt', 'relop_ne', 'relop_ge', 'relop_gt', 'logical_and', 'logical_or', 'op_not']
stack.append('S')

tree = { }
key = 0
while len(stack) != 0 and finalinp == 0:
    # Getting next token from input file until we hit EOF
    flag = 0
    token = my_tokenizer.get_next_token()
    inp = ''
    if token.token == "string_error" or token.token == "char_error" or token.token == "float_error" or token.token == "Invalid_Token":
        print("[-] Lexical error encountered : " + token.lexeme + " at line " +
              str(token.line) + " between position "+str(token.begin)+" - "+str(token.end))
        continue
    if token.token == "EOF":
        inp = '$'
        finalinp = 1

    elif token.token in nont:
        inp = token.token
    else:
        inp = token.lexeme
    print()
    print("inp : ", inp)
    if stack[-1] == inp:
        print('stack : ', stack)
        print("Matched : "+inp)

    while len(stack) != 0 and stack[-1] != inp and flag == 0:
        print('stack : ', stack)
        if stack[-1] not in df.columns:
            print('[-] Syntax error : expected ', stack[-1], 'got ', inp)
            stack.pop()
            continue
        rule = df[stack[-1]][inp]
        #print('rule  : ', rule)
        if rule == 'none':
            flag = 1
            print(
                '[-] Syntax error : error detected on line ' + str(token.line) + ' at position ' + str(token.begin)+'.')
            errorprinter(stack[-1], inp)
            break
        elif rule == 'synch':
            print(
                '[-] Syntax error : error detected on line ' + str(token.line) + ' at position ' + str(token.begin)+'.')
            errorprinter(stack[-1], inp)
            stack.pop()
            continue
        stack.pop()
        rule_lhs = (rule.split("::="))[0]
        rule_lhs = ' '.join(rule_lhs.split())
        print("rule_lhs = '" + rule_lhs + "'")
        rule = (rule.split("::="))[-1]
        rule = ' '.join(rule.split())
        rule = rule.split(' ')
    
        # print(rule)
        for r in reversed(rule):
            if r != 'ε':
                stack.append(r)
            
        tree[(key, rule_lhs)] = []
        oldkey = key
        for r in rule:
            key += 1
            tree[(oldkey, rule_lhs)].append((key, r))
        
        if stack[-1] == inp:
            print('stack : ', stack)
            print("Matched : "+inp)
    if flag == 0 and len(stack) != 0:
        stack.pop()
print()
print("**** PARSING COMPLETED ****")
print()
printTree(tree)

#print('Parsing aborted')
