import pandas as pd
from tokenizer import Tokenizer
df = pd.read_csv("Parsetable.csv", index_col=0).T
firfol = pd.read_csv('First Follows.csv', index_col='Nonterminal').T
firfol = firfol.fillna('none')
df = df.fillna('none')
# print(df.columns)
# print(firfol.head())
# code testing
for ind in firfol.columns:
    for fol in firfol[ind]['Follow'].split(","):
        fol = fol.replace(' ', '')
        if ind != 'none' and fol != 'none' and len(fol) != 0:
            if df[ind][fol] == 'none':
                df[ind][fol] = 'synch'
                #print(ind, fol)

######
my_tokenizer = Tokenizer('input.txt')
stack = []
finalinp = 0
nont = ['id', 'integer_literal', 'string_literal', 'float_literal', 'true', 'false', 'relop_eq', 'relop_eq',
        'relop_le', 'relop_lt', 'relop_ne', 'relop_ge', 'relop_gt', 'logical_and', 'logical_or', 'op_not']
stack.append('S')
while len(stack) != 0 and finalinp == 0:
    # Getting next token from input file until we hit EOF
    flag = 0
    token = my_tokenizer.get_next_token()
    inp = ''
    if token.token == "EOF":
        inp = '$'
        finalinp = 1

    elif token.token in nont:
        inp = token.token
    else:
        inp = token.lexeme
    print("inp : ", inp)
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
                '[-] Syntax error : error detected on ' + str(token.line) + '.')
            break
        elif rule == 'synch':
            print(
                '[-] Syntax error : error detected on ' + str(token.line) + '.')
            stack.pop()
            continue
        stack.pop()
        rule = (rule.split("::="))[-1]
        rule = ' '.join(rule.split())
        rule = rule.split(' ')
        # print(rule)
        for r in reversed(rule):
            if r != 'ε':
                stack.append(r)
    if flag == 0 and len(stack) != 0:
        stack.pop()

print("Parsing successful")

#print('Parsing aborted')
