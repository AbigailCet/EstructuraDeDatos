import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Grafo:
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.aristas_info = {}
        self.vertices_info = {}
        self.contador_aristas = 0
        
    # ==================== OPERACIONES GENERALES ====================
    
    def numVertices(self):
        return self.G.number_of_nodes()
    
    def numAristas(self):
        return len(self.aristas_info)
    
    def vertices(self):
        return list(self.G.nodes())
    
    def aristas(self):
        return list(self.aristas_info.keys())
    
    def grado(self, v):
        if v not in self.G:
            return None
        return self.G.degree(v)
    
    def verticesAdyacentes(self, v):
        if v not in self.G:
            return []
        adyacentes = set()
        adyacentes.update(self.G.predecessors(v))
        adyacentes.update(self.G.successors(v))
        return list(adyacentes)
    
    def aristasIncidentes(self, v):
        if v not in self.G:
            return []
        incidentes = []
        for arista_id, info in self.aristas_info.items():
            origen, destino = info['vertices']
            if origen == v or destino == v:
                incidentes.append(arista_id)
        return incidentes
    
    def verticesFinales(self, e):
        if e not in self.aristas_info:
            return None
        return self.aristas_info[e]['vertices']
    
    def opuesto(self, v, e):
        if e not in self.aristas_info:
            return None
        origen, destino = self.aristas_info[e]['vertices']
        if origen == v:
            return destino
        elif destino == v:
            return origen
        return None
    
    def esAdyacente(self, v, w):
        if v not in self.G or w not in self.G:
            return False
        return self.G.has_edge(v, w) or self.G.has_edge(w, v)
    
    # ==================== OPERACIONES CON ARISTAS DIRIGIDAS ====================
    
    def aristasDirigidas(self):
        return [aid for aid, info in self.aristas_info.items() if info['dirigida']]
    
    def aristasNodirigidas(self):
        return [aid for aid, info in self.aristas_info.items() if not info['dirigida']]
    
    def gradoEnt(self, v):
        if v not in self.G:
            return None
        return self.G.in_degree(v)
    
    def gradoSalida(self, v):
        if v not in self.G:
            return None
        return self.G.out_degree(v)
    
    def aristasIncidentesEnt(self, v):
        if v not in self.G:
            return []
        return [aid for aid, info in self.aristas_info.items() 
                if info['dirigida'] and info['vertices'][1] == v]
    
    def aristasIncidentesSal(self, v):
        if v not in self.G:
            return []
        return [aid for aid, info in self.aristas_info.items() 
                if info['dirigida'] and info['vertices'][0] == v]
    
    def verticesAdyacentesEnt(self, v):
        if v not in self.G:
            return []
        return list(self.G.predecessors(v))
    
    def verticesAdyacentesSal(self, v):
        if v not in self.G:
            return []
        return list(self.G.successors(v))
    
    def destino(self, e):
        if e not in self.aristas_info or not self.aristas_info[e]['dirigida']:
            return None
        return self.aristas_info[e]['vertices'][1]
    
    def origen(self, e):
        if e not in self.aristas_info or not self.aristas_info[e]['dirigida']:
            return None
        return self.aristas_info[e]['vertices'][0]
    
    def esDirigida(self, e):
        if e not in self.aristas_info:
            return None
        return self.aristas_info[e]['dirigida']
    
    # ==================== OPERACIONES PARA ACTUALIZAR GRAFOS ====================
    
    def insertaVertice(self, o):
        nuevo_id = f"V{self.numVertices()}"
        self.G.add_node(nuevo_id)
        self.vertices_info[nuevo_id] = {'objeto': str(o)}
        return nuevo_id
    
    def insertaArista(self, v, w, o):
        if v not in self.G or w not in self.G:
            return None
        arista_id = f"E{self.contador_aristas}"
        self.contador_aristas += 1
        self.G.add_edge(v, w, key=arista_id)
        self.G.add_edge(w, v, key=arista_id)
        self.aristas_info[arista_id] = {
            'dirigida': False,
            'objeto': str(o),
            'vertices': (v, w)
        }
        return arista_id
    
    def insertaAristaDirigida(self, v, w, o):
        if v not in self.G or w not in self.G:
            return None
        arista_id = f"E{self.contador_aristas}"
        self.contador_aristas += 1
        self.G.add_edge(v, w, key=arista_id)
        self.aristas_info[arista_id] = {
            'dirigida': True,
            'objeto': str(o),
            'vertices': (v, w)
        }
        return arista_id
    
    def eliminaVertice(self, v):
        if v not in self.G:
            return False
        aristas_a_eliminar = self.aristasIncidentes(v)
        for arista_id in aristas_a_eliminar:
            self.eliminaArista(arista_id)
        self.G.remove_node(v)
        del self.vertices_info[v]
        return True
    
    def eliminaArista(self, e):
        if e not in self.aristas_info:
            return False
        info = self.aristas_info[e]
        v, w = info['vertices']
        self.G.remove_edge(v, w, key=e)
        if not info['dirigida']:
            self.G.remove_edge(w, v, key=e)
        del self.aristas_info[e]
        return True
    
    def convierteNoDirigida(self, e):
        if e not in self.aristas_info:
            return False
        info = self.aristas_info[e]
        if not info['dirigida']:
            return True
        v, w = info['vertices']
        self.G.add_edge(w, v, key=e)
        self.aristas_info[e]['dirigida'] = False
        return True
    
    def invierteDireccion(self, e):
        if e not in self.aristas_info or not self.aristas_info[e]['dirigida']:
            return False
        info = self.aristas_info[e]
        v, w = info['vertices']
        self.G.remove_edge(v, w, key=e)
        self.G.add_edge(w, v, key=e)
        self.aristas_info[e]['vertices'] = (w, v)
        return True
    
    def asignaDireccionDesde(self, e, v):
        if e not in self.aristas_info:
            return False
        info = self.aristas_info[e]
        origen, destino = info['vertices']
        if origen != v and destino != v:
            return False
        otro = destino if origen == v else origen
        if info['dirigida']:
            self.G.remove_edge(origen, destino, key=e)
        else:
            self.G.remove_edge(origen, destino, key=e)
            self.G.remove_edge(destino, origen, key=e)
        self.G.add_edge(v, otro, key=e)
        self.aristas_info[e]['dirigida'] = True
        self.aristas_info[e]['vertices'] = (v, otro)
        return True
    
    def asignaDireccionA(self, e, v):
        if e not in self.aristas_info:
            return False
        info = self.aristas_info[e]
        origen, destino = info['vertices']
        if origen != v and destino != v:
            return False
        otro = destino if origen == v else origen
        if info['dirigida']:
            self.G.remove_edge(origen, destino, key=e)
        else:
            self.G.remove_edge(origen, destino, key=e)
            self.G.remove_edge(destino, origen, key=e)
        self.G.add_edge(otro, v, key=e)
        self.aristas_info[e]['dirigida'] = True
        self.aristas_info[e]['vertices'] = (otro, v)
        return True


class GrafoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Visualizador Interactivo de Grafos")
        self.root.geometry("1500x900")
        self.root.configure(bg='#f0f0f0')
        
        self.grafo = Grafo()
        self.pos = {}  # Posiciones de nodos
        self.selected_node = None
        self.first_node_for_edge = None
        self.modo = "seleccionar"  # modos: seleccionar, agregar_vertice, agregar_arista
        
        self.crear_interfaz()
        self.dibujar_grafo()
        
    def crear_interfaz(self):
        # Barra superior de herramientas
        toolbar = tk.Frame(self.root, bg='#2c3e50', height=80)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Título
        title_label = tk.Label(toolbar, text="🎯 Visualizador de Grafos", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Botones de modo
        btn_frame = tk.Frame(toolbar, bg='#2c3e50')
        btn_frame.pack(side=tk.LEFT, padx=20)
        
        self.btn_seleccionar = tk.Button(btn_frame, text="👆 Seleccionar", 
                                         command=lambda: self.cambiar_modo("seleccionar"),
                                         font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                                         padx=15, pady=8, relief=tk.RAISED, cursor='hand2')
        self.btn_seleccionar.pack(side=tk.LEFT, padx=5)
        
        self.btn_vertice = tk.Button(btn_frame, text="➕ Agregar Vértice", 
                                     command=lambda: self.cambiar_modo("agregar_vertice"),
                                     font=('Arial', 10, 'bold'), bg='#2ecc71', fg='white',
                                     padx=15, pady=8, relief=tk.RAISED, cursor='hand2')
        self.btn_vertice.pack(side=tk.LEFT, padx=5)
        
        self.btn_arista = tk.Button(btn_frame, text="🔗 Agregar Arista", 
                                    command=lambda: self.cambiar_modo("agregar_arista"),
                                    font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                                    padx=15, pady=8, relief=tk.RAISED, cursor='hand2')
        self.btn_arista.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Limpiar", 
                 command=self.limpiar_grafo,
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white',
                 padx=15, pady=8, relief=tk.RAISED, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Indicador de modo
        self.modo_label = tk.Label(toolbar, text="Modo: Seleccionar", 
                                  font=('Arial', 12), bg='#2c3e50', fg='#ecf0f1')
        self.modo_label.pack(side=tk.RIGHT, padx=20)
        
        # Contenedor principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (Grafo)
        left_panel = tk.Frame(main_container, bg='white', relief=tk.RIDGE, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Título del grafo
        graph_title = tk.Label(left_panel, text="📊 Visualización del Grafo", 
                              font=('Arial', 12, 'bold'), bg='white')
        graph_title.pack(pady=10)
        
        # Instrucciones
        self.instrucciones = tk.Label(left_panel, 
                                     text="💡 Clic derecho en vértices para ver operaciones",
                                     font=('Arial', 9), bg='white', fg='#7f8c8d')
        self.instrucciones.pack()
        
        # Canvas del grafo
        self.fig = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, left_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Eventos del mouse
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)
        
        # Panel derecho (Operaciones y Consola)
        right_panel = tk.Frame(main_container, bg='#ecf0f1', width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Notebook de operaciones
        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Pestaña de Información
        info_tab = tk.Frame(notebook, bg='white')
        notebook.add(info_tab, text="📋 Información")
        self.crear_tab_info(info_tab)
        
        # Pestaña de Operaciones
        ops_tab = tk.Frame(notebook, bg='white')
        notebook.add(ops_tab, text="⚙️ Operaciones")
        self.crear_tab_operaciones(ops_tab)
        
        # Consola de salida
        console_frame = tk.LabelFrame(right_panel, text="📝 Consola de Salida", 
                                     font=('Arial', 10, 'bold'), bg='#ecf0f1')
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(console_frame, height=10, 
                                                     font=('Courier', 9),
                                                     bg='#2c3e50', fg='#ecf0f1',
                                                     insertbackground='white')
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log("✨ Bienvenido al Visualizador de Grafos")
        self.log("💡 Usa los botones superiores para agregar vértices y aristas")
        
    def crear_tab_info(self, parent):
        # Frame con scroll
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Estadísticas generales
        stats_frame = tk.LabelFrame(scrollable_frame, text="📊 Estadísticas", 
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stat_vertices = tk.Label(stats_frame, text="Vértices: 0", 
                                     font=('Arial', 10), bg='white', anchor='w')
        self.stat_vertices.pack(fill=tk.X)
        
        self.stat_aristas = tk.Label(stats_frame, text="Aristas: 0", 
                                    font=('Arial', 10), bg='white', anchor='w')
        self.stat_aristas.pack(fill=tk.X)
        
        self.stat_dirigidas = tk.Label(stats_frame, text="Dirigidas: 0", 
                                      font=('Arial', 10), bg='white', anchor='w')
        self.stat_dirigidas.pack(fill=tk.X)
        
        self.stat_no_dirigidas = tk.Label(stats_frame, text="No Dirigidas: 0", 
                                         font=('Arial', 10), bg='white', anchor='w')
        self.stat_no_dirigidas.pack(fill=tk.X)
        
        # Información del nodo seleccionado
        self.node_info_frame = tk.LabelFrame(scrollable_frame, text="🔍 Nodo Seleccionado", 
                                            font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        self.node_info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.node_info_text = tk.Text(self.node_info_frame, height=12, 
                                     font=('Courier', 9), bg='#ecf0f1', wrap=tk.WORD)
        self.node_info_text.pack(fill=tk.BOTH, expand=True)
        self.node_info_text.insert('1.0', 'Selecciona un vértice para ver su información')
        self.node_info_text.config(state=tk.DISABLED)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_tab_operaciones(self, parent):
        canvas = tk.Canvas(parent, bg='white')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Consultas rápidas
        quick_frame = tk.LabelFrame(scrollable_frame, text="⚡ Consultas Rápidas", 
                                   font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        quick_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(quick_frame, text="📋 Listar todos los vértices", 
                 command=lambda: self.log(f"Vértices: {self.grafo.vertices()}"),
                 bg='#3498db', fg='white', cursor='hand2').pack(fill=tk.X, pady=2)
        
        tk.Button(quick_frame, text="📋 Listar todas las aristas", 
                 command=lambda: self.log(f"Aristas: {self.grafo.aristas()}"),
                 bg='#3498db', fg='white', cursor='hand2').pack(fill=tk.X, pady=2)
        
        tk.Button(quick_frame, text="➡️ Listar aristas dirigidas", 
                 command=lambda: self.log(f"Dirigidas: {self.grafo.aristasDirigidas()}"),
                 bg='#e74c3c', fg='white', cursor='hand2').pack(fill=tk.X, pady=2)
        
        tk.Button(quick_frame, text="↔️ Listar aristas no dirigidas", 
                 command=lambda: self.log(f"No dirigidas: {self.grafo.aristasNodirigidas()}"),
                 bg='#2ecc71', fg='white', cursor='hand2').pack(fill=tk.X, pady=2)
        
        # Operaciones sobre vértices
        vertex_frame = tk.LabelFrame(scrollable_frame, text="🔵 Operaciones sobre Vértices", 
                                    font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        vertex_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(vertex_frame, text="Vértice:", bg='white').pack(anchor='w')
        vertex_entry_frame = tk.Frame(vertex_frame, bg='white')
        vertex_entry_frame.pack(fill=tk.X, pady=5)
        
        self.vertex_op_entry = tk.Entry(vertex_entry_frame, font=('Arial', 10))
        self.vertex_op_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Button(vertex_entry_frame, text="ℹ️", 
                 command=self.mostrar_info_vertice,
                 bg='#9b59b6', fg='white', cursor='hand2').pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(vertex_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="Grado", 
                 command=lambda: self.ejecutar_op_vertice('grado'),
                 bg='#1abc9c', fg='white', font=('Arial', 8), cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(btn_frame, text="Adyacentes", 
                 command=lambda: self.ejecutar_op_vertice('verticesAdyacentes'),
                 bg='#1abc9c', fg='white', font=('Arial', 8), cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        btn_frame2 = tk.Frame(vertex_frame, bg='white')
        btn_frame2.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame2, text="Aristas Inc.", 
                 command=lambda: self.ejecutar_op_vertice('aristasIncidentes'),
                 bg='#1abc9c', fg='white', font=('Arial', 8), cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(btn_frame2, text="🗑️ Eliminar", 
                 command=self.eliminar_vertice_op,
                 bg='#e74c3c', fg='white', font=('Arial', 8), cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Operaciones sobre aristas
        edge_frame = tk.LabelFrame(scrollable_frame, text="🔗 Operaciones sobre Aristas", 
                                  font=('Arial', 10, 'bold'), bg='white', padx=10, pady=10)
        edge_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(edge_frame, text="Arista:", bg='white').pack(anchor='w')
        edge_entry_frame = tk.Frame(edge_frame, bg='white')
        edge_entry_frame.pack(fill=tk.X, pady=5)
        
        self.edge_op_entry = tk.Entry(edge_entry_frame, font=('Arial', 10))
        self.edge_op_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Button(edge_entry_frame, text="ℹ️", 
                 command=self.mostrar_info_arista,
                 bg='#9b59b6', fg='white', cursor='hand2').pack(side=tk.LEFT)
        
        btn_frame3 = tk.Frame(edge_frame, bg='white')
        btn_frame3.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame3, text="Invertir ⇄", 
                 command=self.invertir_arista_op,
                 bg='#f39c12', fg='white', font=('Arial', 8), cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(btn_frame3, text="↔️ No Dirigida", 
                 command=self.convertir_no_dirigida_op,
                 bg='#2ecc71', fg='white', font=('Arial', 8), cursor='hand2').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        btn_frame4 = tk.Frame(edge_frame, bg='white')
        btn_frame4.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame4, text="🗑️ Eliminar", 
                 command=self.eliminar_arista_op,
                 bg='#e74c3c', fg='white', font=('Arial', 8), cursor='hand2').pack(fill=tk.X, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def cambiar_modo(self, nuevo_modo):
        self.modo = nuevo_modo
        self.first_node_for_edge = None
        
        # Resetear colores de botones
        self.btn_seleccionar.config(relief=tk.RAISED, bg='#95a5a6')
        self.btn_vertice.config(relief=tk.RAISED, bg='#95a5a6')
        self.btn_arista.config(relief=tk.RAISED, bg='#95a5a6')
        
        # Destacar botón activo
        if nuevo_modo == "seleccionar":
            self.btn_seleccionar.config(relief=tk.SUNKEN, bg='#3498db')
            self.modo_label.config(text="Modo: 👆 Seleccionar")
            self.instrucciones.config(text="💡 Clic derecho en vértices para operaciones")
        elif nuevo_modo == "agregar_vertice":
            self.btn_vertice.config(relief=tk.SUNKEN, bg='#2ecc71')
            self.modo_label.config(text="Modo: ➕ Agregar Vértice")
            self.instrucciones.config(text="💡 Haz clic en el área del grafo para agregar vértices")
        elif nuevo_modo == "agregar_arista":
            self.btn_arista.config(relief=tk.SUNKEN, bg='#e74c3c')
            self.modo_label.config(text="Modo: 🔗 Agregar Arista")
            self.instrucciones.config(text="💡 Haz clic en dos vértices para conectarlos")
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        if event.button == 1:  # Clic izquierdo
            if self.modo == "agregar_vertice":
                self.agregar_vertice_click(event.xdata, event.ydata)
            elif self.modo == "agregar_arista":
                nodo = self.get_node_at_position(event.xdata, event.ydata)
                if nodo:
                    self.agregar_arista_click(nodo)
            elif self.modo == "seleccionar":
                nodo = self.get_node_at_position(event.xdata, event.ydata)
                if nodo:
                    self.seleccionar_nodo(nodo)
                    
        elif event.button == 3:  # Clic derecho
            nodo = self.get_node_at_position(event.xdata, event.ydata)
            if nodo:
                self.mostrar_menu_contextual(event, nodo)
    
    def on_hover(self, event):
        if event.inaxes != self.ax or not self.pos:
            return
        
        nodo = self.get_node_at_position(event.xdata, event.ydata)
        if nodo:
            self.canvas.get_tk_widget().config(cursor='hand2')
        else:
            self.canvas.get_tk_widget().config(cursor='arrow')
    
    def get_node_at_position(self, x, y, threshold=0.1):
        """Encuentra el nodo más cercano a la posición dada"""
        if not self.pos:
            return None
        
        for nodo, (nx, ny) in self.pos.items():
            dist = np.sqrt((nx - x)**2 + (ny - y)**2)
            if dist < threshold:
                return nodo
        return None
    
    def agregar_vertice_click(self, x, y):
        """Agrega un vértice en la posición del clic"""
        obj = simpledialog.askstring("Nuevo Vértice", 
                                     "Nombre/Objeto del vértice (opcional):",
                                     parent=self.root)
        if obj is None:  # Usuario canceló
            return
        if not obj:
            obj = "null"
        
        v_id = self.grafo.insertaVertice(obj)
        self.pos[v_id] = (x, y)
        self.log(f"✅ Vértice {v_id} agregado: '{obj}'")
        self.actualizar_interfaz()
    
    def agregar_arista_click(self, nodo):
        """Maneja la selección de nodos para crear arista"""
        if self.first_node_for_edge is None:
            self.first_node_for_edge = nodo
            self.log(f"🔵 Primer nodo seleccionado: {nodo}")
            self.log(f"👉 Selecciona el segundo nodo...")
            # Resaltar el primer nodo
            self.dibujar_grafo(highlight_node=nodo)
        else:
            segundo_nodo = nodo
            
            # Preguntar tipo de arista
            respuesta = messagebox.askyesnocancel(
                "Tipo de Arista",
                f"Conectar {self.first_node_for_edge} → {segundo_nodo}\n\n" +
                "¿Dirigida?\n\n" +
                "Sí = Dirigida (→)\n" +
                "No = No dirigida (↔)\n" +
                "Cancelar = Cancelar operación"
            )
            
            if respuesta is None:  # Cancelar
                self.first_node_for_edge = None
                self.log("❌ Operación cancelada")
                self.dibujar_grafo()
                return
            
            # Pedir objeto/nombre de la arista
            obj = simpledialog.askstring("Nueva Arista", 
                                        "Nombre/Objeto de la arista (opcional):",
                                        parent=self.root)
            if obj is None:
                self.first_node_for_edge = None
                self.log("❌ Operación cancelada")
                self.dibujar_grafo()
                return
            if not obj:
                obj = "null"
            
            # Crear arista
            if respuesta:  # Dirigida
                arista_id = self.grafo.insertaAristaDirigida(self.first_node_for_edge, segundo_nodo, obj)
                tipo = "dirigida →"
            else:  # No dirigida
                arista_id = self.grafo.insertaArista(self.first_node_for_edge, segundo_nodo, obj)
                tipo = "no dirigida ↔"
            
            if arista_id:
                self.log(f"✅ Arista {tipo} creada: {arista_id} ({self.first_node_for_edge} - {segundo_nodo})")
            else:
                self.log(f"❌ Error al crear arista")
            
            self.first_node_for_edge = None
            self.actualizar_interfaz()
    
    def seleccionar_nodo(self, nodo):
        """Selecciona un nodo y muestra su información"""
        self.selected_node = nodo
        self.log(f"🔍 Nodo seleccionado: {nodo}")
        self.mostrar_info_nodo(nodo)
        self.dibujar_grafo(highlight_node=nodo)
    
    def mostrar_info_nodo(self, nodo):
        """Muestra información detallada del nodo"""
        self.node_info_text.config(state=tk.NORMAL)
        self.node_info_text.delete('1.0', tk.END)
        
        info = f"🔵 Vértice: {nodo}\n"
        info += f"{'='*30}\n\n"
        info += f"📊 Grado: {self.grafo.grado(nodo)}\n"
        info += f"📥 Grado Entrada: {self.grafo.gradoEnt(nodo)}\n"
        info += f"📤 Grado Salida: {self.grafo.gradoSalida(nodo)}\n\n"
        
        adyacentes = self.grafo.verticesAdyacentes(nodo)
        info += f"👥 Adyacentes ({len(adyacentes)}):\n"
        info += f"   {adyacentes}\n\n"
        
        adj_ent = self.grafo.verticesAdyacentesEnt(nodo)
        info += f"⬅️ Adyacentes Entrada:\n"
        info += f"   {adj_ent}\n\n"
        
        adj_sal = self.grafo.verticesAdyacentesSal(nodo)
        info += f"➡️ Adyacentes Salida:\n"
        info += f"   {adj_sal}\n\n"
        
        aristas_inc = self.grafo.aristasIncidentes(nodo)
        info += f"🔗 Aristas Incidentes ({len(aristas_inc)}):\n"
        for a in aristas_inc:
            tipo = "→" if self.grafo.esDirigida(a) else "↔"
            vertices = self.grafo.verticesFinales(a)
            info += f"   {a} {tipo} {vertices}\n"
        
        self.node_info_text.insert('1.0', info)
        self.node_info_text.config(state=tk.DISABLED)
    
    def mostrar_menu_contextual(self, event, nodo):
        """Muestra menú contextual para operaciones sobre el nodo"""
        menu = tk.Menu(self.root, tearoff=0, font=('Arial', 9))
        
        menu.add_command(label=f"📋 Info de {nodo}", 
                        command=lambda: self.mostrar_info_nodo(nodo))
        menu.add_separator()
        menu.add_command(label=f"📊 Grado: {self.grafo.grado(nodo)}", state=tk.DISABLED)
        menu.add_command(label=f"📥 Grado Entrada: {self.grafo.gradoEnt(nodo)}", state=tk.DISABLED)
        menu.add_command(label=f"📤 Grado Salida: {self.grafo.gradoSalida(nodo)}", state=tk.DISABLED)
        menu.add_separator()
        
        adyacentes = self.grafo.verticesAdyacentes(nodo)
        menu.add_command(label=f"👥 Ver Adyacentes ({len(adyacentes)})", 
                        command=lambda: self.log(f"Adyacentes de {nodo}: {adyacentes}"))
        
        aristas = self.grafo.aristasIncidentes(nodo)
        menu.add_command(label=f"🔗 Ver Aristas ({len(aristas)})", 
                        command=lambda: self.log(f"Aristas de {nodo}: {aristas}"))
        
        menu.add_separator()
        menu.add_command(label=f"🗑️ Eliminar {nodo}", 
                        command=lambda: self.eliminar_vertice_menu(nodo),
                        foreground='red')
        
        try:
            menu.tk_popup(event.guiEvent.x_root, event.guiEvent.y_root)
        finally:
            menu.grab_release()
    
    def eliminar_vertice_menu(self, nodo):
        """Elimina un vértice desde el menú contextual"""
        if messagebox.askyesno("Confirmar", f"¿Eliminar vértice {nodo}?"):
            if self.grafo.eliminaVertice(nodo):
                self.log(f"🗑️ Vértice {nodo} eliminado")
                if nodo in self.pos:
                    del self.pos[nodo]
                self.selected_node = None
                self.actualizar_interfaz()
            else:
                self.log(f"❌ Error al eliminar {nodo}")
    
    def ejecutar_op_vertice(self, operacion):
        """Ejecuta operación sobre vértice desde el panel"""
        v = self.vertex_op_entry.get().strip()
        if not v:
            messagebox.showwarning("Advertencia", "Ingresa un vértice")
            return
        
        if operacion == 'grado':
            resultado = self.grafo.grado(v)
            self.log(f"📊 grado({v}) = {resultado}")
        elif operacion == 'verticesAdyacentes':
            resultado = self.grafo.verticesAdyacentes(v)
            self.log(f"👥 verticesAdyacentes({v}) = {resultado}")
        elif operacion == 'aristasIncidentes':
            resultado = self.grafo.aristasIncidentes(v)
            self.log(f"🔗 aristasIncidentes({v}) = {resultado}")
    
    def mostrar_info_vertice(self):
        """Muestra información del vértice ingresado"""
        v = self.vertex_op_entry.get().strip()
        if not v:
            messagebox.showwarning("Advertencia", "Ingresa un vértice")
            return
        
        if v not in self.grafo.vertices():
            messagebox.showerror("Error", f"Vértice {v} no existe")
            return
        
        self.seleccionar_nodo(v)
    
    def eliminar_vertice_op(self):
        """Elimina vértice desde el panel de operaciones"""
        v = self.vertex_op_entry.get().strip()
        if not v:
            messagebox.showwarning("Advertencia", "Ingresa un vértice")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar vértice {v}?"):
            if self.grafo.eliminaVertice(v):
                self.log(f"🗑️ Vértice {v} eliminado")
                if v in self.pos:
                    del self.pos[v]
                self.vertex_op_entry.delete(0, tk.END)
                self.actualizar_interfaz()
            else:
                messagebox.showerror("Error", f"Vértice {v} no existe")
    
    def mostrar_info_arista(self):
        """Muestra información de la arista ingresada"""
        e = self.edge_op_entry.get().strip()
        if not e:
            messagebox.showwarning("Advertencia", "Ingresa una arista")
            return
        
        if e not in self.grafo.aristas():
            messagebox.showerror("Error", f"Arista {e} no existe")
            return
        
        info = f"🔗 Arista: {e}\n"
        info += f"{'='*40}\n"
        
        es_dirigida = self.grafo.esDirigida(e)
        tipo = "Dirigida →" if es_dirigida else "No Dirigida ↔"
        info += f"Tipo: {tipo}\n"
        
        vertices = self.grafo.verticesFinales(e)
        info += f"Vértices: {vertices}\n"
        
        if es_dirigida:
            info += f"Origen: {self.grafo.origen(e)}\n"
            info += f"Destino: {self.grafo.destino(e)}\n"
        
        self.log(info)
    
    def invertir_arista_op(self):
        """Invierte dirección de arista"""
        e = self.edge_op_entry.get().strip()
        if not e:
            messagebox.showwarning("Advertencia", "Ingresa una arista")
            return
        
        if self.grafo.invierteDireccion(e):
            self.log(f"⇄ Arista {e} invertida")
            self.actualizar_interfaz()
        else:
            messagebox.showerror("Error", "No se pudo invertir (¿es dirigida?)")
    
    def convertir_no_dirigida_op(self):
        """Convierte arista a no dirigida"""
        e = self.edge_op_entry.get().strip()
        if not e:
            messagebox.showwarning("Advertencia", "Ingresa una arista")
            return
        
        if self.grafo.convierteNoDirigida(e):
            self.log(f"↔️ Arista {e} convertida a NO DIRIGIDA")
            self.actualizar_interfaz()
        else:
            messagebox.showerror("Error", "No se pudo convertir")
    
    def eliminar_arista_op(self):
        """Elimina arista desde el panel"""
        e = self.edge_op_entry.get().strip()
        if not e:
            messagebox.showwarning("Advertencia", "Ingresa una arista")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar arista {e}?"):
            if self.grafo.eliminaArista(e):
                self.log(f"🗑️ Arista {e} eliminada")
                self.edge_op_entry.delete(0, tk.END)
                self.actualizar_interfaz()
            else:
                messagebox.showerror("Error", f"Arista {e} no existe")
    
    def dibujar_grafo(self, highlight_node=None):
        """Dibuja el grafo con visualización mejorada"""
        self.ax.clear()
        
        if self.grafo.numVertices() == 0:
            self.ax.text(0.5, 0.5, 'Grafo vacío\n\n➕ Usa los botones superiores\npara agregar vértices', 
                        ha='center', va='center', fontsize=14, color='#95a5a6',
                        bbox=dict(boxstyle='round', facecolor='white', edgecolor='#bdc3c7'))
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Crear grafo para visualización
        G_visual = nx.DiGraph()
        for v in self.grafo.vertices():
            G_visual.add_node(v)
        
        # Calcular posiciones si no existen
        if not self.pos or len(self.pos) != self.grafo.numVertices():
            try:
                self.pos = nx.spring_layout(G_visual, k=2, iterations=50, seed=42)
            except:
                self.pos = nx.circular_layout(G_visual)
        
        # Separar aristas
        aristas_dirigidas = []
        aristas_no_dirigidas = []
        labels_aristas = {}
        
        for arista_id, info in self.grafo.aristas_info.items():
            v, w = info['vertices']
            if info['dirigida']:
                aristas_dirigidas.append((v, w))
                labels_aristas[(v, w)] = arista_id
            else:
                if (w, v) not in aristas_no_dirigidas:
                    aristas_no_dirigidas.append((v, w))
                    labels_aristas[(v, w)] = arista_id
        
        # Dibujar aristas no dirigidas
        if aristas_no_dirigidas:
            nx.draw_networkx_edges(G_visual, self.pos, edgelist=aristas_no_dirigidas,
                                  edge_color='#3498db', width=3, alpha=0.7,
                                  arrows=False, ax=self.ax, style='solid')
        
        # Dibujar aristas dirigidas
        if aristas_dirigidas:
            nx.draw_networkx_edges(G_visual, self.pos, edgelist=aristas_dirigidas,
                                  edge_color='#e74c3c', width=3, alpha=0.7,
                                  arrows=True, arrowsize=25, arrowstyle='->',
                                  connectionstyle='arc3,rad=0.15', ax=self.ax)
        
        # Colores de nodos
        node_colors = []
        for node in G_visual.nodes():
            if node == highlight_node:
                node_colors.append('#f39c12')  # Naranja para destacar
            else:
                node_colors.append('#2ecc71')  # Verde normal
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G_visual, self.pos, node_color=node_colors,
                              node_size=1000, ax=self.ax, 
                              edgecolors='#27ae60', linewidths=3)
        
        # Etiquetas de nodos
        nx.draw_networkx_labels(G_visual, self.pos, font_size=12, 
                               font_weight='bold', font_color='white', ax=self.ax)
        
        # Etiquetas de aristas (más pequeñas y discretas)
        edge_labels_pos = {}
        for edge, label in labels_aristas.items():
            pos1 = self.pos[edge[0]]
            pos2 = self.pos[edge[1]]
            edge_labels_pos[edge] = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
        
        for edge, pos in edge_labels_pos.items():
            self.ax.text(pos[0], pos[1], labels_aristas[edge], 
                        fontsize=8, color='#9b59b6', weight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                 edgecolor='#9b59b6', alpha=0.8))
        
        # Leyenda
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='#e74c3c', lw=3, label='Arista dirigida →'),
            Line2D([0], [0], color='#3498db', lw=3, label='Arista no dirigida ↔'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ecc71', 
                   markersize=10, label='Vértice', markeredgecolor='#27ae60', markeredgewidth=2)
        ]
        self.ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
        
        self.ax.set_title(f'Grafo: {self.grafo.numVertices()} vértices, ' +
                         f'{self.grafo.numAristas()} aristas', 
                         fontsize=14, weight='bold', pad=20)
        self.ax.axis('off')
        
        # Ajustar límites para mejor visualización
        margin = 0.2
        self.ax.set_xlim(min([p[0] for p in self.pos.values()]) - margin,
                        max([p[0] for p in self.pos.values()]) + margin)
        self.ax.set_ylim(min([p[1] for p in self.pos.values()]) - margin,
                        max([p[1] for p in self.pos.values()]) + margin)
        
        self.canvas.draw()
    
    def actualizar_interfaz(self):
        """Actualiza toda la interfaz"""
        self.dibujar_grafo(highlight_node=self.selected_node)
        self.actualizar_estadisticas()
        if self.selected_node and self.selected_node in self.grafo.vertices():
            self.mostrar_info_nodo(self.selected_node)
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas mostradas"""
        self.stat_vertices.config(text=f"Vértices: {self.grafo.numVertices()}")
        self.stat_aristas.config(text=f"Aristas: {self.grafo.numAristas()}")
        self.stat_dirigidas.config(text=f"Dirigidas: {len(self.grafo.aristasDirigidas())}")
        self.stat_no_dirigidas.config(text=f"No Dirigidas: {len(self.grafo.aristasNodirigidas())}")
    
    def log(self, mensaje):
        """Agrega mensaje a la consola"""
        self.output_text.insert(tk.END, f"{mensaje}\n")
        self.output_text.see(tk.END)
    
    def limpiar_grafo(self):
        """Limpia todo el grafo"""
        if self.grafo.numVertices() == 0:
            messagebox.showinfo("Info", "El grafo ya está vacío")
            return
            
        if messagebox.askyesno("Confirmar", "¿Eliminar todo el grafo?"):
            self.grafo = Grafo()
            self.pos = {}
            self.selected_node = None
            self.first_node_for_edge = None
            self.output_text.delete(1.0, tk.END)
            self.log("🗑️ Grafo limpiado completamente")
            self.log("✨ Listo para comenzar de nuevo")
            self.actualizar_interfaz()


if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoGUI(root)
    root.mainloop()