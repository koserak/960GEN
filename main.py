import tkinter as tk
from PIL import Image, ImageTk
import chess
import random
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

PIECE_FOLDER = resource_path("pieces")
SQUARE_SIZE = 45
COLUMNS = 3  # Cuántos tableros por fila

# Cargar imágenes PNG
def load_piece_images():
    images = {}
    for piece_code in ['K','Q','R','B','N','P']:
        for color in ['w', 'b']:
            filename = os.path.join(PIECE_FOLDER, f"{color}{piece_code}.png")
            if os.path.exists(filename):
                image = Image.open(filename).resize((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.LANCZOS)
                images[f"{color}{piece_code}"] = ImageTk.PhotoImage(image)
            else:
                print(f"⚠️ No se encontró la imagen: {filename}")
    return images

# Dibujar un tablero en un canvas
def draw_board(canvas, board, piece_images):
    margin_left = 15   # espacio para números fila
    margin_bottom = 15 # espacio para letras columna
    board_size = 8 * SQUARE_SIZE

    canvas.config(width=board_size + margin_left, height=board_size + margin_bottom)

    # Dibujar fondo de tablero con margen
    canvas.create_rectangle(0, 0, board_size + margin_left, board_size + margin_bottom, fill="white", outline="")

    # Dibujar casillas y piezas
    for rank in range(8):
        for file in range(8):
            square = chess.square(file, 7 - rank)
            piece = board.piece_at(square)

            x = margin_left + file * SQUARE_SIZE
            y = rank * SQUARE_SIZE

            color = "#EEEED2" if (file + rank) % 2 == 0 else "#769656"
            canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=color)

            if piece:
                key = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().upper()}"
                img = piece_images.get(key)
                if img:
                    canvas.create_image(x, y, anchor='nw', image=img)

    # Letras columnas (A-H)
    letras = ['A','B','C','D','E','F','G','H']
    for i, letra in enumerate(letras):
        x = margin_left + i * SQUARE_SIZE + SQUARE_SIZE / 2
        y = board_size + 10
        canvas.create_text(x, y, text=letra, font=("Arial", 8))

    # Números filas (8-1) a la izquierda (de arriba abajo)
    numeros = list(range(8, 0, -1))
    for i, num in enumerate(numeros):
        x = margin_left / 2
        y = i * SQUARE_SIZE + SQUARE_SIZE / 2
        canvas.create_text(x, y, text=str(num), font=("Arial", 8))


# Generar y mostrar múltiples tableros
def generar_tableros():
    try:
        n = int(entry.get())
        if n < 1 or n > 128:
            entry.delete(0, tk.END)
            entry.insert(0, "1" if n < 1 else "128")
            return
    except ValueError:
        return


    for widget in tablero_frame.winfo_children():
        widget.destroy()

    for i in range(n):
        seed = random.randint(0, 959)
        board = chess.Board.from_chess960_pos(seed)

        canvas = tk.Canvas(tablero_frame, width=8*SQUARE_SIZE, height=8*SQUARE_SIZE)
        draw_board(canvas, board, piece_images)

        tk.Label(tablero_frame, text=f"Tablero {i+1} (#{seed})").grid(row=i // COLUMNS * 2, column=i % COLUMNS, pady=(10, 0))
        canvas.grid(row=i // COLUMNS * 2 + 1, column=i % COLUMNS, padx=10, pady=5)

# --- GUI ---
root = tk.Tk()
root.iconbitmap(resource_path("icono.ico"))
root.title("960GEN")

entry_label = tk.Label(root, text="¿Cuántos tableros quieres generar?")
entry_label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

generate_button = tk.Button(root, text="Generar", command=generar_tableros)
generate_button.pack(pady=5)

scroll_canvas = tk.Canvas(root, width=8*SQUARE_SIZE*COLUMNS + 50, height=600)
scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)

tablero_frame = tk.Frame(scroll_canvas)
scroll_canvas.create_window((0, 0), window=tablero_frame, anchor="nw")

def on_configure(event):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

def _on_mousewheel(event):
    scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

tablero_frame.bind("<Configure>", on_configure)


# Cargar imágenes PNG
piece_images = load_piece_images()

# Mostrar al inicio
#generar_tableros()
root.mainloop()
