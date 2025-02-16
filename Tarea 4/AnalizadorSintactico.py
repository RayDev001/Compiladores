# -*- coding: utf-8 -*-
"""
Analizador Sintáctico LALR(1) (método LR) en Python utilizando PLY
------------------------------------------------------------------
Este programa implementa un analizador sintáctico que evalúa expresiones
aritméticas simples. Utiliza PLY, que por defecto genera un parser LALR(1),
una variante del método LR.
"""

import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import scrolledtext

# ----------------------------------------------------------------------
# Parte Léxica: Definición de tokens
# ----------------------------------------------------------------------
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN'
)

# Patrones para los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convertir la cadena a entero
    return t


t_ignore = ' \t'  # Ignorar espacios y tabulaciones


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)


# Construcción del lexer
lexer = lex.lex()


# ----------------------------------------------------------------------
# Parte Sintáctica: Definición de la gramática (método LR - LALR(1))
# ----------------------------------------------------------------------
# La gramática es la siguiente:
#
# expression : expression PLUS term
#            | expression MINUS term
#            | term
#
# term       : term TIMES factor
#            | term DIVIDE factor
#            | factor
#
# factor     : NUMBER
#            | LPAREN expression RPAREN

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


def p_error(p):
    if p:
        print(f"Error sintáctico en el token {p.type}")
    else:
        print("Error sintáctico al final de la entrada")


# Construcción del parser (usa LALR(1), método LR)
parser = yacc.yacc()

# ----------------------------------------------------------------------
# Interfaz Gráfica con Tkinter
# ----------------------------------------------------------------------
root = tk.Tk()
root.title("Analizador Sintáctico LALR (LR)")

# Marco para la entrada de la expresión
frame_input = tk.LabelFrame(root, text="Expresión a analizar", padx=10, pady=10)
frame_input.pack(padx=10, pady=10, fill="both", expand=True)

text_input = scrolledtext.ScrolledText(frame_input, wrap=tk.WORD, width=60, height=5)
text_input.pack(fill="both", expand=True)


# Función que procesa la expresión usando el parser LR (LALR(1))
def analyze_syntax():
    input_text = text_input.get("1.0", tk.END).strip()
    if input_text == "":
        return
    try:
        result = parser.parse(input_text)
        output = f"Resultado: {result}"
    except Exception as e:
        output = f"Error: {str(e)}"

    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output)
    text_output.config(state=tk.DISABLED)


# Botón para iniciar el análisis
btn_parse = tk.Button(root, text="Analizar", command=analyze_syntax)
btn_parse.pack(pady=5)

# Marco para la salida de resultados
frame_output = tk.LabelFrame(root, text="Resultado del Análisis", padx=10, pady=10)
frame_output.pack(padx=10, pady=10, fill="both", expand=True)

text_output = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD, width=60, height=5, state=tk.DISABLED)
text_output.pack(fill="both", expand=True)

# Iniciar la aplicación gráfica
root.mainloop()
