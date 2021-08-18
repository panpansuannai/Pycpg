import ply.yacc as yacc
from lexer import tokens, lexer
from proc_struct import  *

def test():
    test_condition = __name__ == '__main__'
    return test_condition

''' Which rule to start with'''
start = 'Unit'

def p_unit(p):
    '''Unit : StmtList'''
    p[0] = p[1]

def p_element(p):
    '''Element : STRING
                | OP'''
    p[0] = BodyStruct(p[1])

def p_element_list(p):
    '''ElementList : Element
                    | ElementList Element'''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[1].merge_body(p[2])
        p[0] = p[1]

def p_element_parentness(p):
    'Element : LPARENT ElementList RPARENT'
    p[0] = p[2]

def p_stmt(p):
    'Stmt : ElementList SEMI'
    p[0] = StructsBlock()
    p[0].add_struct(p[1])

''' while ( Strings ) { Stmts } '''
def p_while_stmt(p):
    'Stmt : WHILE LPARENT ElementList RPARENT LCURLY StmtList RCURLY'
    block = WhileStructBody(p[6])
    p[0] = WhileStruct(p[3], block)

''' if ( Strings { Stmts } '''
def p_if_stmt(p):
    'Stmt : IF LPARENT ElementList RPARENT LCURLY StmtList RCURLY'
    if_block = IfStructBody(p[6])
    p[0] = IfStruct(p[3], if_block)

def p_stmt_list(p):
    '''StmtList : Stmt 
                | StmtList Stmt'''
    if (len(p) == 2):
        p[0] = StructsBlock()
        p[0].add_struct(p[1])
    elif (len(p) == 3):
        p[1].add_struct(p[2])
        p[0] = p[1]

def p_error(p):
    print("Parser Error")
    if not test():
        exit(0)

parser = yacc.yacc(write_tables=False,debug=None)

''' Run Test'''
if test():
    test_case_str = ('if (~`!#$%^&*2167djia jdfia) { jdiofa; jidfa; jodfa;}',
    'while(dfjiao(djfio3902++f) **dfjai) { jdoa; *&*#; ++; }')
    for s in test_case_str:
        print("> {}".format(s))
        print(parser.parse(s, lexer=lexer))
    ''' Interprete '''
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s, lexer=lexer)
        print(result)