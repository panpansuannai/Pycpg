import ply.lex as lex

reversed = {
    'if': 'IF',
    'while': 'WHILE',
    'else' : 'ELSE',
    'return' : 'RETURN',
    'break' : 'BREAK',
    'continue' : 'CONTINUE'
}

tokens = [
    'OP',
    'SEMI',
    'LPARENT',
    'RPARENT',
    'LCURLY',
    'RCURLY',
    'LSQUARE',
    'RSQUARE',
    'STRING'
] + list(reversed.values())

t_OP = r'\+|-|\*|\%|/|=|\&|\||\^|\'|\"|~|`|\!|\#|\$|>|<'
t_SEMI = r';'
t_IF = r'if'
t_WHILE = r'while'
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'

def t_STRING(t):
    r'[\w\d]+'
    t.type = reversed.get(t.value, 'STRING')
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    print("Invalid token: {}".format(t.values[0]))
    exit(0)

lexer = lex.lex(nowarn=True)

''' Run Test '''
if __name__ == '__main__':
    data = " if dfjaod3920{ df} break continue ~!#$%%^&*(( + - * / a = 19; % while "
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
