import ply.lex as lex

tokens = [
    'PROGRAM', 'BEGIN', 'END', 'VAR', 'INTEGER', 'BOOLEAN', 'REAL', 'STRING', 'ARRAY', 'OF',
    'FUNCTION', 'PROCEDURE', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FOR', 'TO', 'DOWNTO', 'REPEAT',
    'UNTIL', 'AND', 'OR', 'NOT', 'DIV', 'MOD', 'TRUE', 'FALSE', 'READ', 'READLN', 'WRITE', 'WRITELN',
    'ID', 'NUMBER', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK',
    'SEMI', 'COLON', 'COMMA', 'DOT', 'DOTDOT', 'CHAR_LITERAL'
]

t_ASSIGN = r':='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'='
t_NE = r'<>'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_DOTDOT = r'\.\.'

t_ignore = ' \t'

def t_PROGRAM(t):
    r'(?i:program)'
    return t

def t_BEGIN(t):
    r'(?i:begin)'
    return t

def t_END(t):
    r'(?i:end)'
    return t

def t_TRUE(t):
    r'(?i:true)'
    t.value = "true"
    return t

def t_FALSE(t):
    r'(?i:false)'
    t.value = "false"
    return t

def t_VAR(t):
    r'(?i:var)'
    return t

def t_INTEGER(t):
    r'(?i:integer)'
    return t

def t_BOOLEAN(t):
    r'(?i:boolean)'
    return t

def t_REAL(t):
    r'(?i:real)'
    return t

def t_STRING(t):
    r'(?i:string)'
    return t

def t_ARRAY(t):
    r'(?i:array)'
    return t

def t_OF(t):
    r'(?i:of)'
    return t

def t_FUNCTION(t):
    r'(?i:function)'
    return t

def t_PROCEDURE(t):
    r'(?i:procedure)'
    return t

def t_IF(t):
    r'(?i:if)'
    return t

def t_THEN(t):
    r'(?i:then)'
    return t

def t_ELSE(t):
    r'(?i:else)'
    return t

def t_WHILE(t):
    r'(?i:while)'
    return t

def t_DOWNTO(t):
    r'(?i:downto)'
    return t

def t_DO(t):
    r'(?i:do)'
    return t

def t_FOR(t):
    r'(?i:for)'
    return t

def t_TO(t):
    r'(?i:to)'
    return t

def t_REPEAT(t):
    r'(?i:repeat)'
    return t

def t_UNTIL(t):
    r'(?i:until)'
    return t

def t_AND(t):
    r'(?i:and)'
    t.value = 'and'
    return t

def t_OR(t):
    r'(?i:or)'
    t.value = 'or'
    return t

def t_NOT(t):
    r'(?i:not)'
    t.value = 'not'
    return t

def t_DIV(t):
    r'(?i:div)'
    return t

def t_MOD(t):
    r'(?i:mod)'
    return t

def t_READLN(t):
    r'(?i:readln)'
    return t

def t_READ(t):
    r'(?i:read)'
    return t

def t_WRITELN(t):
    r'(?i:writeln)'
    return t

def t_WRITE(t):
    r'(?i:write)'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_LITERAL(t):
    r'\'[^\']\''
    t.value = t.value
    return t

def t_STRING_LITERAL(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    t.value = t.value[1:-1] 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comment(t):
    r'\{.*?\}|\/\/.*'
    pass

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

#with open("../test.txt", "r", encoding="utf-8") as f:
#    data = f.read()
#    lexer.input(data)
#
#    for token in lexer:
#        print(token)
