# Mini Python Compiler con Tkinter

Este proyecto implementa un **compilador simple** para un **subconjunto de Python** que utiliza bloques explícitos (`BEGIN ... END`) para definir estructuras de control. El compilador abarca varias fases típicas:

- **Análisis Léxico (Lexer):** Divide el código fuente en tokens usando expresiones regulares.
- **Análisis Sintáctico (Parser):** Construye un Árbol de Sintaxis Abstracta (AST) mediante un parser de descenso recursivo.
- **Análisis Semántico y Generación de Tabla de Símbolos:** Verifica el uso correcto de las variables y registra las declaraciones en una tabla de símbolos.
- **Generación de Código Intermedio (IR):** Produce código de tres direcciones para representar la lógica del programa.
- **Interfaz Gráfica con Tkinter:** Permite ingresar el código fuente y visualizar, en pestañas, los tokens, el AST, la tabla de símbolos y el código intermedio.

> **Nota:**  
> Este compilador no soporta la totalidad de Python, sino un subconjunto con asignaciones, expresiones aritméticas y estructuras de control básicas (`if-else` y `while`) utilizando bloques definidos con `BEGIN ... END`.

## Características

- **Lexer:** Procesa y tokeniza palabras clave, identificadores, números, operadores y otros símbolos.
- **Parser:** Implementa un parser recursivo que genera un AST a partir de las reglas del lenguaje.
- **Análisis Semántico:** Verifica el uso correcto de variables y construye una tabla de símbolos.
- **Generación de Código Intermedio:** Convierte el AST en un código de tres direcciones (IR) con variables temporales y etiquetas.
- **Interfaz Gráfica:** Interfaz sencilla en Tkinter para compilar y visualizar el proceso de compilación.

## Requisitos

- **Python 3.x**
- **Tkinter:** Generalmente viene incluido en la instalación estándar de Python.

## Instalación y Ejecución

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/RayDev001/Compiladores.git
   cd Compiladores
