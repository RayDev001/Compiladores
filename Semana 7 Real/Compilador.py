import re
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

############################################################
# 1. ANALIZADOR LÉXICO
############################################################
token_spec = [
    ('IF', r'if\b'),
    ('ELSE', r'else\b'),
    ('WHILE', r'while\b'),
    ('BEGIN', r'BEGIN\b'),
    ('END', r'END\b'),
    ('ID', r'[A-Za-z_]\w*'),  # Identificadores
    ('NUM', r'\d+(\.\d+)?'),  # Números (enteros o decimales)
    ('ASSIGN', r'='),  # Asignación
    ('OP', r'[+\-*/]'),  # Operadores aritméticos
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COLON', r':'),
    ('SEMICOL', r';'),
    ('NEWLINE', r'\n+'),
    ('SKIP', r'[ \t]+'),  # Espacios
    ('MISMATCH', r'.'),  # Cualquier otro carácter no esperado
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)


def lexer(code):
    """
    Convierte el código fuente en una lista de tokens (tipo, valor).
    """
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind in ['IF', 'ELSE', 'WHILE', 'BEGIN', 'END']:
            tokens.append((kind, value))
        elif kind == 'ID':
            tokens.append(('ID', value))
        elif kind == 'NUM':
            val = float(value) if '.' in value else int(value)
            tokens.append(('NUM', val))
        elif kind == 'ASSIGN':
            tokens.append(('ASSIGN', value))
        elif kind == 'OP':
            tokens.append(('OP', value))
        elif kind == 'LPAREN':
            tokens.append(('LPAREN', value))
        elif kind == 'RPAREN':
            tokens.append(('RPAREN', value))
        elif kind == 'COLON':
            tokens.append(('COLON', value))
        elif kind == 'SEMICOL':
            tokens.append(('SEMICOL', value))
        elif kind == 'NEWLINE':
            # Ignoramos saltos de línea en este ejemplo
            continue
        elif kind == 'SKIP':
            # Ignoramos espacios
            continue
        elif kind == 'MISMATCH':
            raise ValueError(f"Carácter inesperado: {value}")
    return tokens


############################################################
# 2. AST (Árbol de Sintaxis Abstracta)
############################################################
class ASTNode:
    def __init__(self, nodetype, value=None, children=None):
        """
        nodetype: 'assign', 'binop', 'if', 'while', 'num', 'id', 'block'
        value:    nombre de variable, operador, etc.
        children: lista de nodos hijos
        """
        self.nodetype = nodetype
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"{self.nodetype}({self.value}, {self.children})"


############################################################
# 3. PARSER: Construye el AST a partir de la lista de tokens
############################################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_type):
        """
        Avanza en la lista de tokens si el tipo coincide,
        de lo contrario lanza un error de sintaxis.
        """
        token = self.current_token()
        if token and token[0] == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Se esperaba {expected_type}, encontrado {token}")

    def parse(self):
        """
        parse() -> Devuelve una lista de nodos AST (varias sentencias).
        """
        statements = []
        while self.current_token() is not None:
            statements.append(self.statement())
        return statements

    def statement(self):
        """
        statement -> if_statement | while_statement | assign_statement
        """
        token = self.current_token()
        if not token:
            return None
        if token[0] == 'IF':
            return self.if_statement()
        elif token[0] == 'WHILE':
            return self.while_statement()
        elif token[0] == 'ID':
            return self.assign_statement()
        else:
            raise SyntaxError(f"Sentencia desconocida con token {token}")

    def block(self):
        """
        block -> BEGIN statement* END
        """
        self.match('BEGIN')
        stmts = []
        while self.current_token() and self.current_token()[0] != 'END':
            stmts.append(self.statement())
        self.match('END')
        return ASTNode('block', None, stmts)

    def if_statement(self):
        """
        if_statement -> IF expression COLON block [ ELSE COLON block ]
        """
        self.match('IF')
        condition = self.expression()
        self.match('COLON')
        if_block = self.block()

        else_block = ASTNode('block', None, [])
        token = self.current_token()
        if token and token[0] == 'ELSE':
            self.match('ELSE')
            self.match('COLON')
            else_block = self.block()
        return ASTNode('if', None, [condition, if_block, else_block])

    def while_statement(self):
        """
        while_statement -> WHILE expression COLON block
        """
        self.match('WHILE')
        condition = self.expression()
        self.match('COLON')
        body_block = self.block()
        return ASTNode('while', None, [condition, body_block])

    def assign_statement(self):
        """
        assign_statement -> ID ASSIGN expression SEMICOL
        """
        id_token = self.match('ID')
        self.match('ASSIGN')
        expr_node = self.expression()
        self.match('SEMICOL')
        return ASTNode('assign', id_token[1], [expr_node])

    def expression(self):
        """
        Soporta +, -, *, /, y paréntesis:
        expression -> term ( ('+'|'-') term )*
        """
        node = self.term()
        while (self.current_token() and
               self.current_token()[0] == 'OP' and
               self.current_token()[1] in ['+', '-']):
            op_token = self.match('OP')
            right = self.term()
            node = ASTNode('binop', op_token[1], [node, right])
        return node

    def term(self):
        """
        term -> factor ( ('*'|'/') factor )*
        """
        node = self.factor()
        while (self.current_token() and
               self.current_token()[0] == 'OP' and
               self.current_token()[1] in ['*', '/']):
            op_token = self.match('OP')
            right = self.factor()
            node = ASTNode('binop', op_token[1], [node, right])
        return node

    def factor(self):
        """
        factor -> NUM | ID | '(' expression ')'
        """
        token = self.current_token()
        if not token:
            raise SyntaxError("Fin de tokens inesperado en 'factor'.")

        if token[0] == 'NUM':
            self.match('NUM')
            return ASTNode('num', token[1])
        elif token[0] == 'ID':
            self.match('ID')
            return ASTNode('id', token[1])
        elif token[0] == 'LPAREN':
            self.match('LPAREN')
            node = self.expression()
            self.match('RPAREN')
            return node
        else:
            raise SyntaxError(f"Factor inesperado con token {token}")


############################################################
# 4. ANÁLISIS SEMÁNTICO Y TABLA DE SÍMBOLOS
############################################################
symbol_table = {}


def semantic_analysis(ast_nodes):
    """
    Recorre el AST y verifica uso de variables, llenando la tabla de símbolos.
    """
    symbol_table.clear()
    for node in ast_nodes:
        analyze_node(node)


def analyze_node(node):
    if node.nodetype == 'assign':
        var_name = node.value
        if var_name not in symbol_table:
            symbol_table[var_name] = {'type': 'unknown', 'initialized': True}
        analyze_node(node.children[0])

    elif node.nodetype == 'binop':
        left, right = node.children
        analyze_node(left)
        analyze_node(right)

    elif node.nodetype == 'num':
        # No requiere acción
        pass

    elif node.nodetype == 'id':
        if node.value not in symbol_table:
            symbol_table[node.value] = {'type': 'unknown', 'initialized': False}

    elif node.nodetype == 'if':
        # children = [cond, if_block, else_block]
        condition = node.children[0]
        if_block = node.children[1]
        else_block = node.children[2]
        analyze_node(condition)
        analyze_node(if_block)
        analyze_node(else_block)

    elif node.nodetype == 'while':
        condition = node.children[0]
        block_node = node.children[1]
        analyze_node(condition)
        analyze_node(block_node)

    elif node.nodetype == 'block':
        for stmt in node.children:
            analyze_node(stmt)


############################################################
# 5. GENERACIÓN DE CÓDIGO INTERMEDIO (3 Direcciones)
############################################################
temp_count = 0
ir_code = []


def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"


def generate_code(ast_nodes):
    global ir_code, temp_count
    ir_code = []
    temp_count = 0
    for node in ast_nodes:
        gen_stmt(node)
    return ir_code


def gen_stmt(node):
    if node.nodetype == 'assign':
        expr_result = gen_expr(node.children[0])
        ir_code.append(f"{node.value} = {expr_result}")

    elif node.nodetype == 'if':
        # children = [cond, if_block, else_block]
        cond_expr = gen_expr(node.children[0])
        label_else = f"label_else_{new_temp()}"
        label_end = f"label_end_{new_temp()}"
        ir_code.append(f"IF NOT {cond_expr} GOTO {label_else}")

        # if_block
        gen_stmt(node.children[1])

        ir_code.append(f"GOTO {label_end}")
        ir_code.append(f"{label_else}:")
        # else_block
        gen_stmt(node.children[2])
        ir_code.append(f"{label_end}:")

    elif node.nodetype == 'while':
        # children = [cond, block]
        label_start = f"label_while_{new_temp()}"
        label_end = f"label_end_{new_temp()}"
        ir_code.append(f"{label_start}:")
        cond_expr = gen_expr(node.children[0])
        ir_code.append(f"IF NOT {cond_expr} GOTO {label_end}")
        gen_stmt(node.children[1])
        ir_code.append(f"GOTO {label_start}")
        ir_code.append(f"{label_end}:")

    elif node.nodetype == 'block':
        for stmt in node.children:
            gen_stmt(stmt)


def gen_expr(node):
    if node.nodetype == 'num':
        return str(node.value)
    elif node.nodetype == 'id':
        return node.value
    elif node.nodetype == 'binop':
        left = gen_expr(node.children[0])
        right = gen_expr(node.children[1])
        temp_var = new_temp()
        ir_code.append(f"{temp_var} = {left} {node.value} {right}")
        return temp_var
    else:
        # if, while, assign se manejan en gen_stmt, no en gen_expr
        return ""


############################################################
# 6. FUNCIÓN PRINCIPAL DEL COMPILADOR
############################################################
def compile_code(source):
    """
    Toma el código fuente, produce (tokens, ast, symbol_table, ir).
    """
    # 1. Análisis Léxico
    tokens = lexer(source)

    # 2. Análisis Sintáctico
    parser = Parser(tokens)
    ast_nodes = parser.parse()

    # 3. Análisis Semántico
    semantic_analysis(ast_nodes)

    # 4. Generación de Código Intermedio
    ir = generate_code(ast_nodes)

    return tokens, ast_nodes, symbol_table.copy(), ir


############################################################
# 7. INTERFAZ GRÁFICA CON TKINTER
############################################################
class MiniPythonCompilerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini-Compilador (Subconjunto de Python) con Tkinter")
        self.geometry("1000x700")

        # Frame superior: Área de texto para el código y botón "Compilar"
        top_frame = tk.Frame(self, padx=5, pady=5)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top_frame, text="Código Fuente:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        compile_button = tk.Button(top_frame, text="Compilar", command=self.on_compile)
        compile_button.pack(side=tk.RIGHT, padx=5)

        # Área de texto para el código fuente
        self.code_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10)
        self.code_text.pack(fill=tk.X, padx=5, pady=5)
        example_code = """\
# Ejemplo de código en este mini-lenguaje:
x = 3 + 2;
if x : BEGIN
    x = x * 2;
END
else : BEGIN
    x = x - 1;
END

while x : BEGIN
    x = x - 1;
END
"""
        self.code_text.insert(tk.END, example_code)

        # Notebook para mostrar Tokens, AST, Tabla de Símbolos, IR
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tokens_text = self.create_tab("Tokens")
        self.ast_text = self.create_tab("AST")
        self.symtab_text = self.create_tab("Tabla de Símbolos")
        self.ir_text = self.create_tab("Código Intermedio")

    def create_tab(self, title):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)
        return text_area

    def on_compile(self):
        source_code = self.code_text.get("1.0", tk.END)
        # Limpiar áreas de salida
        self.tokens_text.delete("1.0", tk.END)
        self.ast_text.delete("1.0", tk.END)
        self.symtab_text.delete("1.0", tk.END)
        self.ir_text.delete("1.0", tk.END)

        try:
            tokens, ast_nodes, symtab, ir = compile_code(source_code)

            # Mostrar Tokens
            self.tokens_text.insert(tk.END, "Tokens:\n")
            for t in tokens:
                self.tokens_text.insert(tk.END, f"{t}\n")

            # Mostrar AST
            self.ast_text.insert(tk.END, "Árbol de Sintaxis (AST):\n")
            for node in ast_nodes:
                self.ast_text.insert(tk.END, f"{node}\n")

            # Mostrar Tabla de Símbolos
            self.symtab_text.insert(tk.END, "Tabla de Símbolos:\n")
            for k, v in symtab.items():
                self.symtab_text.insert(tk.END, f"{k} -> {v}\n")

            # Mostrar Código Intermedio
            self.ir_text.insert(tk.END, "Código Intermedio (3 Direcciones):\n")
            for line in ir:
                self.ir_text.insert(tk.END, line + "\n")

        except Exception as e:
            self.tokens_text.insert(tk.END, f"Error: {e}\n")
            self.ast_text.insert(tk.END, f"Error: {e}\n")
            self.symtab_text.insert(tk.END, f"Error: {e}\n")
            self.ir_text.insert(tk.END, f"Error: {e}\n")


def main():
    app = MiniPythonCompilerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
