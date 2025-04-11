import re

token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('IF',       r'if'),
    ('THEN',     r'then'),
    ('END',      r'end'),
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('ASSIGN',   r'='),
    ('OP',       r'[+\-*/]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

def lexer(code):
    pos = 0
    tokens = []
    mo = get_token(code, pos)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind in ['SKIP', 'NEWLINE']:
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Símbolo inesperado: {value}')
        else:
            tokens.append((kind, value))
        pos = mo.end()
        mo = get_token(code, pos)
    return tokens
