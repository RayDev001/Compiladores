import tkinter as tk
from tkinter import filedialog, messagebox
from intermediate import compile_code
from lexer import lexer
from executor import execute_code
from visual_ast import show_ast_window

generated_code = []

def run_compiler():
    global generated_code
    code = code_input.get("1.0", tk.END)
    output_display.delete("1.0", tk.END)
    generated_code = []
    try:
        tokens = lexer(code)
        output_display.insert(tk.END, "Tokens generados:\n")
        for token in tokens:
            output_display.insert(tk.END, f"{token}\n")
        intermediate, ast = compile_code(code)
        generated_code = intermediate
        output_display.insert(tk.END, "\nCódigo intermedio:\n")
        for line in intermediate:
            output_display.insert(tk.END, line + '\n')
        output_display.insert(tk.END, "\nEjecución:\n")
        results = execute_code(intermediate)
        for r in results:
            output_display.insert(tk.END, r + '\n')
        show_ast_window(ast)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    code_input.delete("1.0", tk.END)
    output_display.delete("1.0", tk.END)

def load_code():
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, "r") as file:
            code = file.read()
            code_input.delete("1.0", tk.END)
            code_input.insert(tk.END, code)

def save_code():
    if not generated_code:
        messagebox.showwarning("Advertencia", "Primero debes compilar el código.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, "w") as f:
            for line in generated_code:
                f.write(line + "\n")
        messagebox.showinfo("Éxito", f"Código intermedio guardado en {path}")

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Compilador Completo - AST y Ejecución")
    app.geometry("950x700")

    frame = tk.Frame(app)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    global code_input, output_display

    code_input = tk.Text(frame, height=15, width=110)
    code_input.pack(pady=10)

    btn_frame = tk.Frame(frame)
    btn_frame.pack()

    tk.Button(btn_frame, text="Cargar Archivo", command=load_code).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Compilar", command=run_compiler).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Guardar TXT", command=save_code).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Limpiar", command=clear_fields).pack(side=tk.LEFT, padx=5)

    output_display = tk.Text(frame, height=20, width=110, bg="black", fg="lime", insertbackground="white")
    output_display.pack(pady=10)

    app.mainloop()
