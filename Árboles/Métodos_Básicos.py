import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import deque

# =========================
#  Modelo: Nodo y Árbol
# =========================

class Nodo:
    """Clase que representa un nodo del árbol"""
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.x = 0
        self.y = 0

class ArbolBinario:
    """Clase que implementa un Árbol Binario de Búsqueda"""
    def __init__(self):
        self.raiz = None
    
    def es_vacio(self):
        return self.raiz is None
    
    # --------- INSERTAR ---------
    def insertar(self, valor):
        pasos = []
        info = {"path": [], "current": None, "found": None, "inserted": None}
        if self.es_vacio():
            self.raiz = Nodo(valor)
            pasos.append(f"✓ El árbol estaba vacío. {valor} insertado como raíz")
            info["path"] = [self.raiz]
            info["current"] = self.raiz
            info["inserted"] = self.raiz
            return pasos, info
        
        return self._insertar_recursivo(self.raiz, valor, pasos, info)
    
    def _insertar_recursivo(self, nodo, valor, pasos, info):
        info["current"] = nodo
        info["path"].append(nodo)

        if valor < nodo.valor:
            pasos.append(f"{valor} < {nodo.valor} → ir a la IZQUIERDA")
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
                pasos.append(f"✓ {valor} insertado como hijo izquierdo de {nodo.valor}")
                info["inserted"] = nodo.izquierdo
                info["path"].append(nodo.izquierdo)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor, pasos, info)
        elif valor > nodo.valor:
            pasos.append(f"{valor} > {nodo.valor} → ir a la DERECHA")
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
                pasos.append(f"✓ {valor} insertado como hijo derecho de {nodo.valor}")
                info["inserted"] = nodo.derecho
                info["path"].append(nodo.derecho)
            else:
                self._insertar_recursivo(nodo.derecho, valor, pasos, info)
        else:
            pasos.append(f"✗ {valor} ya existe en el árbol")
            info["found"] = nodo
        return pasos, info
    
    # --------- BUSCAR ---------
    def buscar(self, valor):
        pasos = []
        info = {"path": [], "current": None, "found": None, "inserted": None}
        if self.es_vacio():
            pasos.append("✗ El árbol está vacío")
            return (False, pasos, info)
        
        return self._buscar_recursivo(self.raiz, valor, pasos, info)
    
    def _buscar_recursivo(self, nodo, valor, pasos, info):
        if nodo is None:
            pasos.append(f"✗ Elemento {valor} NO encontrado")
            return (False, pasos, info)
        
        info["current"] = nodo
        info["path"].append(nodo)
        pasos.append(f"Visitando nodo: {nodo.valor}")
        
        if valor == nodo.valor:
            pasos.append(f"✓ ¡Elemento {valor} ENCONTRADO!")
            info["found"] = nodo
            return (True, pasos, info)
        elif valor < nodo.valor:
            pasos.append(f"{valor} < {nodo.valor} → buscar en IZQUIERDA")
            return self._buscar_recursivo(nodo.izquierdo, valor, pasos, info)
        else:
            pasos.append(f"{valor} > {nodo.valor} → buscar en DERECHA")
            return self._buscar_recursivo(nodo.derecho, valor, pasos, info)
    
    # --------- RECORRIDOS ---------
    def pre_orden(self):
        resultado = []
        self._pre_orden_recursivo(self.raiz, resultado)
        return resultado
    
    def _pre_orden_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.valor)
            self._pre_orden_recursivo(nodo.izquierdo, resultado)
            self._pre_orden_recursivo(nodo.derecho, resultado)
    
    def in_orden(self):
        resultado = []
        self._in_orden_recursivo(self.raiz, resultado)
        return resultado
    
    def _in_orden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._in_orden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._in_orden_recursivo(nodo.derecho, resultado)
    
    def post_orden(self):
        resultado = []
        self._post_orden_recursivo(self.raiz, resultado)
        return resultado
    
    def _post_orden_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._post_orden_recursivo(nodo.izquierdo, resultado)
            self._post_orden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.valor)
    
    def por_niveles(self):
        if self.es_vacio():
            return []
        resultado = []
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.valor)
            if nodo.izquierdo: cola.append(nodo.izquierdo)
            if nodo.derecho: cola.append(nodo.derecho)
        return resultado
    
    def altura(self):
        return self._altura_recursiva(self.raiz)
    
    def _altura_recursiva(self, nodo):
        if nodo is None:
            return 0
        return max(self._altura_recursiva(nodo.izquierdo), 
                   self._altura_recursiva(nodo.derecho)) + 1
    
    def contar_hojas(self):
        return self._contar_hojas_recursivo(self.raiz)
    
    def _contar_hojas_recursivo(self, nodo):
        if nodo is None:
            return 0
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        return (self._contar_hojas_recursivo(nodo.izquierdo) + 
                self._contar_hojas_recursivo(nodo.derecho))
    
    def contar_nodos(self):
        return self._contar_nodos_recursivo(self.raiz)
    
    def _contar_nodos_recursivo(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_nodos_recursivo(nodo.izquierdo) + self._contar_nodos_recursivo(nodo.derecho)
    
    def es_completo(self):
        if self.es_vacio():
            return True
        cola = deque([self.raiz])
        incompleto = False
        while cola:
            nodo = cola.popleft()
            if nodo.izquierdo:
                if incompleto: return False
                cola.append(nodo.izquierdo)
            else:
                incompleto = True
            if nodo.derecho:
                if incompleto: return False
                cola.append(nodo.derecho)
            else:
                incompleto = True
        return True
    
    def es_lleno(self):
        return self._es_lleno_recursivo(self.raiz)
    
    def _es_lleno_recursivo(self, nodo):
        if nodo is None:
            return True
        if nodo.izquierdo is None and nodo.derecho is None:
            return True
        if nodo.izquierdo is not None and nodo.derecho is not None:
            return self._es_lleno_recursivo(nodo.izquierdo) and self._es_lleno_recursivo(nodo.derecho)
        return False
    
    # --------- ELIMINAR (predecesor/sucesor) ---------
    def eliminar_predecesor(self, valor):
        pasos = []
        info = {"path": [], "current": None, "found": None, "inserted": None}
        self.raiz, _ = self._eliminar_predecesor_recursivo(self.raiz, valor, pasos, info)
        return pasos, info
    
    def _eliminar_predecesor_recursivo(self, nodo, valor, pasos, info):
        if nodo is None:
            pasos.append(f"✗ Valor {valor} no encontrado")
            return None, False
        
        info["current"] = nodo
        info["path"].append(nodo)

        if valor < nodo.valor:
            pasos.append(f"{valor} < {nodo.valor} → ir a IZQUIERDA")
            nodo.izquierdo, eliminado = self._eliminar_predecesor_recursivo(nodo.izquierdo, valor, pasos, info)
            return nodo, eliminado
        elif valor > nodo.valor:
            pasos.append(f"{valor} > {nodo.valor} → ir a DERECHA")
            nodo.derecho, eliminado = self._eliminar_predecesor_recursivo(nodo.derecho, valor, pasos, info)
            return nodo, eliminado
        else:
            pasos.append(f"✓ Nodo {valor} encontrado")
            info["found"] = nodo
            if nodo.izquierdo is None and nodo.derecho is None:
                pasos.append(f"→ Nodo {valor} es HOJA, se elimina directamente")
                return None, True
            elif nodo.izquierdo is None:
                pasos.append(f"→ Nodo {valor} solo tiene hijo DERECHO")
                return nodo.derecho, True
            elif nodo.derecho is None:
                pasos.append(f"→ Nodo {valor} solo tiene hijo IZQUIERDO")
                return nodo.izquierdo, True
            else:
                pasos.append(f"→ Nodo {valor} tiene DOS hijos")
                pasos.append(f"→ Buscando PREDECESOR (máximo del subárbol izquierdo)...")
                predecesor = self._encontrar_maximo(nodo.izquierdo)
                pasos.append(f"→ Predecesor encontrado: {predecesor.valor}")
                pasos.append(f"→ Reemplazando {valor} con {predecesor.valor}")
                nodo.valor = predecesor.valor
                nodo.izquierdo, _ = self._eliminar_predecesor_recursivo(nodo.izquierdo, predecesor.valor, pasos, info)
                return nodo, True
    
    def eliminar_sucesor(self, valor):
        pasos = []
        info = {"path": [], "current": None, "found": None, "inserted": None}
        self.raiz, _ = self._eliminar_sucesor_recursivo(self.raiz, valor, pasos, info)
        return pasos, info
    
    def _eliminar_sucesor_recursivo(self, nodo, valor, pasos, info):
        if nodo is None:
            pasos.append(f"✗ Valor {valor} no encontrado")
            return None, False
        
        info["current"] = nodo
        info["path"].append(nodo)

        if valor < nodo.valor:
            pasos.append(f"{valor} < {nodo.valor} → ir a IZQUIERDA")
            nodo.izquierdo, eliminado = self._eliminar_sucesor_recursivo(nodo.izquierdo, valor, pasos, info)
            return nodo, eliminado
        elif valor > nodo.valor:
            pasos.append(f"{valor} > {nodo.valor} → ir a DERECHA")
            nodo.derecho, eliminado = self._eliminar_sucesor_recursivo(nodo.derecho, valor, pasos, info)
            return nodo, eliminado
        else:
            pasos.append(f"✓ Nodo {valor} encontrado")
            info["found"] = nodo
            if nodo.izquierdo is None and nodo.derecho is None:
                pasos.append(f"→ Nodo {valor} es HOJA, se elimina directamente")
                return None, True
            elif nodo.izquierdo is None:
                pasos.append(f"→ Nodo {valor} solo tiene hijo DERECHO")
                return nodo.derecho, True
            elif nodo.derecho is None:
                pasos.append(f"→ Nodo {valor} solo tiene hijo IZQUIERDO")
                return nodo.izquierdo, True
            else:
                pasos.append(f"→ Nodo {valor} tiene DOS hijos")
                pasos.append(f"→ Buscando SUCESOR (mínimo del subárbol derecho)...")
                sucesor = self._encontrar_minimo(nodo.derecho)
                pasos.append(f"→ Sucesor encontrado: {sucesor.valor}")
                pasos.append(f"→ Reemplazando {valor} con {sucesor.valor}")
                nodo.valor = sucesor.valor
                nodo.derecho, _ = self._eliminar_sucesor_recursivo(nodo.derecho, sucesor.valor, pasos, info)
                return nodo, True
    
    def _encontrar_minimo(self, nodo):
        while nodo and nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo
    
    def _encontrar_maximo(self, nodo):
        while nodo and nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo
    
    def eliminar_arbol(self):
        self.raiz = None
    
    def mostrar_acostado(self):
        lineas = []
        self._mostrar_acostado_recursivo(self.raiz, 0, lineas)
        return lineas
    
    def _mostrar_acostado_recursivo(self, nodo, nivel, lineas):
        if nodo is not None:
            self._mostrar_acostado_recursivo(nodo.derecho, nivel + 1, lineas)
            lineas.append(("    " * nivel) + f"[{nodo.valor}]")
            self._mostrar_acostado_recursivo(nodo.izquierdo, nivel + 1, lineas)

# =========================
#  Vista/Controlador Tkinter
# =========================

class AplicacionArbol:
    def __init__(self, root):
        self.root = root
        self.root.title("🌳 Árbol Binario de Búsqueda - Visualizador Interactivo")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f4f8")
        
        self.arbol = ArbolBinario()
        
        # mapa de resaltado: id(nodo) -> estado
        # estados posibles: "normal", "path", "current", "found", "inserted"
        self.marcadores = {}

        # paleta de colores por estado (fill, outline)
        self.COLORES = {
            "normal":   ("#3b82f6", "#1e40af"),  # azul base
            "path":     ("#fde68a", "#f59e0b"),  # amarillo
            "current":  ("#fca5a5", "#b91c1c"),  # rojo
            "found":    ("#34d399", "#065f46"),  # verde
            "inserted": ("#93c5fd", "#1d4ed8"),  # azul claro
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        titulo_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(titulo_frame, text="🌳 Árbol Binario de Búsqueda - Visualizador Interactivo", 
                font=("Arial", 20, "bold"), bg="#ffffff", fg="#1e40af").pack(pady=10)
        tk.Label(titulo_frame, text="Aprende los conceptos de árboles binarios de forma visual", 
                font=("Arial", 11), bg="#ffffff", fg="#64748b").pack(pady=(0, 10))
        
        # Frame contenedor para panel y visualización
        contenedor = tk.Frame(main_frame, bg="#f0f4f8")
        contenedor.pack(fill=tk.BOTH, expand=True)
        
        # Panel de control (izquierda)
        panel_frame = tk.Frame(contenedor, bg="#ffffff", relief=tk.RAISED, borderwidth=2, width=300)
        panel_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        panel_frame.pack_propagate(False)
        
        tk.Label(panel_frame, text="Panel de Control", font=("Arial", 14, "bold"), 
                bg="#ffffff", fg="#1e40af").pack(pady=10)
        
        # Input
        tk.Label(panel_frame, text="Ingresa un valor:", font=("Arial", 10), 
                bg="#ffffff").pack(pady=(10, 5))
        self.valor_entry = tk.Entry(panel_frame, font=("Arial", 12), width=20, justify="center")
        self.valor_entry.pack(pady=5)
        self.valor_entry.bind('<Return>', lambda e: self.insertar())
        
        # Botones principales
        tk.Button(panel_frame, text="➕ Insertar", command=self.insertar, 
                 bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), 
                 width=20, cursor="hand2").pack(pady=5)
        
        tk.Button(panel_frame, text="🔍 Buscar", command=self.buscar, 
                 bg="#10b981", fg="white", font=("Arial", 10, "bold"), 
                 width=20, cursor="hand2").pack(pady=5)
        
        tk.Button(panel_frame, text="🗑️ Eliminar (Predecesor)", command=lambda: self.eliminar("predecesor"), 
                 bg="#f97316", fg="white", font=("Arial", 10, "bold"), 
                 width=20, cursor="hand2").pack(pady=5)
        
        tk.Button(panel_frame, text="🗑️ Eliminar (Sucesor)", command=lambda: self.eliminar("sucesor"), 
                 bg="#ea580c", fg="white", font=("Arial", 10, "bold"), 
                 width=20, cursor="hand2").pack(pady=5)
        
        # Separador
        tk.Frame(panel_frame, height=2, bg="#e2e8f0").pack(fill=tk.X, pady=10)
        
        tk.Label(panel_frame, text="Recorridos", font=("Arial", 11, "bold"), 
                bg="#ffffff", fg="#1e40af").pack(pady=5)
        
        tk.Button(panel_frame, text="PreOrden", command=lambda: self.recorrido("pre"), 
                 bg="#8b5cf6", fg="white", font=("Arial", 10), 
                 width=20, cursor="hand2").pack(pady=3)
        
        tk.Button(panel_frame, text="InOrden", command=lambda: self.recorrido("in"), 
                 bg="#8b5cf6", fg="white", font=("Arial", 10), 
                 width=20, cursor="hand2").pack(pady=3)
        
        tk.Button(panel_frame, text="PostOrden", command=lambda: self.recorrido("post"), 
                 bg="#8b5cf6", fg="white", font=("Arial", 10), 
                 width=20, cursor="hand2").pack(pady=3)
        
        tk.Button(panel_frame, text="Por Niveles", command=lambda: self.recorrido("niveles"), 
                 bg="#8b5cf6", fg="white", font=("Arial", 10), 
                 width=20, cursor="hand2").pack(pady=3)
        
        # Separador
        tk.Frame(panel_frame, height=2, bg="#e2e8f0").pack(fill=tk.X, pady=10)
        
        tk.Label(panel_frame, text="Análisis", font=("Arial", 11, "bold"), 
                bg="#ffffff", fg="#1e40af").pack(pady=5)
        
        tk.Button(panel_frame, text="📊 Ver Estadísticas", command=self.mostrar_estadisticas, 
                 bg="#06b6d4", fg="white", font=("Arial", 10, "bold"), 
                 width=20, cursor="hand2").pack(pady=5)
        
        tk.Button(panel_frame, text="🗑️ Eliminar Árbol", command=self.eliminar_arbol, 
                 bg="#dc2626", fg="white", font=("Arial", 10, "bold"), 
                 width=20, cursor="hand2").pack(pady=5)
        
        # Frame de visualización (derecha)
        visual_frame = tk.Frame(contenedor, bg="#f0f4f8")
        visual_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Canvas para el árbol gráfico + scrollbars
        canvas_frame = tk.Frame(visual_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        tk.Label(canvas_frame, text="Visualización Gráfica", font=("Arial", 12, "bold"), 
                 bg="#ffffff", fg="#1e40af").pack(pady=5)

        canvas_container = tk.Frame(canvas_frame, bg="#ffffff")
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_container, bg="#f8fafc", highlightthickness=0)
        hbar = tk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        vbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="ew")
        canvas_container.rowconfigure(0, weight=1)
        canvas_container.columnconfigure(0, weight=1)

        # arrastrar para pan (botón medio o derecho)
        self._drag_data = {"x": 0, "y": 0}
        self.canvas.bind("<ButtonPress-2>", self._start_pan)
        self.canvas.bind("<B2-Motion>", self._do_pan)
        self.canvas.bind("<ButtonPress-3>", self._start_pan)
        self.canvas.bind("<B3-Motion>", self._do_pan)

        # redibujar al cambiar tamaño
        self.canvas.bind("<Configure>", lambda e: self.actualizar_visualizacion())
        
        # Frame para árbol acostado y pasos
        info_frame = tk.Frame(visual_frame, bg="#f0f4f8")
        info_frame.pack(fill=tk.BOTH)
        
        # Árbol acostado
        acostado_frame = tk.Frame(info_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        acostado_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(acostado_frame, text="Árbol Acostado (Raíz a la izquierda)", 
                font=("Arial", 11, "bold"), bg="#ffffff", fg="#1e40af").pack(pady=5)
        
        self.acostado_text = scrolledtext.ScrolledText(acostado_frame, height=10, 
                                                       font=("Courier", 10), bg="#f8fafc")
        self.acostado_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pasos
        pasos_frame = tk.Frame(info_frame, bg="#ffffff", relief=tk.RAISED, borderwidth=2)
        pasos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(pasos_frame, text="Proceso Paso a Paso", 
                font=("Arial", 11, "bold"), bg="#ffffff", fg="#1e40af").pack(pady=5)
        
        self.pasos_text = scrolledtext.ScrolledText(pasos_frame, height=10, 
                                                    font=("Arial", 10), bg="#eff6ff")
        self.pasos_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.actualizar_visualizacion()
    
    # ======= Señal visual (parpadeo/halo) para un nodo =======
    def _halo_step(self, nodo, step, total_steps, halo_ids):
        """Un paso de la animación del halo (parpadeo)."""
        if nodo is None:
            return

        radio_base = 25
        visible = (step % 2 == 0)

        # limpiar halos anteriores de este ciclo
        for _id in halo_ids:
            self.canvas.delete(_id)
        halo_ids.clear()

        if visible:
            # dos anillos concéntricos
            r1 = radio_base + 8
            r2 = radio_base + 14
            x, y = nodo.x, nodo.y
            halo_ids.append(
                self.canvas.create_oval(x - r1, y - r1, x + r1, y + r1,
                                        outline="#22c55e", width=3)
            )
            halo_ids.append(
                self.canvas.create_oval(x - r2, y - r2, x + r2, y + r2,
                                        outline="#16a34a", width=2)
            )

        if step < total_steps:
            self.canvas.after(180, self._halo_step, nodo, step + 1, total_steps, halo_ids)
        else:
            for _id in halo_ids:
                self.canvas.delete(_id)

    def señalar_nodo(self, nodo, duracion_parpadeos=8):
        """Inicia una animación de halo/parpadeo alrededor del nodo."""
        if nodo is None:
            return
        halo_ids = []
        self._halo_step(nodo, 0, duracion_parpadeos, halo_ids)

    # ========== Control: Acciones ==========
    def insertar(self):
        try:
            valor = int(self.valor_entry.get())
            pasos, info = self.arbol.insertar(valor)
            self.mostrar_pasos(pasos)
            self.valor_entry.delete(0, tk.END)
            self.marcar(info)
            self.actualizar_visualizacion()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
    
    def buscar(self):
        try:
            valor = int(self.valor_entry.get())
            encontrado, pasos, info = self.arbol.buscar(valor)
            self.mostrar_pasos(pasos)
            self.marcar(info)
            self.actualizar_visualizacion()
            if encontrado and info.get("found") is not None:
                # pequeño delay para asegurar que el nodo ya se dibujó
                self.root.after(50, lambda: self.señalar_nodo(info["found"]))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
    
    def eliminar(self, tipo):
        try:
            valor = int(self.valor_entry.get())
            if tipo == "predecesor":
                pasos, info = self.arbol.eliminar_predecesor(valor)
            else:
                pasos, info = self.arbol.eliminar_sucesor(valor)
            self.mostrar_pasos(pasos)
            self.valor_entry.delete(0, tk.END)
            self.marcar(info)
            self.actualizar_visualizacion()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
    
    def recorrido(self, tipo):
        # los recorridos no resaltan camino; solo muestran el listado
        self.marcadores.clear()
        if tipo == "pre":
            resultado = self.arbol.pre_orden()
            texto = f"PreOrden (Raíz-Izq-Der): {' → '.join(map(str, resultado))}"
        elif tipo == "in":
            resultado = self.arbol.in_orden()
            texto = f"InOrden (Izq-Raíz-Der): {' → '.join(map(str, resultado))}"
        elif tipo == "post":
            resultado = self.arbol.post_orden()
            texto = f"PostOrden (Izq-Der-Raíz): {' → '.join(map(str, resultado))}"
        else:
            resultado = self.arbol.por_niveles()
            texto = f"Por Niveles: {' → '.join(map(str, resultado))}"
        
        self.mostrar_pasos([texto])
        self.actualizar_visualizacion()
    
    def mostrar_estadisticas(self):
        pasos = [
            f"Altura del árbol: {self.arbol.altura()}",
            f"Cantidad de hojas: {self.arbol.contar_hojas()}",
            f"Cantidad de nodos: {self.arbol.contar_nodos()}",
            f"¿Es completo?: {'Sí' if self.arbol.es_completo() else 'No'}",
            f"¿Es lleno?: {'Sí' if self.arbol.es_lleno() else 'No'}"
        ]
        self.mostrar_pasos(pasos)
    
    def eliminar_arbol(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar todo el árbol?")
        if respuesta:
            self.arbol.eliminar_arbol()
            self.marcadores.clear()
            self.mostrar_pasos(["Árbol eliminado completamente"])
            self.actualizar_visualizacion()
    
    # ========== Utilidades de vista ==========
    def marcar(self, info):
        """Convierte el 'info' devuelto por las operaciones en colores en el canvas."""
        self.marcadores.clear()
        for n in info.get("path", []):
            if n is not None:
                self.marcadores[id(n)] = "path"
        if info.get("current") is not None:
            self.marcadores[id(info["current"])] = "current"
        if info.get("found") is not None:
            self.marcadores[id(info["found"])] = "found"
        if info.get("inserted") is not None:
            self.marcadores[id(info["inserted"])] = "inserted"
    
    def mostrar_pasos(self, pasos):
        self.pasos_text.delete(1.0, tk.END)
        for i, paso in enumerate(pasos, 1):
            self.pasos_text.insert(tk.END, f"{i}. {paso}\n")
    
    def actualizar_visualizacion(self):
        self.canvas.delete("all")
        if not self.arbol.es_vacio():
            self.dibujar_arbol()
        else:
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            self.canvas.create_text(w//2, h//2, text="Árbol vacío\nInserta valores para comenzar", 
                                   font=("Arial", 14), fill="#94a3b8")
        
        # Actualizar árbol acostado
        self.acostado_text.delete(1.0, tk.END)
        if not self.arbol.es_vacio():
            lineas = self.arbol.mostrar_acostado()
            for linea in lineas:
                self.acostado_text.insert(tk.END, linea + "\n")
        else:
            self.acostado_text.insert(tk.END, "Árbol vacío")
    
    # ------ Layout que siempre cabe horizontalmente ------
    def _asignar_posiciones_inorder(self):
        """Asigna x por índice inorder y y por nivel (siempre cabe horizontalmente)."""
        if self.arbol.raiz is None:
            return

        # 1) niveles por BFS
        niveles = {}
        q = deque([(self.arbol.raiz, 0)])
        max_nivel = 0
        while q:
            n, lvl = q.popleft()
            if n is None: 
                continue
            niveles[n] = lvl
            max_nivel = max(max_nivel, lvl)
            if n.izquierdo: q.append((n.izquierdo, lvl+1))
            if n.derecho:  q.append((n.derecho,  lvl+1))

        # 2) inorder para asignar índice
        orden = []
        def inorder(n):
            if n is None: return
            inorder(n.izquierdo)
            orden.append(n)
            inorder(n.derecho)
        inorder(self.arbol.raiz)

        # 3) espaciar según ancho visible
        w = max(self.canvas.winfo_width(), 400)
        margen_x = 40
        margen_y = 40
        n = max(len(orden), 1)
        gap_x = max((w - 2*margen_x) / n, 50)  # mínimo 50 px entre columnas
        gap_y = 90  # distancia vertical por nivel

        for i, nodo in enumerate(orden, start=1):
            x = margen_x + i * gap_x
            y = margen_y + niveles[nodo] * gap_y
            nodo.x, nodo.y = int(x), int(y)

    def dibujar_arbol(self):
        if self.arbol.raiz is None:
            return

        # asignar posiciones ajustadas al ancho
        self._asignar_posiciones_inorder()

        # Dibujar líneas primero
        self.dibujar_lineas(self.arbol.raiz)

        # Dibujar nodos
        self.dibujar_nodos(self.arbol.raiz)

        # Ajustar región de scroll a todo lo dibujado
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def dibujar_lineas(self, nodo):
        if nodo is None:
            return
        if nodo.izquierdo:
            self.canvas.create_line(nodo.x, nodo.y, nodo.izquierdo.x, nodo.izquierdo.y, 
                                   fill="#64748b", width=2)
            self.dibujar_lineas(nodo.izquierdo)
        if nodo.derecho:
            self.canvas.create_line(nodo.x, nodo.y, nodo.derecho.x, nodo.derecho.y, 
                                   fill="#64748b", width=2)
            self.dibujar_lineas(nodo.derecho)
    
    def dibujar_nodos(self, nodo):
        if nodo is None:
            return
        radio = 25
        estado = self.marcadores.get(id(nodo), "normal")
        fill, outline = self.COLORES.get(estado, self.COLORES["normal"])
        self.canvas.create_oval(nodo.x - radio, nodo.y - radio, 
                                nodo.x + radio, nodo.y + radio, 
                                fill=fill, outline=outline, width=2)
        self.canvas.create_text(nodo.x, nodo.y, text=str(nodo.valor), 
                                font=("Arial", 12, "bold"), fill="white")
        self.dibujar_nodos(nodo.izquierdo)
        self.dibujar_nodos(nodo.derecho)

    # ------ Pan (arrastrar) en el canvas ------
    def _start_pan(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _do_pan(self, event):
        dx = self._drag_data["x"] - event.x
        dy = self._drag_data["y"] - event.y
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.canvas.xview_scroll(int(dx), "units")
        self.canvas.yview_scroll(int(dy), "units")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionArbol(root)
    root.mainloop()
