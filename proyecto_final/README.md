# Compilador con Interfaz Gráfica - Raynick Rosario

Este proyecto es un compilador completo desarrollado en Python con una interfaz gráfica usando Tkinter. Incluye análisis léxico, sintáctico, generación de código intermedio, ejecución del mismo y visualización del árbol sintáctico (AST).

## 📦 Estructura del Proyecto

- `compiler_gui.py`: Interfaz gráfica principal.
- `lexer.py`: Analizador léxico.
- `parser.py`: Analizador sintáctico y generador de AST.
- `intermediate.py`: Generador de código intermedio.
- `executor.py`: Ejecuta el código intermedio.
- `visual_ast.py`: Visualiza el árbol sintáctico usando Tkinter Canvas.

## 🚀 Cómo usar

1. Asegúrate de tener Python 3 instalado.
2. Extrae los archivos del `.zip`.
3. Ejecuta el archivo `compiler_gui.py`:

```bash
python compiler_gui.py
```

## 🧪 Ejemplo de Código

```plaintext
x = 5
y = 3
if x then
    z = x + y
end
```

## ✅ Funcionalidades

- **Compilar**: Muestra los tokens, código intermedio, resultado de ejecución y AST visual.
- **Guardar TXT**: Guarda el código intermedio en un archivo `.txt`.
- **Cargar Archivo**: Carga código desde un archivo `.txt`.
- **Limpiar**: Borra la entrada y salida.

## 🎨 Personalización

Puedes modificar el fondo del área de salida en `compiler_gui.py`:

```python
output_display = tk.Text(..., bg="black", fg="lime", insertbackground="white")
```

## 👨‍💻 Autor

Proyecto final de Raynick Rosario  
Universidad | Matrícula: 1-21-0012
