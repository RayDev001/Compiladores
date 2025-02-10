# -*- coding: utf-8 -*-
"""
Analizador Léxico en Python utilizando PLY (similar a FLEX)
------------------------------------------------------------
Este programa implementa un analizador léxico para un lenguaje simple
de expresiones aritméticas y de identificadores. Se utiliza la librería
PLY para definir los tokens y las expresiones regulares, y se presenta una
interfaz gráfica (Tkinter) para ingresar el texto y visualizar el análisis.
"""

import tkinter as tk
from tkinter import scrolledtext
import ply.lex as lex

# ----------------------------------------------------------------------
# Definición de tokens
# ----------------------------------------------------------------------
# Lista de nombres de tokens que el analizador reconocerá.
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'ID'
)

# Expresiones regulares para tokens de un solo carácter
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Token para identificadores: letras, números y guiones bajos, comenzando con letra o _
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'


# Token para números (enteros)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convertir el valor a entero
    return t


# Caracteres a ignorar (espacios y tabulaciones)
t_ignore = ' \t'


# Actualización del contador de línea para saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Manejo de errores: se muestra un mensaje en consola y se ignora el carácter ilegal
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)


# Construcción del lexer (analizador léxico)
lexer = lex.lex()


# ----------------------------------------------------------------------
# Función para realizar el análisis léxico sobre el texto de entrada
# ----------------------------------------------------------------------
def analyze_input():
    # Obtener el texto ingresado en el widget de texto
    input_text = text_input.get("1.0", tk.END)
    lexer.input(input_text)

    # Acumular la salida (tokens encontrados)
    output = ""
    while True:
        tok = lexer.token()
        if not tok:
            break  # No hay más tokens
        output += f"Token: {tok.type}, Valor: {tok.value}, Línea: {tok.lineno}\n"

    # Mostrar la salida en el widget de texto de resultados
    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, output)
    text_output.config(state=tk.DISABLED)


# ----------------------------------------------------------------------
# Configuración de la interfaz gráfica con Tkinter
# ----------------------------------------------------------------------
root = tk.Tk()
root.title("Analizador Léxico")

# Marco para la entrada de texto
frame_input = tk.LabelFrame(root, text="Entrada de Texto", padx=10, pady=10)
frame_input.pack(padx=10, pady=10, fill="both", expand=True)

# Widget de texto con scroll para la entrada
text_input = scrolledtext.ScrolledText(frame_input, wrap=tk.WORD, width=60, height=10)
text_input.pack(fill="both", expand=True)

# Botón para iniciar el análisis léxico
btn_analyze = tk.Button(root, text="Analizar", command=analyze_input)
btn_analyze.pack(pady=5)

# Marco para la salida de resultados
frame_output = tk.LabelFrame(root, text="Salida del Analizador Léxico", padx=10, pady=10)
frame_output.pack(padx=10, pady=10, fill="both", expand=True)

# Widget de texto con scroll para mostrar los tokens encontrados (modo solo lectura)
text_output = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD, width=60, height=10, state=tk.DISABLED)
text_output.pack(fill="both", expand=True)

# Iniciar la aplicación gráfica
root.mainloop()
