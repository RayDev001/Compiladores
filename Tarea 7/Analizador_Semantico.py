# semantic_analyzer.py

# =========================================
# DEFINICIÓN DE NODOS DEL AST (Árbol de Sintaxis Abstracta)
# =========================================

class Node:
    pass

class Program(Node):
    def __init__(self, global_decls, functions):
        # global_decls: lista de VariableDeclaration
        # functions: lista de FunctionDeclaration
        self.global_decls = global_decls
        self.functions = functions

class VariableDeclaration(Node):
    def __init__(self, var_type, name):
        self.var_type = var_type  # Ej. "int"
        self.name = name

class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left      # expresión izquierda
        self.operator = operator  # Ej. '+', '-', '*', '/', '>', '<'
        self.right = right    # expresión derecha

class Literal(Node):
    def __init__(self, value, lit_type="int"):
        self.value = value
        self.lit_type = lit_type  # Por defecto, consideramos enteros

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class FunctionDeclaration(Node):
    def __init__(self, name, parameters, return_type, body):
        # parameters: lista de tuplas (nombre, tipo)
        # body: lista de sentencias (nodos)
        self.name = name
        self.parameters = parameters
        self.return_type = return_type  # Ej. "int" o "void"
        self.body = body

class FunctionCall(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments  # lista de expresiones

class IfStatement(Node):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body  # lista de sentencias
        self.else_body = else_body  # lista de sentencias o None

class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body  # lista de sentencias

class ReturnStatement(Node):
    def __init__(self, expr=None):
        self.expr = expr  # puede ser None en funciones void

# =========================================
# GESTIÓN DE TABLA DE SÍMBOLOS Y ÁMBITOS
# =========================================

class SymbolTable:
    def __init__(self):
        # Utilizaremos una pila de ámbitos (cada uno es un diccionario: nombre -> tipo)
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, var_type):
        # Declara una variable en el ámbito actual.
        current = self.scopes[-1]
        if name in current:
            return False  # ya estaba declarada en el ámbito actual
        current[name] = var_type
        return True

    def lookup(self, name):
        # Busca la variable en todos los ámbitos (desde el actual hasta el global)
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

# =========================================
# ANALIZADOR SEMÁNTICO
# =========================================

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        # Tabla de funciones: nombre -> (lista_de_parametros, return_type)
        self.functions = {}
        # Registro de errores semánticos
        self.errors = []
        # Para verificar el tipo de retorno dentro de funciones
        self.current_function_return_type = None

    def error(self, message):
        self.errors.append(message)
        print("Error semántico:", message)

    def analyze(self, node):
        method_name = 'analyze_' + node.__class__.__name__
        method = getattr(self, method_name, self.generic_analyze)
        return method(node)

    def generic_analyze(self, node):
        raise Exception(f'No se ha implementado analyze_{node.__class__.__name__}')

    def analyze_Program(self, node: Program):
        # Primero procesamos las declaraciones globales
        for decl in node.global_decls:
            self.analyze(decl)
        # Luego registramos las funciones (sin analizar sus cuerpos aún)
        for func in node.functions:
            if func.name in self.functions:
                self.error(f"La función '{func.name}' ya ha sido declarada.")
            else:
                self.functions[func.name] = (func.parameters, func.return_type)
        # Ahora analizamos el cuerpo de cada función
        for func in node.functions:
            self.analyze(func)

    def analyze_VariableDeclaration(self, node: VariableDeclaration):
        if not self.symbol_table.declare(node.name, node.var_type):
            self.error(f"La variable '{node.name}' ya fue declarada en este ámbito.")

    def analyze_Assignment(self, node: Assignment):
        var_type = self.symbol_table.lookup(node.name)
        if var_type is None:
            self.error(f"La variable '{node.name}' no ha sido declarada.")
        expr_type = self.analyze(node.expr)
        if var_type and expr_type and var_type != expr_type:
            self.error(f"Tipo incompatible en la asignación a '{node.name}': variable es de tipo '{var_type}' pero se le asigna '{expr_type}'.")

    def analyze_BinaryExpression(self, node: BinaryExpression):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        # Para este ejemplo, sólo se manejan enteros
        if left_type != "int" or right_type != "int":
            self.error(f"Operador '{node.operator}' solo admite operandos de tipo 'int'.")
            return None
        # Operadores aritméticos y de comparación producen 'int'
        return "int"

    def analyze_Literal(self, node: Literal):
        return node.lit_type

    def analyze_Identifier(self, node: Identifier):
        var_type = self.symbol_table.lookup(node.name)
        if var_type is None:
            self.error(f"La variable '{node.name}' no ha sido declarada.")
            return None
        return var_type

    def analyze_FunctionDeclaration(self, node: FunctionDeclaration):
        # Entramos en un nuevo ámbito para los parámetros y el cuerpo de la función.
        self.symbol_table.enter_scope()
        # Establecemos el tipo de retorno actual para verificar las sentencias return.
        previous_return_type = self.current_function_return_type
        self.current_function_return_type = node.return_type

        # Declaramos los parámetros
        for param_name, param_type in node.parameters:
            if not self.symbol_table.declare(param_name, param_type):
                self.error(f"El parámetro '{param_name}' ya fue declarado en la función '{node.name}'.")
        # Analizamos cada sentencia del cuerpo
        for stmt in node.body:
            self.analyze(stmt)
        # Restauramos el ámbito y el tipo de retorno anterior
        self.symbol_table.exit_scope()
        self.current_function_return_type = previous_return_type

    def analyze_FunctionCall(self, node: FunctionCall):
        if node.name not in self.functions:
            self.error(f"La función '{node.name}' no ha sido declarada.")
            return None
        param_list, ret_type = self.functions[node.name]
        if len(node.arguments) != len(param_list):
            self.error(f"La función '{node.name}' espera {len(param_list)} argumentos pero se le pasaron {len(node.arguments)}.")
        else:
            for i, arg in enumerate(node.arguments):
                arg_type = self.analyze(arg)
                expected_type = param_list[i][1]
                if arg_type != expected_type:
                    self.error(f"En la llamada a '{node.name}', el argumento {i+1} es de tipo '{arg_type}' pero se esperaba '{expected_type}'.")
        return ret_type

    def analyze_IfStatement(self, node: IfStatement):
        cond_type = self.analyze(node.condition)
        if cond_type != "int":
            self.error("La condición del 'if' debe ser de tipo 'int'.")
        # Nuevo ámbito para el bloque then
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            self.analyze(stmt)
        self.symbol_table.exit_scope()
        # Si existe bloque else, también se analiza en un nuevo ámbito
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                self.analyze(stmt)
            self.symbol_table.exit_scope()

    def analyze_WhileStatement(self, node: WhileStatement):
        cond_type = self.analyze(node.condition)
        if cond_type != "int":
            self.error("La condición del 'while' debe ser de tipo 'int'.")
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.analyze(stmt)
        self.symbol_table.exit_scope()

    def analyze_ReturnStatement(self, node: ReturnStatement):
        # Verificamos que estemos dentro de una función
        if self.current_function_return_type is None:
            self.error("La sentencia 'return' se encuentra fuera de una función.")
            return
        if self.current_function_return_type == "void":
            if node.expr is not None:
                self.error("La función es 'void' y no debe retornar un valor.")
        else:
            if node.expr is None:
                self.error(f"La función debe retornar un valor de tipo '{self.current_function_return_type}', pero no se retorna nada.")
            else:
                ret_expr_type = self.analyze(node.expr)
                if ret_expr_type != self.current_function_return_type:
                    self.error(f"Tipo de retorno incorrecto: se esperaba '{self.current_function_return_type}' pero se retorna '{ret_expr_type}'.")

# =========================================
# EJEMPLO DE AST (PROGRAMA DE PRUEBA)
# =========================================

def crear_programa_ejemplo():
    # Declaración global: int a;
    global_decl = VariableDeclaration("int", "a")

    # Función main (retorna int)
    # Sentencias de main:
    #   int x;
    #   x = 5;
    #   a = x + 2;
    #   b = 10;         // Error: 'b' no declarada
    #   int x;          // Error: redeclaración de 'x'
    #   foo(x);
    #   if (x > 0) { int y; y = x; } else { x = 0; }
    #   while (x < 10) { x = x + 1; }
    #   return x;
    main_body = [
        VariableDeclaration("int", "x"),
        Assignment("x", Literal(5)),
        Assignment("a", BinaryExpression(Identifier("x"), "+", Literal(2))),
        Assignment("b", Literal(10)),  # Error: 'b' no ha sido declarada
        VariableDeclaration("int", "x"),  # Error: redeclaración de 'x'
        FunctionCall("foo", [Identifier("x")]),
        IfStatement(
            condition=BinaryExpression(Identifier("x"), ">", Literal(0)),
            then_body=[
                VariableDeclaration("int", "y"),
                Assignment("y", Identifier("x"))
            ],
            else_body=[
                Assignment("x", Literal(0))
            ]
        ),
        WhileStatement(
            condition=BinaryExpression(Identifier("x"), "<", Literal(10)),
            body=[
                Assignment("x", BinaryExpression(Identifier("x"), "+", Literal(1)))
            ]
        ),
        ReturnStatement(Identifier("x"))
    ]
    func_main = FunctionDeclaration("main", parameters=[], return_type="int", body=main_body)

    # Función foo (tipo void, con parámetro int)
    # Sentencias de foo:
    #   a = param * 2;
    #   return;  (en funciones void, return no debe retornar valor)
    func_foo_body = [
        Assignment("a", BinaryExpression(Identifier("param"), "*", Literal(2))),
        ReturnStatement()  # Correcto para void
    ]
    func_foo = FunctionDeclaration("foo", parameters=[("param", "int")], return_type="void", body=func_foo_body)

    return Program(global_decls=[global_decl], functions=[func_main, func_foo])

# =========================================
# EJECUCIÓN DEL ANALIZADOR SEMÁNTICO
# =========================================

if __name__ == '__main__':
    programa = crear_programa_ejemplo()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(programa)
    if analyzer.errors:
        print("\nSe detectaron errores semánticos:")
        for err in analyzer.errors:
            print(" -", err)
    else:
        print("El análisis semántico se completó sin errores.")
