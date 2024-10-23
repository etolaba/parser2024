import ply.lex as lex

# Lista de palabras clave
keywords = {
    'def': 'DEF',
    'if': 'IF',
    'then': 'THEN',
    'elif': 'ELIF',
    'else': 'ELSE',
    'case': 'CASE',
    'Nil': 'NIL',
    'let': 'LET',
    'in': 'IN'
}

tokens = [
    'ID',
    'EQUALS',
    'NUMBER',
    'CHAR',
    'STRING',
    'LPAREN',
    'RPAREN',
    'PIPE',
    'ARROW', 
    'BACKSLASH',
    'SEMICOLON',
    'OR',
    'AND',
    'NOT',
    'EQ',
    'NE',
    'GE',
    'LE',
    'GT',
    'LT',
    'ADD',
    'SUB',
    'MUL',
    'DIV',
    'MOD',
    'NEWLINE',
] + list(keywords.values())


t_EQUALS = r'='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')  # Verificar si es una palabra clave
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'


t_ARROW = r'->'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BACKSLASH = r'\\'
t_SEMICOLON = r';'
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_PIPE = r'\|'

def t_CHAR(t):
    r"\'(\\[ntr\'\"\\]|.)\'"
    value = t.value[1:-1] 
    if value.startswith("\\"):
        escape_dict = {
            'n': '\n',
            't': '\t',
            'r': '\r',
            '\'': '\'',
            '"': '\"',
            '\\': '\\'
        }
        value = escape_dict.get(value[1], value)
    t.value = ord(value)
    return t

def t_STRING(t):
    r'\"(\\.|[^\\"])*\"'
    t.value = t.value[1:-1]

    escape_sequences = {
        '\\n': '\n',
        '\\t': '\t',
        '\\r': '\r',
        '\\\'': '\'',
        '\\"': '\"',
        '\\\\': '\\' 
    }
    
    for esc_seq, char in escape_sequences.items():
        t.value = t.value.replace(esc_seq, char)
    
    # Convertir los caracteres individuales en sus representaciones numéricas (ASCII)
    t.value = [ord(c) for c in t.value]
    
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass
    

def t_ignore_COMMENT(t):
    r'\-\-.*'
    pass 

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Función para probar el analizador léxico
def test_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

def remove_comments(code):
    """Elimina comentarios que comienzan con '--' y descarta todo lo que está después de '--' en una línea, excepto dentro de cadenas."""
    result = []
    lines = code.splitlines()

    for line in lines:
        # Si la línea empieza con '--', es un comentario completo y la descartamos
        if line.strip().startswith('--'):
            continue
        
        in_string = False
        i = len(line) - 1 
        while i >= 0:
            if line[i] == '"' and (i == 0 or line[i - 1] != '\\'):
                in_string = not in_string
            elif i > 1 and line[i-1:i+1] == '--' and not in_string: 
                line = line[:i-1].rstrip()
                break
            i -= 1
        
        if line.strip():
            result.append(line.strip())

    return '\n'.join(result)