"""UI von Jonathan Alexander Greive"""
import tkinter as tk
from tkinter import ttk
import os
import urllib.request
import datetime
import glob

from controller import parse, a_star

# Moderne Farbpalette
CELL_COLORS = {
    'S': '#4CAF50',  # Grün
    'E': '#F44336',  # Rot
    '#': '#2C3E50',  # Dunkles Blau-Grau (Hindernis)
    'D': '#7F8C8D',  # Dunkles Grau
    'H': '#BDC3C7',  # Helles Grau
    '.': '#FFFFFF'  # Weiß
}

# Beschreibungen für die Legende (inklusive der genannten Kosten zur Info)
CELL_TEXT = {
    'S': 'Start',
    'E': 'Ziel',
    '#': 'Hindernis (unpassierbar)',
    'D': 'Dunkelgrau (Kosten: 10)',
    'H': 'Hellgrau (Kosten: 4)',
    '.': 'Frei (Kosten: 1)'
}

# Moderne Fonts
FONT_MAIN = ("Segoe UI", 12, "bold")
FONT_AXIS = ("Segoe UI", 10, "bold")
FONT_LEGEND = ("Segoe UI", 11)


def get_gradient_color(cost, min_cost, max_cost):
    """Erzeugt einen Farbgradienten von Hellblau nach Dunkelblau."""
    if max_cost == min_cost:
        return '#ADD8E6', 'black'

    ratio = (cost - min_cost) / (max_cost - min_cost)

    # RGB von Hellblau (173, 216, 230) nach Dunkelblau (10, 36, 106)
    r = int(173 + ratio * (10 - 173))
    g = int(216 + ratio * (36 - 216))
    b = int(230 + ratio * (106 - 230))

    hex_color = f'#{r:02x}{g:02x}{b:02x}'
    text_color = "white" if ratio > 0.5 else "black"  # Textfarbe für Lesbarkeit anpassen

    return hex_color, text_color


def draw_maze(parent, grid):
    """Zeichnet das Labyrinth als Raster von Labels im modernen Look."""
    maze_frame = tk.Frame(parent, bg="#DFE6E9")  # Container Background für saubere Gridlines
    maze_frame.pack(side=tk.TOP, padx=30, pady=(30, 10), anchor="w")

    # X-Koordinaten am oberen Rand
    for c in range(len(grid[0])):
        tk.Label(maze_frame, text=str(c), fg="#2980B9", bg="#DFE6E9", font=FONT_AXIS).grid(row=0, column=c + 1,
                                                                                           pady=(0, 5))

    label_grid = []
    for r, row in enumerate(grid):
        # Y-Koordinaten am linken Rand
        tk.Label(maze_frame, text=str(r), fg="#2980B9", bg="#DFE6E9", font=FONT_AXIS).grid(row=r + 1, column=0,
                                                                                           padx=(0, 5))

        label_row = []
        for c, cell in enumerate(row):
            color = CELL_COLORS.get(cell, '#FFFFFF')
            text_color = "white" if cell in ['#', 'D'] else "#2C3E50"

            # highlightthickness=3 reserviert Platz für den farbigen Rahmen (Hover-Effekt)
            lbl = tk.Label(maze_frame, text=cell, bg=color, fg=text_color,
                           width=4, height=2, relief="flat", font=FONT_MAIN,
                           highlightthickness=3, highlightbackground="#DFE6E9")
            # 1px Abstand sorgt dafür, dass der Frame-Hintergrund als Linien durchscheint (Grid-Look)
            lbl.grid(row=r + 1, column=c + 1, padx=1, pady=1)
            label_row.append(lbl)
        label_grid.append(label_row)
    return label_grid, maze_frame


def draw_legend(parent):
    """Zeichnet die Legende neben das Labyrinth."""
    legend_frame = tk.Frame(parent, bg="#F8F9FA")
    legend_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 20))

    tk.Label(legend_frame, text="Legende", font=('Segoe UI', 16, 'bold'), bg="#F8F9FA", fg="#2C3E50").pack(pady=(0, 15),
                                                                                                           anchor="w")

    for key, color in CELL_COLORS.items():
        row_frame = tk.Frame(legend_frame, bg="#F8F9FA")
        row_frame.pack(fill=tk.X, pady=4)

        text_color = "white" if key in ['#', 'D'] else "#2C3E50"

        # Farbbox
        tk.Label(row_frame, text=key, bg=color, fg=text_color,
                 width=3, height=1, relief="flat",
                 font=FONT_MAIN).pack(side=tk.LEFT, padx=(0, 15))

        # Beschreibung
        tk.Label(row_frame, text=CELL_TEXT[key], font=FONT_LEGEND, bg="#F8F9FA", fg="#2C3E50").pack(side=tk.LEFT)

    # Trennlinie
    tk.Frame(legend_frame, height=2, bg="#DFE6E9").pack(fill=tk.X, pady=15)

    # Legende: A* Pfad
    row_frame = tk.Frame(legend_frame, bg="#F8F9FA")
    row_frame.pack(fill=tk.X, pady=4)
    tk.Label(row_frame, text="*", bg="#F1C40F", fg="#2C3E50",
             width=3, height=1, relief="flat",
             font=FONT_MAIN).pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(row_frame, text="A* Pfad", font=FONT_LEGEND, bg="#F8F9FA", fg="#2C3E50").pack(side=tk.LEFT)

    # Legende: Hover-Rahmen
    row_frame = tk.Frame(legend_frame, bg="#F8F9FA")
    row_frame.pack(fill=tk.X, pady=4)
    lbl_hover = tk.Label(row_frame, text=" ", bg="#ADD8E6", fg="#2C3E50", width=3, height=1, relief="flat",
                         font=FONT_MAIN, highlightthickness=3, highlightbackground="#FF3366")
    lbl_hover.pack(side=tk.LEFT, padx=0)
    tk.Label(row_frame, text="  Hover Pfad zum Start", font=FONT_LEGEND, bg="#F8F9FA", fg="#2C3E50").pack(side=tk.LEFT)

    # Legende: A* Graph Gradient
    row_frame = tk.Frame(legend_frame, bg="#F8F9FA")
    row_frame.pack(fill=tk.X, pady=10)

    # Zeige einen kleinen Gradienten in der Legende
    grad_frame = tk.Frame(row_frame, bg="#F8F9FA")
    grad_frame.pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(grad_frame, text=" 0", bg="#ADD8E6", fg="black", width=2, relief="flat", font=("Segoe UI", 9)).pack(
        side=tk.LEFT)
    tk.Label(grad_frame, text="99", bg="#0a246a", fg="white", width=2, relief="flat", font=("Segoe UI", 9)).pack(
        side=tk.LEFT)

    tk.Label(row_frame, text="A* Graph (G-Kosten)", font=FONT_LEGEND, bg="#F8F9FA", fg="#2C3E50").pack(side=tk.LEFT)

    return legend_frame


def create_btn(parent, text, cmd, bg_col, fg_col="#2C3E50"):
    """Hilfsfunktion für moderne Buttons."""
    btn = tk.Button(parent, text=text, command=cmd, font=('Segoe UI', 11, 'bold'),
                    bg=bg_col, fg=fg_col, relief="flat",
                    activebackground="#BDC3C7", cursor="hand2", padx=20, pady=8)
    return btn


def load_raw_grid_for_ui(filepath):
    """Liest die txt-Datei nur für die optische Darstellung als 2D-Liste ein."""
    raw_grid = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip() == "" or line.startswith("Legend:"):
                break
            raw_grid.append(line.split())
    return raw_grid


def start_ui(default_filepath):
    """Startet die Tkinter-basierte Benutzeroberfläche."""
    root = tk.Tk()
    root.title("A* Labyrinth Solver")

    root.geometry("900x750")

    root.resizable(True, True)
    root.config(bg="#F8F9FA")  # Heller, sauberer Hintergrund

    # Container für Top-Bar (Dropdown & Download)
    top_frame = tk.Frame(root, bg="#DFE6E9", pady=10, padx=20)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # State mapping für Dateipfade
    maze_files = {"Standard Labyrinth": default_filepath}
    mazes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mazes")
    os.makedirs(mazes_dir, exist_ok=True)

    def refresh_maze_list():
        files = sorted(glob.glob(os.path.join(mazes_dir, "*.txt")))
        for f in files:
            name = os.path.basename(f)
            maze_files[name] = f
        combo['values'] = list(maze_files.keys())

    tk.Label(top_frame, text="Labyrinth auswählen:", font=FONT_LEGEND, bg="#DFE6E9", fg="#2C3E50").pack(side=tk.LEFT,
                                                                                                        padx=(0, 10))

    combo_var = tk.StringVar()
    combo = ttk.Combobox(top_frame, textvariable=combo_var, state="readonly", font=FONT_LEGEND, width=30)
    combo.pack(side=tk.LEFT)

    # Restliche UI Container
    main_content = tk.Frame(root, bg="#F8F9FA")
    main_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    left_col = tk.Frame(main_content, bg="#F8F9FA")
    left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    right_col = tk.Frame(main_content, bg="#F8F9FA")
    # Hier side=tk.LEFT und anchor="nw" verwenden, damit die Spalte direkt rechts ans Grid rückt und linksbündig abschließt.
    right_col.pack(side=tk.LEFT, fill=tk.Y, anchor="nw", padx=(0, 30), pady=30)

    maze_container = tk.Frame(left_col, bg="#F8F9FA")
    maze_container.pack(side=tk.TOP, anchor="w")

    button_frame = tk.Frame(left_col, bg="#F8F9FA")
    button_frame.pack(side=tk.TOP, anchor="w", padx=30, pady=(0, 20))

    legend_container = tk.Frame(right_col, bg="#F8F9FA")
    legend_container.pack(side=tk.TOP, fill=tk.X)

    info_frame = tk.Frame(right_col, bg="#F8F9FA")
    info_label = tk.Label(info_frame, text="Pfad-Koordinaten:", font=FONT_LEGEND, bg="#F8F9FA", fg="#2C3E50")
    info_label.pack(anchor="w")
    path_text = tk.Text(info_frame, height=5, width=30, font=("Consolas", 10), bg="#DFE6E9", fg="#2C3E50",
                        relief="flat", wrap=tk.WORD)
    path_text.pack(fill=tk.X, pady=(5, 0))

    def prevent_typing(event):
        if event.state & 4 and event.keysym.lower() in ['c', 'a']: return None
        if event.keysym in ['Left', 'Right', 'Up', 'Down', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R']: return None
        return "break"

    path_text.bind("<Key>", prevent_typing)

    # Globale Referenzen für dynamisches Neuladen
    current_widgets = {}
    current_state = {"grid": None, "path": None, "explored": None, "g_scores": None, "mode": "grid"}
    hovered_path_cells = []

    def clear_hover_borders():
        if "label_grid" in current_widgets:
            for (hx, hy) in hovered_path_cells:
                current_widgets["label_grid"][hy][hx].config(highlightbackground="#DFE6E9")
        hovered_path_cells.clear()

    def update_path_text(text):
        path_text.delete("1.0", tk.END)
        path_text.insert(tk.END, text)

    def load_selected(event=None):
        selection = combo_var.get()
        if selection in maze_files:
            filepath = maze_files[selection]
            load_maze_into_ui(filepath)

    combo.bind("<<ComboboxSelected>>", load_selected)

    def load_maze_into_ui(filepath):
        # Altes abräumen
        if "maze_frame" in current_widgets: current_widgets["maze_frame"].destroy()
        if "legend_frame" in current_widgets: current_widgets["legend_frame"].destroy()
        clear_hover_borders()
        update_path_text("")
        info_frame.pack_forget()

        # --- ANPASSUNG AN IHREN CONTROLLER ---
        grid = load_raw_grid_for_ui(filepath)
        maze_dict, start_pos, end_pos = parse(filepath)

        # Aufruf des A* Algorithmus aus Ihrem Controller
        path, g_scores, explored_nodes = a_star(maze_dict, start_pos, end_pos)

        current_state.update(
            {"grid": grid, "path": path, "explored": explored_nodes, "g_scores": g_scores, "mode": "grid"})

        # UI Elemente erstellen
        label_grid, maze_frame = draw_maze(maze_container, grid)
        legend_frame = draw_legend(legend_container)

        current_widgets["label_grid"] = label_grid
        current_widgets["maze_frame"] = maze_frame
        current_widgets["legend_frame"] = legend_frame

        # Min/Max f. Gradient
        valid_g = [g for pos, g in g_scores.items() if grid[pos[1]][pos[0]] not in ['S', 'E']]
        current_state["min_g"] = min(valid_g) if valid_g else 0
        current_state["max_g"] = max(valid_g) if valid_g else 1

        def on_enter_cell(event, x, y):
            if current_state["mode"] != "graph": return
            if (x, y) in explored_nodes:
                clear_hover_borders()
                curr_node = explored_nodes[(x, y)]
                while curr_node is not None:
                    cx, cy = curr_node.position
                    hovered_path_cells.append((cx, cy))
                    label_grid[cy][cx].config(highlightbackground="#FF3366")
                    curr_node = curr_node.parent

        def on_leave_cell(event, x, y):
            if current_state["mode"] == "graph": clear_hover_borders()

        for y, row in enumerate(label_grid):
            for x, lbl in enumerate(row):
                lbl.bind("<Enter>", lambda e, cx=x, cy=y: on_enter_cell(e, cx, cy))
                lbl.bind("<Leave>", lambda e, cx=x, cy=y: on_leave_cell(e, cx, cy))

    def reset_grid():
        if not current_state["grid"]: return
        current_state["mode"] = "grid"
        clear_hover_borders()
        update_path_text("")
        info_frame.pack_forget()
        grid = current_state["grid"]
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                color = CELL_COLORS.get(cell, '#FFFFFF')
                text_color = "white" if cell in ['#', 'D'] else "#2C3E50"
                current_widgets["label_grid"][y][x].config(bg=color, text=cell, fg=text_color)

    def show_path():
        reset_grid()
        if not current_state["path"]: return
        current_state["mode"] = "path"
        path = current_state["path"]
        grid = current_state["grid"]

        goal_x, goal_y = path[-1]

        # --- ANPASSUNG FÜR TUPEL-ABFRAGE ---
        total_cost = current_state["g_scores"].get((goal_x, goal_y), 0)

        info_label.config(text=f"Gefundener Pfad (Gesamtkosten: {total_cost}):")
        info_frame.pack(side=tk.TOP, fill=tk.X)

        path_str = " -> ".join([f"({x},{y})" for (x, y) in path])
        update_path_text(path_str)
        for (x, y) in path:
            if grid[y][x] not in ['S', 'E']:
                current_widgets["label_grid"][y][x].config(bg='#F1C40F', text='*', fg='#2C3E50')

    def show_graph():
        reset_grid()
        if not current_state["explored"]: return
        current_state["mode"] = "graph"
        for (x, y), node in current_state["explored"].items():
            if current_state["grid"][y][x] not in ['S', 'E']:

                # --- ANPASSUNG FÜR TUPEL-ABFRAGE ---
                cost_val = current_state["g_scores"].get((x, y))

                if cost_val is not None:
                    bg_color, fg_color = get_gradient_color(cost_val, current_state["min_g"], current_state["max_g"])
                    current_widgets["label_grid"][y][x].config(bg=bg_color, text=str(cost_val), fg=fg_color)

    btn_grid = create_btn(button_frame, "Grid (Reset)", reset_grid, "#DFE6E9")
    btn_grid.pack(side=tk.LEFT, padx=10)

    btn_path = create_btn(button_frame, "A* Path", show_path, "#F1C40F")
    btn_path.pack(side=tk.LEFT, padx=10)

    btn_graph = create_btn(button_frame, "A* Graph", show_graph, "#ADD8E6")
    btn_graph.pack(side=tk.LEFT, padx=10)

    # Initialen Zustand laden
    refresh_maze_list()
    combo_var.set("Standard Labyrinth")
    load_maze_into_ui(default_filepath)

    root.mainloop()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    maze_path = os.path.join(current_dir, "maze_with_legend.txt")
    start_ui(maze_path)