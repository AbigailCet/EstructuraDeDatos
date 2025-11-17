# -*- coding: utf-8 -*-
"""
Algoritmo de Warshall interactivo (cierre transitivo) estilo "video teórico":

- Entrada: grafo DIRIGIDO (A B = arista A -> B)
- W0 = R inicial (más la diagonal)
- W(k+1)[i][j] = Wk[i][j] OR (Wk[i][k] AND Wk[k][j])

Interfaz:
- Grafo dirigido en un panel mediano.
- Panel grande para:
  - Wk (matriz de 0/1) con fila k y columna k marcadas.
  - Relación original R (pares que vienen de la entrada).
  - Relación R_k (pares actuales).
  - Pares nuevos = R_k \ R (lo que se va formando con Warshall).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import networkx as nx


class WarshallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Warshall interactivo (Wk y pares)")

        # Grafo dirigido y estado del algoritmo
        self.G = nx.DiGraph()
        self.pos = {}
        self.nodes = []
        self.steps = []          # lista de pasos Wk
        self.current_step = -1

        # Pares originales de la relación (entrada)
        self.original_pairs = set()

        self._create_widgets()
        self._create_matplotlib_canvas()

    # -----------------------------------------------------------
    # UI
    # -----------------------------------------------------------
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo: controles + matrices (más ancho)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Panel derecho: grafo (tamaño medio)
        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.graph_frame = graph_frame

        # ----- Controles arriba -----
        ttk.Label(controls_frame, text="Nodos (separados por comas):").pack(anchor="w")
        self.entry_nodes = ttk.Entry(controls_frame, width=40)
        self.entry_nodes.insert(0, "A,B,C,D,E")
        self.entry_nodes.pack(anchor="w", pady=(0, 5))

        ttk.Label(
            controls_frame,
            text="Aristas dirigidas (una por línea: origen destino):"
        ).pack(anchor="w")
        self.text_edges = ScrolledText(controls_frame, width=40, height=6)
        example_edges = """A E
B A
D B
E D"""
        self.text_edges.insert("1.0", example_edges)
        self.text_edges.pack(anchor="w", pady=(0, 5))

        ttk.Button(
            controls_frame,
            text="Construir grafo dirigido",
            command=self.build_graph
        ).pack(fill=tk.X, pady=(0, 8))

        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X, pady=(5, 5))

        ttk.Button(
            buttons_frame,
            text="Iniciar Warshall",
            command=self.start_warshall
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(
            buttons_frame,
            text="Reiniciar",
            command=self.reset_steps
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        ttk.Button(
            controls_frame,
            text="Paso siguiente",
            command=self.next_step
        ).pack(fill=tk.X, pady=(5, 8))

        # ----- Matriz grande abajo -----
        ttk.Label(controls_frame, text="Matrices Wk y relación R_k:").pack(anchor="w")
        self.text_state = ScrolledText(controls_frame, width=85, height=20)
        self.text_state.configure(font=("Courier New", 10))  # monoespaciada
        self.text_state.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

    def _create_matplotlib_canvas(self):
        # Grafo de tamaño medio, bien visible
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
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
        self.original_pairs.clear()

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

        edges_text = self.text_edges.get("1.0", tk.END).strip()
        if not edges_text:
            messagebox.showerror("Error", "Debes ingresar al menos una arista.")
            return

        for line in edges_text.splitlines():
            parts = line.split()
            if len(parts) != 2:
                messagebox.showerror(
                    "Error",
                    f"La línea '{line}' no tiene formato 'origen destino'."
                )
                return
            u, v = parts
            if u not in self.nodes or v not in self.nodes:
                messagebox.showerror(
                    "Error",
                    f"Los nodos '{u}' o '{v}' de la línea '{line}' no están en la lista de nodos."
                )
                return
            self.G.add_edge(u, v)  # u -> v
            # par original de la relación de entrada
            self.original_pairs.add((u, v))

        # También consideramos la diagonal como parte de la relación base
        for x in self.nodes:
            self.original_pairs.add((x, x))

        # Distribución circular para aprovechar bien el espacio
        if len(self.G.nodes) > 1:
            self.pos = nx.circular_layout(self.G)
        else:
            self.pos = {self.nodes[0]: (0, 0)}

        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Grafo dirigido construido correctamente.\n")

    # -----------------------------------------------------------
    # Warshall paso a paso
    # -----------------------------------------------------------
    def start_warshall(self):
        if self.G.number_of_nodes() == 0:
            messagebox.showerror("Error", "Primero construye un grafo.")
            return

        self.steps = self._compute_warshall_steps()
        if not self.steps:
            messagebox.showinfo("Información", "No se pudieron generar pasos.")
            return

        self.current_step = 0
        self.show_current_step()

    def reset_steps(self):
        self.steps.clear()
        self.current_step = -1
        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Estados reiniciados.\n")

    def next_step(self):
        if not self.steps:
            messagebox.showinfo(
                "Información",
                "Primero inicia Warshall (botón 'Iniciar Warshall')."
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

    def _compute_warshall_steps(self):
        """
        Genera las matrices Wk del algoritmo de Warshall.
        Cada paso:
        - k_index, k_node
        - matrix: matriz de 0/1
        - updates: cambios en ese paso
        """
        n = len(self.nodes)
        index = {node: i for i, node in enumerate(self.nodes)}

        # Matriz inicial W0
        W = [[0] * n for _ in range(n)]
        for i in range(n):
            W[i][i] = 1  # cada nodo se alcanza a sí mismo

        for u, v in self.G.edges:
            i, j = index[u], index[v]
            W[i][j] = 1

        steps = []

        steps.append({
            "action": "init",
            "k_index": None,
            "k_node": None,
            "matrix": [row[:] for row in W],
            "updates": []
        })

        for k in range(n):
            k_node = self.nodes[k]
            updates = []

            for i in range(n):
                for j in range(n):
                    old = W[i][j]
                    new = old or (W[i][k] and W[k][j])

                    if new != old:
                        W[i][j] = new
                        updates.append({
                            "i": self.nodes[i],
                            "j": self.nodes[j],
                            "old": old,
                            "new": new,
                            "via": k_node,
                            "changed": True
                        })
                    else:
                        updates.append({
                            "i": self.nodes[i],
                            "j": self.nodes[j],
                            "old": old,
                            "new": new,
                            "via": k_node,
                            "changed": False
                        })

            steps.append({
                "action": "k_step",
                "k_index": k,
                "k_node": k_node,
                "matrix": [row[:] for row in W],
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

        node_colors = []
        for n in self.nodes:
            if n == current_k_node:
                node_colors.append("#ff9800")  # nodo k
            else:
                node_colors.append("#90caf9")

        nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax)

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edge_color="#9e9e9e",
            arrows=True,
            arrowstyle="->",
            arrowsize=15,
            ax=self.ax
        )

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    # -----------------------------------------------------------
    # Mostrar matriz Wk, fila/columna k y relación R_k
    # -----------------------------------------------------------
    def update_state_text(self, step):
        self.text_state.delete("1.0", tk.END)

        action = step["action"]
        W = step["matrix"]
        n = len(self.nodes)
        width = 4

        # pares (i,j) que cambiaron en este paso
        changed_pairs = set()
        new_pairs_only = []  # solo los que pasan de 0 -> 1 en ESTE paso
        for upd in step["updates"]:
            if upd["changed"]:
                changed_pairs.add((upd["i"], upd["j"]))
                if upd["old"] == 0 and upd["new"] == 1:
                    new_pairs_only.append(upd)

        k_index = step.get("k_index")
        k_node = step.get("k_node")

        # ---- Título del paso: W0, W1, W2...
        if action == "init":
            self.text_state.insert(tk.END, "W0: matriz inicial de alcanzabilidad\n\n")
        else:
            self.text_state.insert(
                tk.END,
                f"W{k_index + 1}: usando k = {k_node} como intermedio\n"
            )
            self.text_state.insert(
                tk.END,
                f"   → Se usa la FILA {k_node} (origen) y la COLUMNA {k_node} (destino)\n\n"
            )

        # ---- Relación ORIGINAL R (entrada) ----
        orig_list = sorted(list(self.original_pairs))
        if orig_list:
            orig_str = ", ".join(f"({a},{b})" for a, b in orig_list)
            self.text_state.insert(tk.END, "Relación ORIGINAL R (entrada):\n")
            self.text_state.insert(tk.END, f"  R = {{{orig_str}}}\n\n")
        else:
            self.text_state.insert(tk.END, "Relación ORIGINAL R (entrada): R = {}\n\n")

        # ---- Relación actual R_k (a partir de Wk) ----
        all_pairs = []
        new_vs_original = []
        for i in range(n):
            for j in range(n):
                if W[i][j] == 1:
                    pair = (self.nodes[i], self.nodes[j])
                    all_pairs.append(pair)
                    if pair not in self.original_pairs:
                        new_vs_original.append(pair)

        if all_pairs:
            all_str = ", ".join(f"({a},{b})" for a, b in all_pairs)
            self.text_state.insert(tk.END, "Relación R_k (cierre parcial actual):\n")
            self.text_state.insert(tk.END, f"  R_k = {{{all_str}}}\n\n")
        else:
            self.text_state.insert(tk.END, "Relación R_k (cierre parcial actual): R_k = {}\n\n")

        # ---- Pares NUEVOS (R_k \ R) acumulados ----
        if new_vs_original:
            new_total_str = ", ".join(f"({a},{b})" for a, b in sorted(set(new_vs_original)))
            self.text_state.insert(tk.END, "Pares NUEVOS acumulados (R_k \\ R):\n")
            self.text_state.insert(tk.END, f"  R_k \\ R = {{{new_total_str}}}\n\n")
        else:
            self.text_state.insert(tk.END, "Pares NUEVOS acumulados (R_k \\ R): {}\n\n")

        # ---- Matriz Wk ----
        self.text_state.insert(tk.END, "MATRIZ Wk (1 = hay camino, 0 = no hay)\n\n")

        # Encabezado columnas
        header = " " * width
        for node in self.nodes:
            header += f"{node:>{width}}"
        self.text_state.insert(tk.END, header + "\n")

        # Línea marcando columna k
        marker_line = " " * width
        for j in range(n):
            if k_index is not None and j == k_index:
                marker_line += f"{'^':>{width}}"
            else:
                marker_line += " " * width
        self.text_state.insert(tk.END, marker_line + "\n")

        # Filas
        for i in range(n):
            row_label = self.nodes[i]
            if k_index is not None and i == k_index:
                row_label = ">" + row_label  # marcar fila k
            row_str = f"{row_label:>{width}}"
            for j in range(n):
                cell = str(W[i][j])
                if (self.nodes[i], self.nodes[j]) in changed_pairs:
                    cell = cell + "*"  # celda que cambió en este paso
                row_str += f"{cell:>{width}}"
            self.text_state.insert(tk.END, row_str + "\n")

        # ---- Pares nuevos SOLO de este paso (tipo unión) ----
        if action == "k_step":
            self.text_state.insert(tk.END, "\nPares NUEVOS añadidos EN ESTE PASO:\n")
            if not new_pairs_only:
                self.text_state.insert(
                    tk.END,
                    "  Ningún par nuevo se añadió con este k.\n"
                )
            else:
                nuevos = [f"({u['i']},{u['j']})" for u in new_pairs_only]
                self.text_state.insert(
                    tk.END,
                    "  R_k = R_{k-1} ∪ {" + ", ".join(nuevos) + "}\n"
                )
                for u in new_pairs_only:
                    self.text_state.insert(
                        tk.END,
                        f"    {u['i']} alcanza a {u['j']} gracias a {u['via']} "
                        f"(W: {u['old']} → {u['new']}).\n"
                    )


if __name__ == "__main__":
    root = tk.Tk()
    app = WarshallApp(root)
    root.mainloop()
