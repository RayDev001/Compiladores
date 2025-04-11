import tkinter as tk

def draw_ast(canvas, node, x, y, dx, dy, parent_coords=None):
    if not node:
        return
    canvas.create_oval(x-20, y-20, x+20, y+20, fill='lightblue')
    canvas.create_text(x, y, text=node.label)
    if parent_coords:
        canvas.create_line(parent_coords[0], parent_coords[1], x, y)
    if hasattr(node, 'children'):
        num_children = len(node.children)
        for i, child in enumerate(node.children):
            cx = x + dx * (i - num_children / 2 + 0.5)
            cy = y + dy
            draw_ast(canvas, child, cx, cy, dx / 1.5, dy, (x, y))

def show_ast_window(ast_root):
    win = tk.Toplevel()
    win.title("Árbol Sintáctico")
    canvas = tk.Canvas(win, width=800, height=600, bg='white')
    canvas.pack(fill=tk.BOTH, expand=True)
    draw_ast(canvas, ast_root, 400, 40, 150, 80)
