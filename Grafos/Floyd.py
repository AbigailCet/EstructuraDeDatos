# -*- coding: utf-8 -*-
"""
Floyd-Warshall interactivo con:
- Matriz de distancias D(k)
- Matriz de recorridos P(k)
- Marcas de celdas que cambian en cada paso (*)
- Búsqueda de camino mínimo entre dos nodos y resaltado en el grafo

Requisitos:
    pip install matplotlib networkx
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import networkx as nx
import math


class FloydApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Floyd-Warshall interactivo (D, P y caminos)")

        # Grafo y estado
        self.G = nx.Graph()
        self.pos = {}
        self.nodes = []       # lista ordenada de nodos
        self.steps = []       # lista de pasos del algoritmo
        self.current_step = -1

        # Para resaltar un camino final
        self.highlight_path_nodes = set()
        self.highlight_path_edges = []

        self._create_widgets()
        self._create_matplotlib_canvas()

    # -----------------------------------------------------------
    # UI
    # -----------------------------------------------------------
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo: controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Panel derecho: grafo
        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.graph_frame = graph_frame

        # Nodos
        ttk.Label(controls_frame, text="Nodos (separados por comas):").pack(anchor="w")
        self.entry_nodes = ttk.Entry(controls_frame, width=30)
        self.entry_nodes.insert(0, "A,B,C,D,E")
        self.entry_nodes.pack(anchor="w", pady=(0, 5))

        # Aristas
        ttk.Label(
            controls_frame,
            text="Aristas (una por línea: origen destino peso):"
        ).pack(anchor="w")
        self.text_edges = ScrolledText(controls_frame, width=30, height=8)
        example_edges = """A B 4
A C 2
B C 1
B D 5
C D 8
C E 10
D E 2"""
        self.text_edges.insert("1.0", example_edges)
        self.text_edges.pack(anchor="w", pady=(0, 5))

        # Botón construir grafo
        ttk.Button(
            controls_frame,
            text="Construir grafo",
            command=self.build_graph
        ).pack(fill=tk.X, pady=(0, 10))

        # Botones Floyd
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X, pady=(5, 5))

        ttk.Button(
            buttons_frame,
            text="Iniciar Floyd",
            command=self.start_floyd
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(
            buttons_frame,
            text="Reiniciar",
            command=self.reset_steps
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Paso siguiente
        ttk.Button(
            controls_frame,
            text="Paso siguiente",
            command=self.next_step
        ).pack(fill=tk.X, pady=(5, 10))

        # Área de texto (matrices)
        ttk.Label(controls_frame, text="Matrices D(k) y P(k):").pack(anchor="w")
        self.text_state = ScrolledText(controls_frame, width=60, height=30)
        self.text_state.configure(font=("Courier New", 10))  # monoespaciada
        self.text_state.pack(anchor="w", pady=(0, 5))

        # ---- Consulta de camino mínimo final ----
        path_frame = ttk.LabelFrame(controls_frame, text="Camino mínimo (final)")
        path_frame.pack(fill=tk.X, pady=(5, 5))

        ttk.Label(path_frame, text="Origen:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.combo_src = ttk.Combobox(path_frame, width=5, state="readonly")
        self.combo_src.grid(row=0, column=1, padx=2, pady=2)

        ttk.Label(path_frame, text="Destino:").grid(row=0, column=2, sticky="w", padx=2, pady=2)
        self.combo_dst = ttk.Combobox(path_frame, width=5, state="readonly")
        self.combo_dst.grid(row=0, column=3, padx=2, pady=2)

        ttk.Button(
            path_frame,
            text="Mostrar camino mínimo",
            command=self.show_shortest_path
        ).grid(row=1, column=0, columnspan=4, sticky="ew", padx=2, pady=4)

    def _create_matplotlib_canvas(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # -----------------------------------------------------------
    # Construcción del grafo
    # -----------------------------------------------------------
    def build_graph(self):
        self.G.clear()
        self.steps.clear()
        self.current_step = -1
        self.nodes = []
        self.highlight_path_nodes.clear()
        self.highlight_path_edges = []

        # Leer nodos
        nodes_text = self.entry_nodes.get().strip()
        if not nodes_text:
            messagebox.showerror("Error", "Debes ingresar al menos un nodo.")
            return

        nodes = [n.strip() for n in nodes_text.split(",") if n.strip()]
        if not nodes:
            messagebox.showerror("Error", "La lista de nodos no es válida.")
            return

        self.nodes = sorted(nodes)
        self.G.add_nodes_from(self.nodes)

        # Actualizar combos de origen/destino
        self.combo_src["values"] = self.nodes
        self.combo_dst["values"] = self.nodes
        if self.nodes:
            self.combo_src.set(self.nodes[0])
            self.combo_dst.set(self.nodes[-1])

        # Leer aristas
        edges_text = self.text_edges.get("1.0", tk.END).strip()
        if not edges_text:
            messagebox.showerror("Error", "Debes ingresar al menos una arista.")
            return

        for line in edges_text.splitlines():
            parts = line.split()
            if len(parts) != 3:
                messagebox.showerror(
                    "Error",
                    f"La línea '{line}' no tiene formato 'u v peso'."
                )
                return
            u, v, w = parts
            if u not in self.nodes or v not in self.nodes:
                messagebox.showerror(
                    "Error",
                    f"Los nodos '{u}' o '{v}' de la línea '{line}' no están en la lista de nodos."
                )
                return
            try:
                w_val = float(w)
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"El peso '{w}' en la línea '{line}' no es un número."
                )
                return

            self.G.add_edge(u, v, weight=w_val)

        # Posiciones del grafo
        if len(self.G.nodes) > 1:
            self.pos = nx.spring_layout(self.G, seed=42)
        else:
            self.pos = {self.nodes[0]: (0, 0)}

        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Grafo construido correctamente.\n")

    # -----------------------------------------------------------
    # Floyd-Warshall paso a paso
    # -----------------------------------------------------------
    def start_floyd(self):
        if self.G.number_of_nodes() == 0:
            messagebox.showerror("Error", "Primero construye un grafo.")
            return

        self.steps = self._compute_floyd_steps()
        if not self.steps:
            messagebox.showinfo("Información", "No se pudieron generar pasos.")
            return

        self.current_step = 0
        self.show_current_step()

    def reset_steps(self):
        self.steps.clear()
        self.current_step = -1
        self.highlight_path_nodes.clear()
        self.highlight_path_edges = []
        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Estados reiniciados.\n")

    def next_step(self):
        if not self.steps:
            messagebox.showinfo(
                "Información",
                "Primero inicia Floyd (botón 'Iniciar Floyd')."
            )
            return

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            messagebox.showinfo(
                "Información",
                "Ya estás en el último paso."
            )

    def _compute_floyd_steps(self):
        """
        Genera pasos para Floyd-Warshall con:
        - dist: matriz de distancias
        - path: matriz de recorridos (siguiente nodo desde i para ir a j)
        """
        n = len(self.nodes)
        index = {node: i for i, node in enumerate(self.nodes)}

        # Matriz de distancias inicial
        dist = [[math.inf] * n for _ in range(n)]
        path = [["-"] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0.0
            path[i][i] = "-"

        for u, v, data in self.G.edges(data=True):
            w = data.get("weight", 1.0)
            i, j = index[u], index[v]
            if w < dist[i][j]:
                dist[i][j] = w
                dist[j][i] = w
                path[i][j] = v
                path[j][i] = u

        steps = []

        # Paso 0: matrices iniciales D(0), P(0)
        steps.append({
            "action": "init",
            "k_index": None,
            "k_node": None,
            "dist": [row[:] for row in dist],
            "path": [row[:] for row in path],
            "updates": []
        })

        # Floyd-Warshall
        for k in range(n):
            k_node = self.nodes[k]
            updates = []

            for i in range(n):
                for j in range(n):
                    old_d = dist[i][j]
                    old_p = path[i][j]

                    via_k = dist[i][k] + dist[k][j]

                    if via_k < old_d:
                        dist[i][j] = via_k
                        # nuevo recorrido: primer salto desde i hacia j
                        path[i][j] = path[i][k]
                        updates.append({
                            "i": self.nodes[i],
                            "j": self.nodes[j],
                            "old_d": old_d,
                            "new_d": via_k,
                            "old_p": old_p,
                            "new_p": path[i][j],
                            "via": k_node,
                            "changed": True
                        })
                    else:
                        updates.append({
                            "i": self.nodes[i],
                            "j": self.nodes[j],
                            "old_d": old_d,
                            "new_d": via_k,
                            "old_p": old_p,
                            "new_p": old_p,
                            "via": k_node,
                            "changed": False
                        })

            steps.append({
                "action": "k_step",
                "k_index": k,
                "k_node": k_node,
                "dist": [row[:] for row in dist],
                "path": [row[:] for row in path],
                "updates": updates
            })

        return steps

    # -----------------------------------------------------------
    # Visualización
    # -----------------------------------------------------------
    def show_current_step(self):
        step = self.steps[self.current_step]
        self.draw_graph(step)
        self.update_state_text(step)

    def draw_graph(self, step=None):
        self.ax.clear()

        if not self.pos:
            self.canvas.draw()
            return

        current_k_node = None
        if step is not None:
            current_k_node = step["k_node"]

        # Colores de nodos: si están en el camino final → verde,
        # si son el k actual → naranja, si no → azul.
        node_colors = []
        for n in self.nodes:
            if n in self.highlight_path_nodes:
                node_colors.append("#4caf50")  # verde camino final
            elif n == current_k_node:
                node_colors.append("#ff9800")  # k
            else:
                node_colors.append("#90caf9")  # otros

        nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax)

        # Todas las aristas base en gris
        nx.draw_networkx_edges(self.G, self.pos, edge_color="#9e9e9e", ax=self.ax)

        # Pesos
        edge_labels = {(u, v): f'{d["weight"]}' for u, v, d in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        # Aristas del camino final resaltadas en rojo
        if self.highlight_path_edges:
            nx.draw_networkx_edges(
                self.G,
                self.pos,
                edgelist=self.highlight_path_edges,
                width=4,
                edge_color="#f44336",
                ax=self.ax
            )

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    # -----------------------------------------------------------
    # Mostrar matrices D(k) y P(k) y cambios
    # -----------------------------------------------------------
    def update_state_text(self, step):
        self.text_state.delete("1.0", tk.END)

        action = step["action"]
        dist = step["dist"]
        path = step["path"]
        n = len(self.nodes)
        width = 6

        # Pares (i,j) que cambiaron en este paso
        changed_pairs = set()
        for upd in step["updates"]:
            if upd["changed"]:
                changed_pairs.add((upd["i"], upd["j"]))

        # Encabezado
        if action == "init":
            self.text_state.insert(tk.END, "D(0), P(0): matrices iniciales\n\n")
        else:
            k_node = step["k_node"]
            k_index = step["k_index"]
            self.text_state.insert(
                tk.END,
                f"D({k_index + 1}), P({k_index + 1}): usando k = {k_node}\n\n"
            )

        # MATRIZ DE DISTANCIAS
        self.text_state.insert(tk.END, "MATRIZ DE DISTANCIAS D(k)\n")
        header = " " * width
        for node in self.nodes:
            header += f"{node:>{width}}"
        self.text_state.insert(tk.END, header + "\n")

        for i in range(n):
            row_str = f"{self.nodes[i]:>{width}}"
            for j in range(n):
                d = dist[i][j]
                if d == math.inf:
                    cell = "∞"
                else:
                    cell = f"{d:.0f}"
                if (self.nodes[i], self.nodes[j]) in changed_pairs:
                    cell = cell + "*"
                row_str += f"{cell:>{width}}"
            self.text_state.insert(tk.END, row_str + "\n")

        # MATRIZ DE RECORRIDOS
        self.text_state.insert(tk.END, "\nMATRIZ DE RECORRIDOS P(k)\n")
        header = " " * width
        for node in self.nodes:
            header += f"{node:>{width}}"
        self.text_state.insert(tk.END, header + "\n")

        for i in range(n):
            row_str = f"{self.nodes[i]:>{width}}"
            for j in range(n):
                cell = path[i][j]
                if (self.nodes[i], self.nodes[j]) in changed_pairs:
                    cell = cell + "*"
                row_str += f"{cell:>{width}}"
            self.text_state.insert(tk.END, row_str + "\n")

        # Lista de cambios
        if action == "k_step":
            self.text_state.insert(tk.END, "\nCambios en este paso:\n")
            any_change = False
            for upd in step["updates"]:
                if upd["changed"]:
                    any_change = True
                    old_d = "∞" if upd["old_d"] == math.inf else f"{upd['old_d']:.0f}"
                    new_d = "∞" if upd["new_d"] == math.inf else f"{upd['new_d']:.0f}"
                    self.text_state.insert(
                        tk.END,
                        f"  dist[{upd['i']}][{upd['j']}]: {old_d} → {new_d} (vía {upd['via']}) | "
                        f"recorrido: {upd['old_p']} → {upd['new_p']}\n"
                    )
            if not any_change:
                self.text_state.insert(
                    tk.END,
                    "  No hubo cambios de distancias al usar este k.\n"
                )

    # -----------------------------------------------------------
    # Camino mínimo entre dos nodos (usando el último paso)
    # -----------------------------------------------------------
    def show_shortest_path(self):
        if not self.steps:
            messagebox.showinfo(
                "Información",
                "Primero ejecuta Floyd (botón 'Iniciar Floyd')."
            )
            return

        src = self.combo_src.get().strip()
        dst = self.combo_dst.get().strip()

        if src not in self.nodes or dst not in self.nodes:
            messagebox.showerror(
                "Error",
                "Origen y destino deben ser nodos válidos."
            )
            return

        final_step = self.steps[-1]
        dist = final_step["dist"]
        path = final_step["path"]
        n = len(self.nodes)
        index = {node: i for i, node in enumerate(self.nodes)}

        i = index[src]
        j = index[dst]

        if math.isinf(dist[i][j]):
            messagebox.showinfo(
                "Camino",
                f"No existe camino entre {src} y {dst}."
            )
            return

        # Reconstruir camino usando la matriz de recorridos (next-hop)
        route = [src]
        current = src
        max_iter = n + 5  # seguridad por si acaso
        steps_used = 0

        while current != dst and steps_used < max_iter:
            ci = index[current]
            next_node = path[ci][j]
            if next_node == "-" or next_node not in index:
                break
            route.append(next_node)
            current = next_node
            steps_used += 1

        if route[-1] != dst:
            messagebox.showinfo(
                "Camino",
                f"No se pudo reconstruir completamente el camino de {src} a {dst}."
            )
            return

        # Actualizar resaltado en grafo
        self.highlight_path_nodes = set(route)
        self.highlight_path_edges = []
        for u, v in zip(route, route[1:]):
            if self.G.has_edge(u, v):
                self.highlight_path_edges.append((u, v))
            elif self.G.has_edge(v, u):
                self.highlight_path_edges.append((v, u))

        # Redibujar grafo con el camino resaltado
        # (usamos el último paso para conservar el color de k, aunque ya no importe mucho)
        self.draw_graph(self.steps[self.current_step])

        # Mostrar camino y distancia en el cuadro de texto
        total_dist = dist[i][j]
        self.text_state.insert(
            tk.END,
            f"\nCamino mínimo de {src} a {dst}:  " +
            " → ".join(route) +
            f"   |  distancia = {total_dist:.0f}\n"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = FloydApp(root)
    root.mainloop()
