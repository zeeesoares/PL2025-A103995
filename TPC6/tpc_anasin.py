from tpc_analex import lexer
'''
Exp : Term ExpCont

ExpCont: ('+' | '-') Term ExpCont
    | ε

Term : Num TermCont

TermCont: ('*' | '/') Num TermCont
     | ε
'''


next_token = None

def next():
    global next_token
    next_token = lexer.token()

def rec_expr():
    left = rec_term()
    return rec_expr_cont(left)

def rec_expr_cont(left):
    global next_token

    if next_token and next_token.value in ('+', '-'):
        op = next_token.value
        next()
        right = rec_term()
        result = (op, left, right)
        return rec_expr_cont(result)

    return left  

def rec_term():
    global next_token

    if next_token and next_token.type == 'NUM':
        left = next_token.value
        next()
        return rec_term_cont(left)
    else:
        raise ValueError("Número esperado")

def rec_term_cont(left):
    global next_token

    if next_token and next_token.value in ('*', '/'):
        op = next_token.value
        next()

        if next_token and next_token.type == 'NUM':
            right = next_token.value
            next()
            result = (op, left, right)
            return rec_term_cont(result)

        else:
            raise ValueError("Número esperado após operador")

    return left  

def parse(expr: str):
    global next_token

    lexer.input(expr)
    next()
    return rec_expr()


def evaluate(tree) :
    if isinstance(tree, int):
        return tree
    (op, left, right) = tree
    if (op == '+'):
        return evaluate(left) + evaluate(right)
    if (op == '-'):
        return evaluate(left) - evaluate(right)
    if (op == '*'):
        return evaluate(left) * evaluate(right)
    if (op == '/'):
        return evaluate(left) / evaluate(right)


with open('input.txt','r') as data:
    lines = data.readlines()
    line = ""
    with open('output.txt','w') as data:
        for line in lines:
            data.write(str(evaluate(parse(line))))
            data.write("\n")

