class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children else []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.code = []
        self.ast = []

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def match(self, expected_type):
        if self.current()[0] == expected_type:
            val = self.current()[1]
            self.pos += 1
            return val
        else:
            raise SyntaxError(f'Se esperaba {expected_type}, se encontró {self.current()}')

    def parse_program(self):
        nodes = []
        while self.current()[0] != 'EOF':
            stmt = self.parse_statement()
            nodes.append(stmt)
        self.ast = Node("Program", nodes)

    def parse_statement(self):
        if self.current()[0] == 'ID':
            var = self.match('ID')
            self.match('ASSIGN')
            expr = self.parse_expression()
            stmt_code = f'{var} = {expr.label}'
            self.code.append(stmt_code)
            return Node('Assign', [Node(var), expr])
        elif self.current()[0] == 'IF':
            self.match('IF')
            cond = self.parse_expression()
            self.match('THEN')
            body = []
            while self.current()[0] != 'END':
                stmt = self.parse_statement()
                body.append(stmt)
            self.match('END')
            self.code.append(f'if {cond.label}:')
            for b in body:
                for line in self._flatten_code(b):
                    self.code.append('    ' + line)
            return Node('If', [cond] + body)
        else:
            raise SyntaxError(f'Sentencia inválida: {self.current()[1]}')

    def parse_expression(self):
        left = self.parse_term()
        while self.current()[0] == 'OP' and self.current()[1] in ['+', '-']:
            op = self.match('OP')
            right = self.parse_term()
            left = Node(op, [left, right])
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current()[0] == 'OP' and self.current()[1] in ['*', '/']:
            op = self.match('OP')
            right = self.parse_factor()
            left = Node(op, [left, right])
        return left

    def parse_factor(self):
        token_type, value = self.current()
        if token_type == 'NUMBER':
            self.match('NUMBER')
            return Node(value)
        elif token_type == 'ID':
            self.match('ID')
            return Node(value)
        elif token_type == 'LPAREN':
            self.match('LPAREN')
            expr = self.parse_expression()
            self.match('RPAREN')
            return expr
        else:
            raise SyntaxError(f'Factor inválido: {value}')

    def _flatten_code(self, node):
        return self.code[-1:] if node.label != 'Assign' else [self.code[-1]]
