# -*- coding: utf-8 -*-
"""
App interactiva de grafos sobre el mapa real de México usando Cartopy.
Ahora con zoom:
- Rueda del mouse para acercar/alejar centrado en el cursor
- Botón "Centrar en selección" (auto-zoom a los estados activos)
- Botón "Restablecer vista"
- Barra de herramientas Matplotlib (pan/zoom)
"""

import itertools
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import math
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Cartopy
try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from cartopy.io import shapereader
    CARTOPY_AVAILABLE = True
except ImportError:
    CARTOPY_AVAILABLE = False
    print("⚠️ Cartopy no está instalado. Usando visualización básica.")

# -------------------------------
# Coordenadas de capitales (lat, lon)
# -------------------------------
CAPITALES_MX = {
    "Aguascalientes": (21.88, -102.29),
    "Baja California": (32.63, -115.45),
    "Baja California Sur": (24.14, -110.31),
    "Campeche": (19.85, -90.53),
    "Chiapas": (16.75, -93.12),
    "Chihuahua": (28.64, -106.08),
    "CDMX": (19.43, -99.13),
    "Coahuila": (25.42, -101.00),
    "Colima": (19.24, -103.72),
    "Durango": (24.03, -104.67),
    "Guanajuato": (21.02, -101.26),
    "Guerrero": (17.55, -99.50),
    "Hidalgo": (20.12, -98.73),
    "Jalisco": (20.67, -103.35),
    "México": (19.29, -99.65),
    "Michoacán": (19.70, -101.19),
    "Morelos": (18.92, -99.23),
    "Nayarit": (21.50, -104.90),
    "Nuevo León": (25.67, -100.31),
    "Oaxaca": (17.06, -96.72),
    "Puebla": (19.04, -98.20),
    "Querétaro": (20.59, -100.39),
    "Quintana Roo": (18.50, -88.30),
    "San Luis Potosí": (22.16, -100.98),
    "Sinaloa": (24.80, -107.39),
    "Sonora": (29.07, -110.97),
    "Tabasco": (17.99, -92.93),
    "Tamaulipas": (23.73, -99.14),
    "Tlaxcala": (19.32, -98.24),
    "Veracruz": (19.54, -96.91),
    "Yucatán": (20.97, -89.62),
    "Zacatecas": (22.77, -102.57),
}

# -------------------------------
# Algoritmos de recorrido
# -------------------------------
def hamiltoniano_minimo(G):
    nodes = list(G.nodes())
    if len(nodes) == 0:
        return None, None
    mejor_coste = float("inf")
    mejor_camino = None
    for perm in itertools.permutations(nodes):
        coste = 0.0
        valido = True
        for i in range(len(perm) - 1):
            u, v = perm[i], perm[i + 1]
            if not G.has_edge(u, v):
                valido = False
                break
            coste += G[u][v]["weight"]
        if valido and coste < mejor_coste:
            mejor_coste = coste
            mejor_camino = list(perm)
    if mejor_camino is None:
        return None, None
    return mejor_coste, mejor_camino


def _diametro_en_arbol(T):
    if T.number_of_nodes() == 0:
        return 0, []
    inicio = next(iter(T.nodes()))
    dist1, _ = nx.single_source_dijkstra(T, source=inicio, weight="weight")
    nodo_extremo1 = max(dist1, key=dist1.get)
    dist2, paths2 = nx.single_source_dijkstra(T, source=nodo_extremo1, weight="weight")
    nodo_extremo2 = max(dist2, key=dist2.get)
    camino = paths2[nodo_extremo2]
    return dist2[nodo_extremo2], camino


def recorrido_con_repeticiones(G):
    if G.number_of_nodes() == 0:
        return 0.0, []
    if not nx.is_connected(G):
        return None, None
    T = nx.minimum_spanning_tree(G, weight="weight")
    _, diam_camino = _diametro_en_arbol(T)

    M = nx.MultiGraph()
    M.add_nodes_from(T.nodes())

    diam_edges = set()
    for i in range(len(diam_camino) - 1):
        a, b = diam_camino[i], diam_camino[i + 1]
        diam_edges.add(tuple(sorted((a, b))))

    for u, v, d in T.edges(data=True):
        M.add_edge(u, v, weight=d["weight"])
    for u, v, d in T.edges(data=True):
        if tuple(sorted((u, v))) not in diam_edges:
            M.add_edge(u, v, weight=d["weight"])

    inicio = diam_camino[0] if diam_camino else next(iter(T.nodes()))
    try:
        path_edges = list(nx.eulerian_path(M, source=inicio))
    except nx.NetworkXError:
        try:
            path_edges = list(nx.eulerian_path(M))
        except Exception:
            return None, None

    if not path_edges:
        return 0.0, [inicio]

    recorrido = [path_edges[0][0]]
    for u, v in path_edges:
        recorrido.append(v)

    costo = 0.0
    for i in range(len(recorrido) - 1):
        u, v = recorrido[i], recorrido[i + 1]
        if T.has_edge(u, v):
            costo += T[u][v]["weight"]
    return costo, recorrido


# -------------------------------
# Aplicación principal
# -------------------------------
class AppGrafoMexico:
    def __init__(self, root):
        self.root = root
        self.root.title("🗺️ Grafo Interactivo - República Mexicana")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        self.G = nx.Graph()
        self.activos = set()
        self.seleccion_par = []
        self.resalta_a = []
        self.resalta_b = []

        self.modo_actual = "seleccionar"

        self.crear_interfaz()
        self.dibujar_mapa()

    # ---------------- UI ----------------
    def crear_interfaz(self):
        titulo_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        titulo_frame.pack(side=tk.TOP, fill=tk.X)
        titulo_frame.pack_propagate(False)
        tk.Label(titulo_frame, text="🗺️ Visualizador de Grafos - República Mexicana",
                 font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)

        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo (mapa)
        left_panel = tk.Frame(main_container, bg='white', relief=tk.RIDGE, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        instr_frame = tk.Frame(left_panel, bg='#e3f2fd', relief=tk.RIDGE, bd=2)
        instr_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(instr_frame, text="📖 INSTRUCCIONES",
                 font=('Arial', 11, 'bold'), bg='#e3f2fd', fg='#0d47a1').pack(pady=5)
        tk.Label(instr_frame, text="1) Clic normal: seleccionar/deseleccionar (máx 7).",
                 font=('Arial', 9), bg='#e3f2fd').pack(anchor='w', padx=10)
        tk.Label(instr_frame, text="2) Modo CONECTAR: clic en estado 1 y estado 2 para crear arista.",
                 font=('Arial', 9), bg='#e3f2fd').pack(anchor='w', padx=10)
        tk.Label(instr_frame, text="3) Zoom: rueda del mouse; Pan/Zoom en barra inferior.",
                 font=('Arial', 9), bg='#e3f2fd').pack(anchor='w', padx=10)

        modo_frame = tk.Frame(left_panel, bg='white')
        modo_frame.pack(fill=tk.X, padx=10, pady=(0, 6))
        self.label_modo = tk.Label(modo_frame, text="📍 Modo: SELECCIONAR ESTADOS",
                                   font=('Arial', 10, 'bold'), bg='white', fg='#2ecc71')
        self.label_modo.pack(side=tk.LEFT, padx=10)
        self.btn_cambiar_modo = tk.Button(
            modo_frame, text="🔗 Cambiar a Modo CONECTAR",
            command=self.cambiar_modo, bg='#3498db', fg='white',
            font=('Arial', 9, 'bold'), padx=12, pady=4, cursor='hand2'
        )
        self.btn_cambiar_modo.pack(side=tk.LEFT)

        # Figura
        if CARTOPY_AVAILABLE:
            self.fig = plt.figure(figsize=(10, 8))
            self.ax = plt.axes(projection=ccrs.PlateCarree())
            self.default_extent = [-118, -86, 14, 33]
            self._configurar_mapa_cartopy()
        else:
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
            self.default_xlim = (-118, -86)
            self.default_ylim = (14, 33)
            self.ax.set_title("Mapa de México (modo básico)")
            self.ax.set_xlim(*self.default_xlim)
            self.ax.set_ylim(*self.default_ylim)
            self.ax.set_aspect('equal')

        self.canvas = FigureCanvasTkAgg(self.fig, master=left_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(6, 0))

        # Barra de herramientas Matplotlib (pan/zoom)
        toolbar = NavigationToolbar2Tk(self.canvas, left_panel, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Eventos de mouse
        self.canvas.mpl_connect("button_press_event", self.on_click_mapa)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)

        # Panel derecho
        right_panel = tk.Frame(main_container, bg='#ecf0f1', width=420)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_panel.pack_propagate(False)

        info_frame = tk.LabelFrame(right_panel, text="📊 Estados Seleccionados",
                                   font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 8))
        self.label_estados = tk.Label(info_frame, text="0/7 estados seleccionados",
                                      font=('Arial', 10), bg='white')
        self.label_estados.pack()

        control_frame = tk.LabelFrame(right_panel, text="⚙️ Controles",
                                      font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        control_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Button(control_frame, text="🔄 Reiniciar Todo", command=self.reiniciar,
                  bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)
        tk.Button(control_frame, text="📋 Mostrar Estados y Relaciones",
                  command=self.mostrar_relaciones,
                  bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)
        tk.Button(control_frame, text="🧹 Limpiar Rutas Resaltadas",
                  command=self.limpiar_resaltados,
                  bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)

        # Zoom helpers
        zoom_frame = tk.LabelFrame(right_panel, text="🔎 Zoom",
                                   font=('Arial', 11, 'bold'), bg='white', padx=10, pady=8)
        zoom_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Button(zoom_frame, text="🎯 Centrar en selección",
                  command=self.centrar_en_seleccion,
                  bg='#16a34a', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)
        tk.Button(zoom_frame, text="↩️ Restablecer vista",
                  command=self.reset_vista,
                  bg='#6b7280', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)

        calc_frame = tk.LabelFrame(right_panel, text="🧮 Cálculos de Recorridos",
                                   font=('Arial', 11, 'bold'), bg='white', padx=10, pady=10)
        calc_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Button(calc_frame, text="(a) Recorrido SIN Repetir Estados",
                  command=self.calcular_sin_repetir,
                  bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)
        tk.Button(calc_frame, text="(b) Recorrido CON Repeticiones (MST)",
                  command=self.calcular_con_repeticiones,
                  bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                  pady=6, cursor='hand2').pack(fill=tk.X, pady=3)

        output_frame = tk.LabelFrame(right_panel, text="📝 Resultados",
                                     font=('Arial', 11, 'bold'), bg='white')
        output_frame.pack(fill=tk.BOTH, expand=True)
        self.output = ScrolledText(output_frame, wrap="word", font=('Consolas', 9),
                                   bg='#2c3e50', fg='#ecf0f1', insertbackground='white')
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log("✨ Bienvenido al Visualizador de Grafos de México")
        self.log("📍 Usa la rueda del mouse para hacer zoom, o la barra inferior para Pan/Zoom.")
        self.log("🔗 Cambia a MODO CONECTAR para unir dos estados con un costo.\n")

    def cambiar_modo(self):
        if self.modo_actual == "seleccionar":
            self.modo_actual = "conectar"
            self.label_modo.config(text="📍 Modo: CONECTAR ESTADOS", fg="#e67e22")
            self.btn_cambiar_modo.config(text="🖱️ Cambiar a Modo SELECCIONAR")
            self.seleccion_par.clear()
            self.log("🔗 Modo CONECTAR activado. Clic en dos estados activos para unirlos.\n")
        else:
            self.modo_actual = "seleccionar"
            self.label_modo.config(text="📍 Modo: SELECCIONAR ESTADOS", fg="#2ecc71")
            self.btn_cambiar_modo.config(text="🔗 Cambiar a Modo CONECTAR")
            self.seleccion_par.clear()
            self.log("🖱️ Modo SELECCIONAR activado. Clic normal para (de)activar estados.\n")

    # ---------------- Mapa ----------------
    def _configurar_mapa_cartopy(self):
        self.ax.set_extent([-118, -86, 14, 33], crs=ccrs.PlateCarree())
        self.ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor='#FFF8E7')
        self.ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor='#B3E5FC')
        self.ax.add_feature(cfeature.LAKES.with_scale("50m"), edgecolor='none', facecolor='#B3E5FC')
        self.ax.add_feature(cfeature.BORDERS.with_scale("50m"), linewidth=1.2, edgecolor='#546E7A')
        try:
            shp = shapereader.natural_earth(resolution="10m",
                                            category="cultural",
                                            name="admin_1_states_provinces_lines")
            reader = shapereader.Reader(shp)
            geometrias = []
            for rec in reader.records():
                if rec.attributes.get("adm0_name") == "Mexico" or rec.attributes.get("admin") == "Mexico":
                    geometrias.append(rec.geometry)
            self.ax.add_geometries(geometrias, crs=ccrs.PlateCarree(),
                                   facecolor="none", edgecolor='#78909C',
                                   linewidth=0.8, zorder=1.5)
        except Exception as e:
            self.log(f"⚠️ No se pudieron cargar límites estatales: {e}\n")
        self.ax.gridlines(draw_labels=False, linewidth=0.5, color='gray', alpha=0.3, linestyle='--')

    def dibujar_mapa(self):
        self.ax.clear()
        if CARTOPY_AVAILABLE:
            self._configurar_mapa_cartopy()
            # mantener la extensión actual si ya existe
            # (Cartopy resetea a veces; así que no tocamos extent aquí)
        else:
            if not hasattr(self, "default_xlim"):
                self.default_xlim = (-118, -86)
                self.default_ylim = (14, 33)
            if not hasattr(self, "_lim_guard"):
                self.ax.set_xlim(*self.default_xlim)
                self.ax.set_ylim(*self.default_ylim)
                self._lim_guard = True
            self.ax.set_aspect('equal')

        transform = ccrs.PlateCarree() if CARTOPY_AVAILABLE else None

        # Aristas
        for u, v, data in self.G.edges(data=True):
            lat1, lon1 = CAPITALES_MX[u]
            lat2, lon2 = CAPITALES_MX[v]
            kwargs = {'transform': transform} if CARTOPY_AVAILABLE else {}
            self.ax.plot([lon1, lon2], [lat1, lat2],
                         linewidth=2.5, color='#64748b', zorder=3, alpha=0.8, **kwargs)
            mx, my = (lon1 + lon2) / 2, (lat1 + lat2) / 2
            self.ax.text(mx, my, f"{data['weight']:.0f}",
                         fontsize=9, ha='center', va='center',
                         bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#64748b', alpha=0.95),
                         zorder=5, **kwargs)

        # Resaltados
        for (u, v) in self.resalta_a:
            lat1, lon1 = CAPITALES_MX[u]; lat2, lon2 = CAPITALES_MX[v]
            kwargs = {'transform': transform} if CARTOPY_AVAILABLE else {}
            self.ax.plot([lon1, lon2], [lat1, lat2], linewidth=4, color='#22c55e', zorder=4, **kwargs)
        for (u, v) in self.resalta_b:
            lat1, lon1 = CAPITALES_MX[u]; lat2, lon2 = CAPITALES_MX[v]
            kwargs = {'transform': transform} if CARTOPY_AVAILABLE else {}
            self.ax.plot([lon1, lon2], [lat1, lat2], linewidth=4, color='#f59e0b',
                         linestyle='--', zorder=4, **kwargs)

        # Nodos
        for nombre, (lat, lon) in CAPITALES_MX.items():
            kwargs = {'transform': transform} if CARTOPY_AVAILABLE else {}
            if nombre in self.activos:
                self.ax.scatter(lon, lat, s=120, color='#10b981',
                                edgecolor='#065f46', linewidth=2.2, zorder=6, **kwargs)
                self.ax.text(lon, lat + 0.25, nombre, ha='center', va='bottom',
                             fontsize=9, fontweight='bold', color='#065f46', zorder=7, **kwargs)
            else:
                self.ax.scatter(lon, lat, s=60, color='#cbd5e1',
                                edgecolor='#64748b', linewidth=1.3, zorder=2, **kwargs)
                self.ax.text(lon, lat + 0.25, nombre, ha='center', va='bottom',
                             fontsize=7.5, color='#475569', zorder=2, **kwargs)

        self.label_estados.config(text=f"{len(self.activos)}/7 estados seleccionados")
        self.fig.tight_layout()
        self.canvas.draw_idle()

    # ---------------- Zoom y navegación ----------------
    def on_scroll(self, event):
        """Zoom con la rueda del mouse centrado en el cursor."""
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        zoom_in = (event.button == 'up')
        factor = 0.9 if zoom_in else 1.1  # <1 acerca, >1 aleja

        if CARTOPY_AVAILABLE:
            x0, x1, y0, y1 = self.ax.get_extent(crs=ccrs.PlateCarree())
            cx, cy = float(event.xdata), float(event.ydata)
            wx = (x1 - x0) * 0.5 * factor
            wy = (y1 - y0) * 0.5 * factor
            self.ax.set_extent([cx - wx, cx + wx, cy - wy, cy + wy], crs=ccrs.PlateCarree())
        else:
            x0, x1 = self.ax.get_xlim()
            y0, y1 = self.ax.get_ylim()
            cx, cy = float(event.xdata), float(event.ydata)
            wx = (x1 - x0) * 0.5 * factor
            wy = (y1 - y0) * 0.5 * factor
            self.ax.set_xlim(cx - wx, cx + wx)
            self.ax.set_ylim(cy - wy, cy + wy)

        self.canvas.draw_idle()

    def centrar_en_seleccion(self):
        """Auto-zoom para encuadrar los estados activos con un margen."""
        if not self.activos:
            messagebox.showinfo("Sin selección", "Selecciona al menos un estado.")
            return
        lats, lons = [], []
        for est in self.activos:
            lat, lon = CAPITALES_MX[est]
            lats.append(lat); lons.append(lon)
        min_lon, max_lon = min(lons), max(lons)
        min_lat, max_lat = min(lats), max(lats)
        # margen en grados
        pad_lon = max(1.5, (max_lon - min_lon) * 0.25)
        pad_lat = max(1.0, (max_lat - min_lat) * 0.25)
        x0 = min_lon - pad_lon; x1 = max_lon + pad_lon
        y0 = min_lat - pad_lat; y1 = max_lat + pad_lat

        if CARTOPY_AVAILABLE:
            self.ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())
        else:
            self.ax.set_xlim(x0, x1)
            self.ax.set_ylim(y0, y1)

        self.canvas.draw_idle()

    def reset_vista(self):
        """Restablece la vista al encuadre de México."""
        if CARTOPY_AVAILABLE:
            self.ax.set_extent(self.default_extent, crs=ccrs.PlateCarree())
        else:
            self.ax.set_xlim(*self.default_xlim)
            self.ax.set_ylim(*self.default_ylim)
        self.canvas.draw_idle()

    # ---------------- Interacción de grafo ----------------
    def on_click_mapa(self, event):
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return
        lon_clic, lat_clic = float(event.xdata), float(event.ydata)
        estado_cercano, dist_minima = None, float('inf')
        umbral = 1.0
        for nombre, (lat, lon) in CAPITALES_MX.items():
            d = math.hypot(lon - lon_clic, lat - lat_clic)
            if d < dist_minima:
                dist_minima = d; estado_cercano = nombre
        if dist_minima > umbral:
            return
        if self.modo_actual == "conectar":
            self.manejar_conexion(estado_cercano)
        else:
            self.alternar_estado(estado_cercano)

    def alternar_estado(self, estado):
        if estado in self.activos:
            self.activos.remove(estado)
            if estado in self.G:
                self.G.remove_node(estado)
            self.log(f"❌ Desactivado: {estado} ({len(self.activos)}/7)\n")
        else:
            if len(self.activos) >= 7:
                messagebox.showwarning("Límite alcanzado",
                                       "Solo puedes seleccionar 7 estados.\nDesactiva uno primero.")
                return
            self.activos.add(estado)
            if estado not in self.G:
                self.G.add_node(estado)
            self.log(f"✅ Activado: {estado} ({len(self.activos)}/7)\n")
        if self.modo_actual == "conectar":
            self.seleccion_par.clear()
        self.dibujar_mapa()

    def manejar_conexion(self, estado):
        if estado not in self.activos:
            messagebox.showinfo("Estado no activo",
                                f"{estado} no está activo.\nPrimero actívalo con clic normal.")
            return
        if estado in self.seleccion_par:
            self.seleccion_par.remove(estado); self.log(f"🔹 Deseleccionado: {estado}\n")
        else:
            if len(self.seleccion_par) < 2:
                self.seleccion_par.append(estado); self.log(f"🔹 Seleccionado: {estado}\n")
            else:
                self.seleccion_par = [estado]; self.log(f"🔹 Nueva selección: {estado}\n")
        if len(self.seleccion_par) == 2:
            self.crear_arista()
        else:
            self.dibujar_mapa()

    def crear_arista(self):
        if len(self.seleccion_par) != 2:
            return
        u, v = self.seleccion_par
        if u == v:
            self.seleccion_par = []; return
        costo = simpledialog.askfloat(
            "Costo de Conexión",
            f"Ingresa el costo de traslado entre:\n{u} ↔ {v}\n\n(En kilómetros o unidades de costo)",
            minvalue=0.0, initialvalue=100.0
        )
        if costo is None:
            self.log(f"❌ Conexión cancelada: {u} ↔ {v}\n")
            self.seleccion_par = []; self.dibujar_mapa(); return
        if self.G.has_edge(u, v):
            if float(costo) < self.G[u][v]["weight"]:
                self.G[u][v]["weight"] = float(costo)
                self.log(f"🔄 Actualizado: {u} ↔ {v} = {costo:.0f}\n")
            else:
                self.log(f"ℹ️ Ya existe {u} ↔ {v} con menor costo\n")
        else:
            self.G.add_edge(u, v, weight=float(costo))
            self.log(f"🔗 Conectado: {u} ↔ {v} = {costo:.0f}\n")
        self.seleccion_par = []
        self.limpiar_resaltados(silencioso=True)
        self.dibujar_mapa()

    def calcular_sin_repetir(self):
        self.limpiar_resaltados(silencioso=True)
        if len(self.activos) != 7:
            messagebox.showwarning("Estados insuficientes", "Necesitas exactamente 7 estados seleccionados.")
            return
        subgrafo = self.G.subgraph(self.activos).copy()
        if not nx.is_connected(subgrafo):
            messagebox.showwarning("Grafo no conexo", "Los 7 estados deben estar conectados.\nAgrega más conexiones.")
            return
        costo, camino = hamiltoniano_minimo(subgrafo)
        if camino is None:
            messagebox.showinfo("Sin solución", "No existe un camino Hamiltoniano.\nFaltan conexiones.")
            return
        self.log("\n" + "="*50)
        self.log("\n(a) RECORRIDO SIN REPETIR ESTADOS")
        self.log("\n" + "="*50 + "\n")
        self.log(f"📍 Camino: {' → '.join(camino)}\n")
        self.log(f"💰 Costo total: {costo:.2f} unidades\n")
        self.log("="*50 + "\n")
        self.resalta_a = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
        self.dibujar_mapa()

    def calcular_con_repeticiones(self):
        self.limpiar_resaltados(silencioso=True)
        if len(self.activos) != 7:
            messagebox.showwarning("Estados insuficientes", "Necesitas exactamente 7 estados seleccionados.")
            return
        subgrafo = self.G.subgraph(self.activos).copy()
        if not nx.is_connected(subgrafo):
            messagebox.showwarning("Grafo no conexo", "Los 7 estados deben estar conectados.\nAgrega más conexiones.")
            return
        costo, recorrido = recorrido_con_repeticiones(subgrafo)
        if recorrido is None:
            messagebox.showerror("Error", "No se pudo calcular el recorrido.")
            return
        self.log("\n" + "="*50)
        self.log("\n(b) RECORRIDO PERMITIENDO REPETICIONES")
        self.log("\n" + "="*50 + "\n")
        self.log(f"📍 Recorrido: {' → '.join(recorrido)}\n")
        self.log(f"💰 Costo total: {costo:.2f} unidades\n")
        repetidos = [e for e in set(recorrido) if recorrido.count(e) > 1]
        if repetidos:
            self.log(f"🔄 Estados repetidos: {', '.join(repetidos)}\n")
        self.log("="*50 + "\n")
        self.resalta_b = [(recorrido[i], recorrido[i+1]) for i in range(len(recorrido)-1)]
        self.dibujar_mapa()

    def mostrar_relaciones(self):
        if len(self.activos) == 0:
            messagebox.showinfo("Sin estados", "No hay estados seleccionados.")
            return
        subgrafo = self.G.subgraph(self.activos).copy()
        self.log("\n" + "="*50)
        self.log("\n📊 ESTADOS Y SUS RELACIONES")
        self.log("\n" + "="*50 + "\n")
        for estado in sorted(self.activos):
            vecinos = list(sorted(subgrafo.neighbors(estado)))
            if vecinos:
                self.log(f"🔵 {estado}:\n")
                for v in vecinos:
                    self.log(f"   → {v} (costo: {subgrafo[estado][v]['weight']:.0f})\n")
            else:
                self.log(f"🔵 {estado}: (sin conexiones)\n")
        self.log(f"\n📈 Total de estados: {len(self.activos)}")
        self.log(f"\n🔗 Total de conexiones: {subgrafo.number_of_edges()}")
        self.log(f"\n✅ Grafo conexo: {'Sí' if nx.is_connected(subgrafo) else 'No'}\n")
        self.log("="*50 + "\n")

    def limpiar_resaltados(self, silencioso=False):
        self.resalta_a = []
        self.resalta_b = []
        self.dibujar_mapa()
        if not silencioso:
            self.log("🧹 Rutas resaltadas limpiadas\n")

    def reiniciar(self):
        if len(self.activos) == 0 and self.G.number_of_edges() == 0:
            messagebox.showinfo("Ya limpio", "No hay nada que reiniciar.")
            return
        if messagebox.askyesno("Confirmar Reinicio", "¿Eliminar todos los estados y conexiones?"):
            self.G.clear(); self.activos.clear(); self.seleccion_par.clear()
            self.resalta_a = []; self.resalta_b = []
            self.output.delete(1.0, tk.END)
            self.reset_vista()
            self.log("🔄 Sistema reiniciado completamente\n")
            self.dibujar_mapa()

    def log(self, mensaje):
        self.output.insert(tk.END, mensaje)
        self.output.see(tk.END)
        self.output.update_idletasks()


# -------------------------------
# Función principal
# -------------------------------
def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        available_themes = style.theme_names()
        if "clam" in available_themes:
            style.theme_use("clam")
        elif "vista" in available_themes:
            style.theme_use("vista")
    except Exception:
        pass

    if not CARTOPY_AVAILABLE:
        respuesta = messagebox.askyesno(
            "Cartopy no disponible",
            "Cartopy no está instalado. El programa funcionará en modo básico sin el mapa detallado.\n\n"
            "Para instalar Cartopy:\n"
            "pip install cartopy\n\n"
            "¿Deseas continuar en modo básico?",
            icon='warning'
        )
        if not respuesta:
            root.destroy()
            return

    app = AppGrafoMexico(root)
    if CARTOPY_AVAILABLE:
        app.log("✅ Cartopy cargado correctamente\n")
    else:
        app.log("⚠️ Modo básico (sin Cartopy)\n")
    root.mainloop()


if __name__ == "__main__":
    main()
