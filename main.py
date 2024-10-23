import sys
from lexer_flecha import lexer, test_lexer, remove_comments
from flecha_parser import parser

def format_ast(node, indent=1):
    if isinstance(node, list):
        indent_str = '  ' * indent
        formatted_list = []
        for elem in node:
            if isinstance(elem, list):
                formatted_list.append(format_ast(elem, indent + 1))
            elif isinstance(elem, int): 
                formatted_list.append(f'{elem}')
            else:
                formatted_list.append(f'"{elem}"')
        return '[\n' + indent_str + ',\n'.join(formatted_list) + f'\n{"  " * (indent-1)}]'
    else:
        return f'"{node}"'


def format_ast_output(ast):
    return '[\n' + ',\n'.join(format_ast(item) for item in ast) + '\n]'

if len(sys.argv) != 3:
    print("Usage: python main.py <inputfile> <outputfile>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    data = f.read()

data = remove_comments(data)

print("Tokens generados por el analizador léxico:")
test_lexer(data)

result = parser.parse(data, lexer=lexer)

# Escribir el AST formateado en el archivo de salida
with open(output_file, 'w') as f:
    formatted_ast = format_ast_output(result)
    f.write(formatted_ast)
