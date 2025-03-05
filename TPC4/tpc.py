import ply.lex as lex
import sys

tokens = (
    "COMMENT",
    "SELECT",
    "WHERE",
    "LIMIT",
    "LBRACE",
    "RBRACE",
    "DOT",
    "VAR",
    "NUM",
    "LITERAL",
    "PREDICATE"
)

def t_COMMENT(t):
    r'\#.*'
    return t

def t_SELECT(t):
    r'(?i:SELECT)'
    return t

def f_WHERE(t):
    r'(?i:WHERE)'
    return t

def f_LIMIT(t):
    r'(?i:LIMIT)'
    return t

def t_LBRACE(t):
    r'{'
    return t

def t_RBRACE(t):
    r'}'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_VAR(t):
    r'\?\w+'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_PREDICATE(t):
    r'a|(\w+:\w+)'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_LITERAL(t):
    r'[\w@\"\s]+'
    return t


t_ignore = ' \t'

def t_error(t):
    print(f'Illegar character "{t.value[0]}"', file=sys.stderr)
    t.lexer.skip(1)

if __name__ == '__main__':
    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    with open("output.txt","w") as wf:
        for token in lexer:
            wf.write(str(token))
            wf.write('\n')
