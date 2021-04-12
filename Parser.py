import pandas as pd
from tokenizer import Tokenizer
df = pd.read_csv("Parsetable.csv", index_col=0).T
df = df.fillna('none')
my_tokenizer = Tokenizer('input.txt')
stack = []
nont = ['id', 'integer_literal', 'string_literal', 'float_literal', 'true', 'false', 'relop_eq', 'relop_eq',
        'relop_le', 'relop_lt', 'relop_ne', 'relop_ge', 'relop_gt', 'logical_and', 'logical_or', 'op_not']
stack.append('S')
while len(stack) != 0:
    # Getting next token from input file until we hit EOF

    token = my_tokenizer.get_next_token()
    inp = ''
    if token.token == "EOF":
        inp = '$'

    elif token.token in nont:
        inp = token.token
    else:
        inp = token.lexeme
    print("inp : ", inp, "   token : ",
          token.token, "   lexeme : ", token.lexeme)
    while stack[-1] != inp:
        print(stack)
        rule = df[stack[-1]][inp]
        print('rule  : ', rule)
        stack.pop()
        rule = (rule.split("::="))[-1]
        rule = ' '.join(rule.split())
        rule = rule.split(' ')
        # print(rule)
        for r in reversed(rule):
            if r == 'none':
                print('error while parsing')
                break
            if r != 'ε':
                stack.append(r)
    stack.pop()
print("Parsing successful")
