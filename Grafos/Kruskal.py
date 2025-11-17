# -*- coding: utf-8 -*-
"""
Algoritmo de Kruskal interactivo (MST) con visualización mejor balanceada.

- Entrada: grafo NO dirigido (A B w = arista A--B con peso w)
- Kruskal paso a paso con Union-Find

Visual:
- Izquierda: controles + explicación (tamaño más compacto).
- Derecha: grafo grande.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import networkx as nx


class KruskalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Kruskal interactivo (MST)")

        # Grafo y estado
        self.G = nx.Graph()
        self.pos = {}
        self.nodes = []
        self.sorted_edges = []   # lista de (u, v, w)
        self.steps = []          # lista de pasos
        self.current_step = -1

        self._create_widgets()
        self._create_matplotlib_canvas()

    # -----------------------------------------------------------
    # UI
    # -----------------------------------------------------------
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=5)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Izquierda: controles (NO se expande tanto a lo ancho)
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Derecha: grafo (se lleva casi todo el espacio)
        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.graph_frame = graph_frame

        # ----- Parte superior de controles (nodos, aristas, botones) -----
        top_controls = ttk.Frame(controls_frame)
        top_controls.pack(fill=tk.X, expand=False)

        ttk.Label(top_controls, text="Nodos (separados por comas):").pack(anchor="w")
        self.entry_nodes = ttk.Entry(top_controls, width=30)
        self.entry_nodes.insert(0, "A,B,C,D,E")
        self.entry_nodes.pack(anchor="w", pady=(0, 5))

        ttk.Label(
            top_controls,
            text="Aristas (una por línea: origen destino peso):"
        ).pack(anchor="w")
        self.text_edges = ScrolledText(top_controls, width=32, height=5)
        example_edges = """A B 4
A C 2
B C 1
B D 5
C D 8
C E 10
D E 2"""
        self.text_edges.insert("1.0", example_edges)
        self.text_edges.pack(anchor="w", pady=(0, 5))

        buttons_row1 = ttk.Frame(top_controls)
        buttons_row1.pack(fill=tk.X, pady=(0, 4))

        ttk.Button(
            buttons_row1,
            text="Construir grafo",
            command=self.build_graph
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(
            buttons_row1,
            text="Reiniciar",
            command=self.reset_steps
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

        buttons_row2 = ttk.Frame(top_controls)
        buttons_row2.pack(fill=tk.X, pady=(0, 4))

        ttk.Button(
            buttons_row2,
            text="Iniciar Kruskal",
            command=self.start_kruskal
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(
            buttons_row2,
            text="Paso siguiente",
            command=self.next_step
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

        # ----- Parte inferior: explicación (altura moderada) -----
        text_frame = ttk.Frame(controls_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        ttk.Label(text_frame, text="Explicación paso a paso:").pack(anchor="w")
        # Altura menor para que no se coma toda la ventana
        self.text_state = ScrolledText(text_frame, width=60, height=14)
        self.text_state.configure(font=("Courier New", 10))
        self.text_state.pack(fill=tk.BOTH, expand=True)

    def _create_matplotlib_canvas(self):
        # Grafo más grande y proporcional
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
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
        self.sorted_edges = []

        # Nodos
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

        # Aristas
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

        # Layout del grafo
        if len(self.G.nodes) > 1:
            self.pos = nx.spring_layout(self.G, seed=42)
        else:
            self.pos = {self.nodes[0]: (0, 0)}

        # Lista de aristas ordenadas por peso
        self.sorted_edges = []
        for u, v, data in self.G.edges(data=True):
            w = data.get("weight", 1.0)
            self.sorted_edges.append((u, v, w))
        self.sorted_edges.sort(key=lambda e: (e[2], e[0], e[1]))

        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Grafo construido. Pulsa 'Iniciar Kruskal'.\n")

    # -----------------------------------------------------------
    # Kruskal paso a paso
    # -----------------------------------------------------------
    def start_kruskal(self):
        if self.G.number_of_nodes() == 0:
            messagebox.showerror("Error", "Primero construye un grafo.")
            return

        if not self.sorted_edges:
            messagebox.showerror("Error", "El grafo no tiene aristas.")
            return

        self.steps = self._compute_kruskal_steps()
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
                "Primero inicia Kruskal (botón 'Iniciar Kruskal')."
            )
            return

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            messagebox.showinfo(
                "Información",
                "Ya estás en el último paso (MST final)."
            )

    # ---------- Union-Find helpers ----------
    def _make_sets(self):
        parent = {v: v for v in self.nodes}
        rank = {v: 0 for v in self.nodes}
        return parent, rank

    def _find(self, parent, x):
        if parent[x] != x:
            parent[x] = self._find(parent, parent[x])
        return parent[x]

    def _union(self, parent, rank, x, y):
        rx = self._find(parent, x)
        ry = self._find(parent, y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True

    def _components_from_parent(self, parent):
        comp = {}
        for v in self.nodes:
            root = self._find(parent, v)
            comp.setdefault(root, []).append(v)
        for k in comp:
            comp[k].sort()
        return comp

    def _compute_kruskal_steps(self):
        parent, rank = self._make_sets()
        steps = []

        # Paso inicial
        steps.append({
            "index": -1,
            "current_edge": None,
            "will_add": False,
            "mst_edges": [],
            "components": self._components_from_parent(parent),
            "is_final": False,
        })

        mst_edges = []

        for idx, (u, v, w) in enumerate(self.sorted_edges):
            ru = self._find(parent, u)
            rv = self._find(parent, v)
            will_add = (ru != rv)

            if will_add:
                self._union(parent, rank, u, v)
                mst_edges = mst_edges + [(u, v, w)]

            steps.append({
                "index": idx,
                "current_edge": (u, v, w),
                "will_add": will_add,
                "mst_edges": mst_edges[:],
                "components": self._components_from_parent(parent),
                "is_final": False,
            })

        # Paso final extra solo MST
        steps.append({
            "index": len(self.sorted_edges),
            "current_edge": None,
            "will_add": False,
            "mst_edges": mst_edges[:],
            "components": self._components_from_parent(parent),
            "is_final": True,
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

        mst_edges = []
        current_edge = None
        will_add = False
        is_final = False

        if step is not None:
            mst_edges = step["mst_edges"]
            current_edge = step["current_edge"]
            will_add = step["will_add"]
            is_final = step.get("is_final", False)

        # Union-Find con aristas del MST
        parent = {v: v for v in self.nodes}
        rank = {v: 0 for v in self.nodes}
        for (u, v, w) in mst_edges:
            self._union(parent, rank, u, v)

        cycle_edges, normal_edges = [], []
        for u, v in self.G.edges():
            ru = self._find(parent, u)
            rv = self._find(parent, v)
            if ru == rv and (u, v, self.G[u][v]["weight"]) not in mst_edges:
                cycle_edges.append((u, v))
            else:
                normal_edges.append((u, v))

        # Nodos
        nx.draw_networkx_nodes(self.G, self.pos, node_color="#90caf9", ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax)

        # Aristas cíclicas (apagadas)
        if cycle_edges:
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=cycle_edges,
                width=1,
                edge_color="#cfd8dc",
                alpha=0.25,
                style="dashed",
                ax=self.ax
            )

        # Aristas normales en gris
        if normal_edges:
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=normal_edges,
                width=1.5,
                edge_color="#b0bec5",
                ax=self.ax
            )

        # MST en verde
        if mst_edges:
            mst_pairs = [(u, v) for (u, v, w) in mst_edges]
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=mst_pairs,
                width=3,
                edge_color="#4caf50",
                ax=self.ax
            )

        # Arista actual (si no es el paso final)
        if current_edge is not None and not is_final:
            u, v, w = current_edge
            color = "#4caf50" if will_add else "#f44336"
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=[(u, v)],
                width=4,
                edge_color=color,
                ax=self.ax
            )

        # Etiquetas de pesos base
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        # Peso resaltado de la arista actual
        if current_edge is not None and not is_final:
            u, v, w = current_edge
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            color = "#4caf50" if will_add else "#f44336"
            self.ax.text(
                mx, my, f"{w}",
                fontsize=11,
                fontweight="bold",
                color=color,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, alpha=0.9),
            )

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    # -----------------------------------------------------------
    # Texto
    # -----------------------------------------------------------
    def update_state_text(self, step):
        self.text_state.delete("1.0", tk.END)
        is_final = step.get("is_final", False)

        self.text_state.insert(tk.END, "Aristas ordenadas por peso (ascendente):\n")
        for idx, (u, v, w) in enumerate(self.sorted_edges):
            if not is_final and idx == step["index"]:
                prefix = "->"
            else:
                prefix = "  "
            self.text_state.insert(
                tk.END,
                f"{prefix} e{idx+1}: ({u},{v})  w = {w}\n"
            )

        self.text_state.insert(tk.END, "\n")

        if step["index"] == -1:
            self.text_state.insert(
                tk.END,
                "Paso 0: estado inicial, sin aristas en el Árbol de Expansión Mínima (MST).\n"
            )
        elif is_final:
            self.text_state.insert(
                tk.END,
                "Paso final: Árbol de Expansión Mínima COMPLETO.\n"
            )
        else:
            u, v, w = step["current_edge"]
            self.text_state.insert(
                tk.END,
                f"Paso {step['index'] + 1}: considerar arista ({u},{v}) con peso {w}\n"
            )
            if step["will_add"]:
                self.text_state.insert(
                    tk.END,
                    "  - Los nodos están en componentes diferentes → NO forma ciclo.\n"
                )
                self.text_state.insert(
                    tk.END,
                    "  → Se AGREGA esta arista al MST.\n"
                )
            else:
                self.text_state.insert(
                    tk.END,
                    "  - Los nodos ya están conectados (misma componente) → formaría un ciclo.\n"
                )
                self.text_state.insert(
                    tk.END,
                    "  → Se DESCARTA esta arista.\n"
                )

        self.text_state.insert(tk.END, "\nComponentes actuales (Union-Find):\n")
        for idx, (root, nodes) in enumerate(sorted(step["components"].items()), start=1):
            self.text_state.insert(tk.END, f"  C{idx}: {{{', '.join(nodes)}}}\n")

        self.text_state.insert(tk.END, "\nAristas del MST hasta ahora:\n")
        mst_edges = step["mst_edges"]
        if not mst_edges:
            self.text_state.insert(tk.END, "  (ninguna arista todavía)\n")
        else:
            total = sum(w for (_, _, w) in mst_edges)
            for (u, v, w) in mst_edges:
                self.text_state.insert(
                    tk.END,
                    f"  ({u},{v})  w = {w}\n"
                )
            self.text_state.insert(
                tk.END,
                f"\nPeso total del MST parcial = {total}\n"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = KruskalApp(root)
    root.mainloop()
