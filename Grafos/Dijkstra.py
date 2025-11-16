# -*- coding: utf-8 -*-
"""
Dijkstra interactivo paso a paso en estilo "tabla de video":

- Paso 0: inicialización (todas las distancias = ∞ excepto el origen).
- Paso k: elegir nodo con menor distancia no visitado (usando cola de prioridad),
          marcarlo como visitado,
          relajar a sus vecinos y mostrar qué distancias CAMBIAN
          o NO CAMBIAN.

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
import heapq   # cola de prioridad


class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra interactivo (cola de prioridad)")

        # Grafo y estados
        self.G = nx.Graph()
        self.pos = {}
        self.steps = []        # lista de iteraciones
        self.current_step = -1
        self.source = None

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
        self.text_edges = ScrolledText(controls_frame, width=30, height=10)
        example_edges = """A B 4
A C 2
B C 1
B D 5
C D 8
C E 10
D E 2"""
        self.text_edges.insert(tk.END, example_edges)
        self.text_edges.pack(anchor="w", pady=(0, 5))

        ttk.Button(
            controls_frame,
            text="Construir grafo",
            command=self.build_graph
        ).pack(fill=tk.X, pady=(0, 10))

        # Nodo origen
        ttk.Label(controls_frame, text="Nodo origen para Dijkstra:").pack(anchor="w")
        self.entry_source = ttk.Entry(controls_frame, width=10)
        self.entry_source.insert(0, "A")
        self.entry_source.pack(anchor="w", pady=(0, 5))

        # Botones Dijkstra
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X, pady=(5, 5))

        ttk.Button(
            buttons_frame,
            text="Iniciar Dijkstra",
            command=self.start_dijkstra
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        ttk.Button(
            buttons_frame,
            text="Reiniciar",
            command=self.reset_steps
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Siguiente paso
        ttk.Button(
            controls_frame,
            text="Paso siguiente",
            command=self.next_step
        ).pack(fill=tk.X, pady=(5, 10))

        # Estado textual
        ttk.Label(controls_frame, text="Tabla de distancias / pasos:").pack(anchor="w")
        self.text_state = ScrolledText(controls_frame, width=30, height=18)
        self.text_state.pack(anchor="w", pady=(0, 5))

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
        self.source = None

        # Nodos
        nodes_text = self.entry_nodes.get().strip()
        if not nodes_text:
            messagebox.showerror("Error", "Debes ingresar al menos un nodo.")
            return
        nodes = [n.strip() for n in nodes_text.split(",") if n.strip()]
        if not nodes:
            messagebox.showerror("Error", "La lista de nodos no es válida.")
            return
        self.G.add_nodes_from(nodes)

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
            if u not in self.G.nodes or v not in self.G.nodes:
                messagebox.showerror(
                    "Error",
                    f"Los nodos '{u}' o '{v}' de la línea '{line}' no están en la lista de nodos."
                )
                return
            try:
                weight = float(w)
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"El peso '{w}' en la línea '{line}' no es un número."
                )
                return
            self.G.add_edge(u, v, weight=weight)

        # Posiciones para dibujar
        if len(self.G.nodes) > 1:
            self.pos = nx.spring_layout(self.G, seed=42)
        else:
            self.pos = {nodes[0]: (0, 0)}

        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Grafo construido correctamente.\n")

    # -----------------------------------------------------------
    # Dijkstra con cola de prioridad
    # -----------------------------------------------------------
    def start_dijkstra(self):
        if self.G.number_of_nodes() == 0:
            messagebox.showerror("Error", "Primero construye un grafo.")
            return

        source = self.entry_source.get().strip()
        if source not in self.G.nodes:
            messagebox.showerror(
                "Error",
                f"El nodo origen '{source}' no existe en el grafo."
            )
            return

        self.source = source
        self.steps = self._compute_dijkstra_iterations(self.G, source)
        if not self.steps:
            messagebox.showinfo(
                "Información",
                "No se pudieron generar pasos para Dijkstra."
            )
            return

        self.current_step = 0
        self.show_current_step()

    def reset_steps(self):
        self.current_step = -1
        self.steps = []
        self.source = None
        self.draw_graph()
        self.text_state.delete("1.0", tk.END)
        self.text_state.insert(tk.END, "Estados reiniciados.\n")

    def next_step(self):
        if not self.steps:
            messagebox.showinfo(
                "Información",
                "Primero inicia Dijkstra (botón 'Iniciar Dijkstra')."
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

    def _compute_dijkstra_iterations(self, G, source):
        """
        Dijkstra usando cola de prioridad (heapq).

        - step 0: acción 'init'
        - step k: acción 'iter', contiene:
             * iter_num
             * current: nodo elegido en esa iteración
             * visited: nodos ya permanentes
             * dist, prev
             * updates: lista de (v, dist_v_antes, dist_v_despues, changed)
             * highlight_edges: aristas (u, v) que se relajaron y CAMBIARON
        """
        dist = {n: math.inf for n in G.nodes}
        prev = {n: None for n in G.nodes}
        dist[source] = 0.0

        visited = set()
        steps = []

        # Paso 0: inicialización
        steps.append({
            "action": "init",
            "iter_num": 0,
            "current": None,
            "visited": visited.copy(),
            "dist": dist.copy(),
            "prev": prev.copy(),
            "updates": [],
            "highlight_edges": []
        })

        # Cola de prioridad: (distancia, nodo)
        pq = []
        heapq.heappush(pq, (0.0, source))

        iter_num = 1

        while pq:
            current_dist, u = heapq.heappop(pq)

            # Si ya está visitado o desactualizado, lo ignoramos
            if u in visited:
                continue
            if current_dist > dist[u]:
                continue

            updates = []
            highlight_edges = []

            # Relajar vecinos no visitados
            for v, data in G[u].items():
                if v in visited:
                    continue

                w = data.get("weight", 1.0)
                old = dist[v]
                new = dist[u] + w

                if new < old:
                    dist[v] = new
                    prev[v] = u
                    updates.append((v, old, new, True))   # CAMBIA
                    highlight_edges.append((u, v))
                    heapq.heappush(pq, (new, v))
                else:
                    updates.append((v, old, new, False))  # NO CAMBIA

            visited.add(u)

            steps.append({
                "action": "iter",
                "iter_num": iter_num,
                "current": u,
                "visited": visited.copy(),
                "dist": dist.copy(),
                "prev": prev.copy(),
                "updates": updates,
                "highlight_edges": highlight_edges
            })

            iter_num += 1

            if len(visited) == len(G.nodes):
                break

        return steps

    # -----------------------------------------------------------
    # Visualización
    # -----------------------------------------------------------
    def show_current_step(self):
        if self.current_step < 0 or self.current_step >= len(self.steps):
            return
        step = self.steps[self.current_step]
        self.draw_graph(step)
        self.update_state_text(step)

    def draw_graph(self, step=None):
        self.ax.clear()

        if not self.pos:
            self.canvas.draw()
            return

        visited = set()
        current = None
        prev = None
        highlight_edges = []

        if step is not None:
            visited = step["visited"]
            current = step["current"]
            prev = step["prev"]
            highlight_edges = step["highlight_edges"]

        # Colores de nodos
        node_colors = []
        for n in self.G.nodes:
            if n == current:
                node_colors.append("#ff9800")  # naranja
            elif n in visited:
                node_colors.append("#8bc34a")  # verde
            else:
                node_colors.append("#90caf9")  # azul

        nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax)

        # Todas las aristas en gris
        nx.draw_networkx_edges(self.G, self.pos, edge_color="#9e9e9e", ax=self.ax)

        # Pesos
        edge_labels = {(u, v): f'{d["weight"]}' for u, v, d in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        # Árbol de caminos mínimos SOLO con nodos visitados
        if step is not None and prev is not None:
            tree_edges = []
            for v, u in prev.items():
                if u is not None and v in visited:
                    tree_edges.append((u, v))
            if tree_edges:
                nx.draw_networkx_edges(
                    self.G, self.pos,
                    edgelist=tree_edges,
                    width=3,
                    edge_color="#4caf50",
                    ax=self.ax
                )

        # Aristas relajadas que cambiaron en esta iteración
        if highlight_edges:
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=highlight_edges,
                width=4,
                edge_color="#f44336",
                ax=self.ax
            )

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    def update_state_text(self, step):
        self.text_state.delete("1.0", tk.END)

        action = step["action"]
        iter_num = step["iter_num"]
        current = step["current"]
        dist = step["dist"]
        prev = step["prev"]
        visited = step["visited"]
        updates = step["updates"]

        if action == "init":
            self.text_state.insert(tk.END, "Paso 0: INICIALIZACIÓN\n")
            self.text_state.insert(tk.END, "Todas las distancias = ∞ excepto el origen.\n")
        else:
            self.text_state.insert(tk.END, f"Paso {iter_num}: Iteración {iter_num}\n")

        self.text_state.insert(tk.END, "-" * 30 + "\n")
        self.text_state.insert(tk.END, f"Nodo actual (elegido con menor distancia): {current}\n")
        self.text_state.insert(tk.END, f"Nodos visitados (permanentes): {sorted(list(visited))}\n")
        self.text_state.insert(tk.END, "-" * 30 + "\n")

        # Actualizaciones en esta iteración
        if action == "iter":
            if updates:
                self.text_state.insert(tk.END, "Actualizaciones en esta iteración:\n")
                for v, old, new, changed in updates:
                    old_str = "∞" if old == math.inf else f"{old:.2f}"
                    new_str = "∞" if new == math.inf else f"{new:.2f}"

                    if changed:
                        self.text_state.insert(
                            tk.END,
                            f"✔ dist[{v}] CAMBIA de {old_str} → {new_str}\n"
                        )
                    else:
                        self.text_state.insert(
                            tk.END,
                            f"✘ dist[{v}] NO CAMBIA ({old_str} ≤ {new_str})\n"
                        )
            else:
                self.text_state.insert(tk.END, "En esta iteración no hubo actualizaciones de distancias.\n")

        self.text_state.insert(tk.END, "\nTABLA DE DISTANCIAS (tipo video):\n")
        self.text_state.insert(tk.END, "Nodo | dist | prev\n")
        self.text_state.insert(tk.END, "-------------------\n")
        for n in sorted(dist.keys()):
            d = dist[n]
            d_str = "∞" if d == math.inf else f"{d:.2f}"
            self.text_state.insert(
                tk.END,
                f" {n:>4} | {d_str:>5} | {str(prev[n]):>4}\n"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()
