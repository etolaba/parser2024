import ply.yacc as yacc
from lexer_flecha import tokens

inside_case_branch = False

precedence = (
    ('right', 'SEMICOLON'),
    ('left', 'LOWER'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'NOT', 'UMINUS')
)

def p_program(p):
    '''program : statements
               | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = []

def p_expression_binary(p):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression EQ expression
                  | expression NE expression
                  | expression GE expression
                  | expression LE expression
                  | expression GT expression
                  | expression LT expression
                  | expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression MOD expression'''
    operator_map = {
        '||': 'OR',
        '&&': 'AND',
        '==': 'EQ',
        '!=': 'NE',
        '>=': 'GE',
        '<=': 'LE',
        '>': 'GT',
        '<': 'LT',
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV',
        '%': 'MOD'
    }
    op = operator_map[p[2]]
    p[0] = ["ExprApply", ["ExprApply", ["ExprVar", op], p[1]], p[3]]

def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]


def p_statements_single(p):
    'statements : statement '
    p[0] = [p[1]]

def p_statement_def(p):
    'statement : DEF ID EQUALS expression'
    p[0] = ["Def", p[2], p[4]] 


def p_expression_variable(p):
    'expression : ID'
    if p[1][0].isupper():  # Detectar si es un constructor
        p[0] = ["ExprConstructor", p[1]]
    else:
        p[0] = ["ExprVar", p[1]]

def p_expression_sequence(p):
    '''expression : expression SEMICOLON expression %prec SEMICOLON'''
    p[0] = ["ExprLet", "_", p[1], p[3]]




def p_expression_unary(p):
    '''expression : NOT expression
                  | SUB expression %prec UMINUS'''
    operator_map = {
        '!': 'NOT',
        '-': 'UMINUS'
    }
    op = operator_map[p[1]]
    p[0] = ["ExprApply", ["ExprVar", op], p[2]]



def p_expression_let(p):
    '''expression : LET ID EQUALS expression IN expression
                  | LET ID params EQUALS expression IN expression'''
    if len(p) == 7:
        p[0] = ["ExprLet", p[2], p[4], p[6]]
    else:
        params = p[3]
        body = p[5]
        lambda_expr = create_lambda(params, body)
        p[0] = ["ExprLet", p[2], lambda_expr, p[7]]

# Función auxiliar para crear expresiones lambda encadenadas
def create_lambda(params, body):
    if not params:
        return body
    param = params[0]
    rest_params = params[1:]
    return ["ExprLambda", param, create_lambda(rest_params, body)]


def p_expression_parens(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_lambda(p):
    '''expression : BACKSLASH parameters ARROW expression
                  | BACKSLASH ARROW expression'''
    if len(p) == 5:
        # Caso con parámetros
        parameters = p[2] if isinstance(p[2], list) else [p[2]]
        expr = p[4]
        for param in reversed(parameters):
            expr = ["ExprLambda", param, expr]
        p[0] = expr
    else:
        # Caso sin parámetros, devuelve directamente la expresión
        p[0] = p[3]

def p_parameters_single(p):
    '''parameters : ID'''
    p[0] = p[1]

def p_expression_apply(p):
    '''expression : expression expression %prec LOWER'''
    p[0] = ["ExprApply", p[1], p[2]]

def p_parameters_multiple(p):
    '''parameters : ID parameters'''
    p[0] = [p[1]] + (p[2] if isinstance(p[2], list) else [p[2]])

def p_expression_string(p):
    'expression : STRING'
    p[0] = string_to_list(p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ["ExprNumber", p[1]]

def p_expression_char(p):
    'expression : CHAR'
    p[0] = ["ExprChar", p[1]]

def p_expression_nil(p):
    'expression : NIL'
    p[0] = ["ExprConstructor", "Nil"]

def p_expression_if(p):
    '''expression : IF expression THEN expression else_clause
                  | IF expression THEN expression NEWLINE
                  | IF expression THEN expression NEWLINE else_clause
                  | IF expression NEWLINE THEN expression NEWLINE else_clause'''
    if len(p) == 5:
        p[0] = ["ExprCase", p[2], [["CaseBranch", "True", [], p[4]]] + p[5]]
    if len(p) == 6:
        p[0] = ["ExprCase", p[2], [["CaseBranch", "True", [], p[4]]] + p[5]]
    if len(p) == 7:
        p[0] = ["ExprCase", p[2], [["CaseBranch", "True", [], p[4]]] + p[6]]
    
def p_else_clause(p):
    '''else_clause : ELSE expression
                   | ELIF expression NEWLINE THEN expression NEWLINE else_clause
                   | ELIF expression THEN expression else_clause
                   | ELIF expression THEN expression NEWLINE else_clause'''
    if len(p) == 3:
        p[0] = [["CaseBranch", "False", [], p[2]]]
    if len(p) == 6:
        p[0] = [["CaseBranch", "False", [], ["ExprCase", p[2], [["CaseBranch", "True", [], p[4]]] + p[5]]]]
    if len(p) == 7:
        p[0] = [["CaseBranch", "False", [], ["ExprCase", p[2], [["CaseBranch", "True", [], p[4]]] + p[6]]]]

def p_expression_case(p):
    '''expression : CASE expression
                  | CASE expression case_branches'''
    if len(p) == 3:
        p[0] = ["ExprCase", p[2], []]
    else:
        p[0] = ["ExprCase", p[2], p[3]]

def p_case_branches(p):
    '''case_branches : PIPE constructor_pattern ARROW expression
                     | case_branches PIPE constructor_pattern ARROW expression'''
    global inside_case_branch
    inside_case_branch = True
    if len(p) == 5:
        constructor, params = p[2]
        p[0] = [["CaseBranch", constructor, params, p[4]]]
    else:
        constructor, params = p[3]
        p[0] = p[1] + [["CaseBranch", constructor, params, p[5]]]
    inside_case_branch = False

def p_constructor_pattern(p):
    '''constructor_pattern : ID
                           | NIL
                           | ID params'''
    if len(p) == 2:
        # Solo un constructor sin parámetros
        p[0] = (p[1], [])
    else:
        # Constructor con parámetros
        p[0] = (p[1], p[2])



def p_pattern(p):
    '''pattern : ID
               | ID ID
               | ID ID ID
               | ID ID ID ID'''
    if len(p) == 2:
        p[0] = p[1]  # Un solo patrón
    else:
        p[0] = [p[1]] + p[2:]  # Patrones múltiples

# Regla para los parámetros de una función
def p_params(p):
    '''params : ID
              | ID params'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]



def p_error(p):
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")

def string_to_list(string):
    result = []
    
    # Convertimos cada carácter en una lista de expresiones
    for char in string:
        if isinstance(char, int):
            # Si el valor ya es un número ASCII, lo usamos directamente
            result.append(["ExprApply", ["ExprConstructor", "Cons"], ["ExprChar", char]])
        else:
            # Si no, aplicamos ord() para obtener su valor ASCII
            result.append(["ExprApply", ["ExprConstructor", "Cons"], ["ExprChar", ord(char)]])
    
    # Agregar el "Nil" al final de la lista
    result.append(["ExprConstructor", "Nil"])
    
    # Enlazamos todos los ExprApply
    while len(result) > 1:
        right = result.pop()
        left = result.pop()
        result.append(["ExprApply", left, right])
    
    return result[0]

parser = yacc.yacc()
