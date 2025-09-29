import tkinter as tk
from tkinter import messagebox, simpledialog
import time

class PilaVisual:
    def __init__(self, canvas, nombre, x_offset, color_tema):
        self.items = []
        self.canvas = canvas
        self.nombre = nombre
        self.x_offset = x_offset
        self.color_tema = color_tema
        self.base_y = 400
        self.alto = 50
        self.ancho = 120
        self.max_elementos = 7
        self.animando = False
        self.seleccionada = False

    def dibujar(self, extra=None):
        x_base = self.x_offset

        # Fondo de la pila
        borde_color = "#ff006e" if self.seleccionada else "#d4a5d9"
        borde_width = 4 if self.seleccionada else 2
        self.canvas.create_rectangle(x_base - 10, 50, x_base + self.ancho + 10, self.base_y + 30,
                                     outline=borde_color, width=borde_width, dash=(5, 5))

        # Nombre de la pila
        self.canvas.create_text(x_base + self.ancho//2, 30,
                               text=self.nombre,
                               font=("Comic Sans MS", 12, "bold"),
                               fill=borde_color)

        # Contador
        self.canvas.create_text(x_base + self.ancho//2, self.base_y + 50,
                               text=f"{len(self.items)}/{self.max_elementos}",
                               font=("Arial", 10, "bold"),
                               fill=self.color_tema["texto"])

        # Línea de base
        self.canvas.create_line(x_base, self.base_y + 20,
                               x_base + self.ancho, self.base_y + 20,
                               fill=self.color_tema["base"], width=3)

        # Dibujar elementos
        for i, elemento in enumerate(self.items):
            x1, y1 = x_base, self.base_y - (i+1)*self.alto
            x2, y2 = x1 + self.ancho, y1 + self.alto

            self.rounded_rect(x1, y1, x2, y2, 15,
                            fill=self.color_tema["fill"],
                            outline=self.color_tema["outline"], width=2)

            # Sombra interior
            self.rounded_rect(x1+3, y1+3, x2-3, y2-3, 12,
                            fill="", outline=self.color_tema["sombra"], width=1)

            # Texto
            emojis = ['⭐','💖','🍭','🌸','🎈','🦄','✨']
            texto = str(elemento)[:12]
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                    text=f"{texto} {emojis[i % len(emojis)]}",
                                    font=("Comic Sans MS", 10, "bold"), fill="white")

        # Indicador de CIMA
        if self.items:
            cima_y = self.base_y - len(self.items)*self.alto + self.alto//2
            self.canvas.create_text(x_base + self.ancho + 40, cima_y,
                                   text="⬅", fill="#ff006e",
                                   font=("Arial", 16, "bold"))

        # Mensaje temporal
        if extra:
            self.canvas.create_text(x_base + self.ancho//2, 60,
                                   text=extra, font=("Arial", 14, "bold"),
                                   fill="#ff006e", tags=f"msg_{self.nombre}")

    def rounded_rect(self, x1, y1, x2, y2, r=15, **kwargs):
        points = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
                  x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
                  x1, y2, x1, y2-r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def animar_apilar(self, elemento):
        if self.animando or not elemento or not elemento.strip():
            return False

        if len(self.items) >= self.max_elementos:
            return False

        self.animando = True
        elemento = elemento.strip()[:15]

        pasos = 10
        for paso in range(pasos):
            progreso = paso / pasos
            desplazamiento = int(60 * (1 - progreso))

            x1 = self.x_offset
            y1 = self.base_y - (len(self.items)+1)*self.alto - desplazamiento
            x2, y2 = x1 + self.ancho, y1 + self.alto

            self.rounded_rect(x1, y1, x2, y2, 15,
                            fill="#90e0ef", outline="#0077b6", width=2)
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                    text=elemento, font=("Comic Sans MS", 10, "bold"),
                                    fill="white")
            self.canvas.update()
            time.sleep(0.03)

        self.items.append(elemento)
        self.animando = False
        return True

    def animar_desapilar(self):
        if self.animando or not self.items:
            return None

        self.animando = True
        elemento = self.items.pop()

        pasos = 8
        for paso in range(pasos):
            desplazamiento = int(paso * 8)

            x1 = self.x_offset
            y1 = self.base_y - (len(self.items)+1)*self.alto - desplazamiento
            x2, y2 = x1 + self.ancho, y1 + self.alto

            self.rounded_rect(x1, y1, x2, y2, 15,
                            fill="#ff595e", outline="#6a040f", width=2)
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2,
                                    text=elemento, font=("Comic Sans MS", 10, "bold"),
                                    fill="white")
            self.canvas.update()
            time.sleep(0.04)

        self.animando = False
        return elemento


class GestorMultiPilas:
    def __init__(self, root):
        self.root = root
        self.pilas = {}
        self.pila_seleccionada = None
        self.animando_global = False

        # Colores para diferentes pilas
        self.colores = [
            {"fill": "#cdb4db", "outline": "#5a189a", "sombra": "#b084cc", "base": "#d4a5d9", "texto": "#5a189a"},
            {"fill": "#a8dadc", "outline": "#1d3557", "sombra": "#8ac4c6", "base": "#457b9d", "texto": "#1d3557"},
            {"fill": "#ffb3c6", "outline": "#c9184a", "sombra": "#ff97b3", "base": "#ff4d6d", "texto": "#c9184a"},
            {"fill": "#b8e0d2", "outline": "#2a9d8f", "sombra": "#9fccbe", "base": "#06d6a0", "texto": "#2a9d8f"},
            {"fill": "#ffd6a5", "outline": "#e85d04", "sombra": "#ffbd7f", "base": "#f77f00", "texto": "#e85d04"},
        ]

        self.setup_ui()
        self.crear_pila_inicial()

    def setup_ui(self):
        # Frame superior
        frame_superior = tk.Frame(self.root, bg="#fdf6f9", pady=10)
        frame_superior.pack(fill=tk.X)

        tk.Label(frame_superior, text="🎀 Gestor de Múltiples Pilas 🎀",
                font=("Comic Sans MS", 16, "bold"), fg="#5a189a", bg="#fdf6f9").pack()

        # Canvas principal
        self.canvas = tk.Canvas(self.root, width=900, height=520,
                               bg="#fdf6f9", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Frame de controles
        frame_controles = tk.Frame(self.root, bg="#fdf6f9")
        frame_controles.pack(pady=5)

        # Selección de pila
        tk.Label(frame_controles, text="Pila activa:",
                font=("Comic Sans MS", 10, "bold"), fg="#5a189a", bg="#fdf6f9").grid(row=0, column=0, padx=5)

        self.var_pila = tk.StringVar()
        self.combo_pilas = tk.OptionMenu(frame_controles, self.var_pila, "",
                                         command=self.seleccionar_pila_combo)
        self.combo_pilas.config(font=("Comic Sans MS", 10), bg="white", width=12)
        self.combo_pilas.grid(row=0, column=1, padx=5)

        # Entrada de datos
        tk.Label(frame_controles, text="Elemento:",
                font=("Comic Sans MS", 10, "bold"), fg="#5a189a", bg="#fdf6f9").grid(row=0, column=2, padx=5)

        self.entry = tk.Entry(frame_controles, font=("Comic Sans MS", 11), width=15)
        self.entry.grid(row=0, column=3, padx=5)
        self.entry.focus()

        # Botones de operaciones
        frame_ops = tk.Frame(self.root, bg="#fdf6f9")
        frame_ops.pack(pady=5)

        tk.Button(frame_ops, text="📥 Apilar", font=("Comic Sans MS", 10, "bold"),
                 bg="#b5e48c", fg="white", command=self.apilar, width=12).grid(row=0, column=0, padx=3)

        tk.Button(frame_ops, text="📤 Desapilar", font=("Comic Sans MS", 10, "bold"),
                 bg="#ffd166", fg="white", command=self.desapilar, width=12).grid(row=0, column=1, padx=3)

        tk.Button(frame_ops, text="👁️ Ver Cima", font=("Comic Sans MS", 10, "bold"),
                 bg="#a0c4ff", fg="white", command=self.ver_cima, width=12).grid(row=0, column=2, padx=3)

        tk.Button(frame_ops, text="🗑️ Vaciar", font=("Comic Sans MS", 10, "bold"),
                 bg="#ffadad", fg="white", command=self.vaciar, width=12).grid(row=0, column=3, padx=3)

        # Botones de gestión de pilas
        frame_gestion = tk.Frame(self.root, bg="#fdf6f9")
        frame_gestion.pack(pady=5)

        tk.Button(frame_gestion, text="➕ Nueva Pila", font=("Comic Sans MS", 10, "bold"),
                 bg="#90e0ef", fg="white", command=self.crear_nueva_pila, width=15).grid(row=0, column=0, padx=3)

        tk.Button(frame_gestion, text="🗑️ Eliminar Pila", font=("Comic Sans MS", 10, "bold"),
                 bg="#ff6b9d", fg="white", command=self.eliminar_pila, width=15).grid(row=0, column=1, padx=3)

        tk.Button(frame_gestion, text="🔄 Mover a otra Pila", font=("Comic Sans MS", 10, "bold"),
                 bg="#c77dff", fg="white", command=self.mover_elemento, width=15).grid(row=0, column=2, padx=3)

        # Info
        self.info_label = tk.Label(self.root, text="",
                                   font=("Comic Sans MS", 10, "italic"),
                                   fg="#7209b7", bg="#fdf6f9")
        self.info_label.pack(pady=5)

        # Atajos
        self.root.bind("<Return>", lambda e: self.apilar())
        self.root.bind("<Delete>", lambda e: self.desapilar())
        self.root.bind("<Control-n>", lambda e: self.crear_nueva_pila())

    def crear_pila_inicial(self):
        self.crear_pila("Pila 1")

    def crear_pila(self, nombre):
        if nombre in self.pilas:
            return

        if len(self.pilas) >= 5:
            messagebox.showwarning("Límite alcanzado", "Máximo 5 pilas permitidas")
            return

        idx = len(self.pilas)
        x_offset = 50 + (idx * 180)
        color = self.colores[idx % len(self.colores)]

        pila = PilaVisual(self.canvas, nombre, x_offset, color)
        self.pilas[nombre] = pila

        if self.pila_seleccionada is None:
            self.pila_seleccionada = nombre
            pila.seleccionada = True

        self.actualizar_combo()
        self.redibujar_todo()
        self.info_label.config(text=f"✅ Pila '{nombre}' creada")

    def crear_nueva_pila(self):
        nombre = simpledialog.askstring("Nueva Pila",
                                       f"Nombre de la pila (hay {len(self.pilas)}):",
                                       parent=self.root)
        if nombre:
            nombre = nombre.strip()[:15]
            if nombre in self.pilas:
                messagebox.showwarning("Nombre duplicado", "Ya existe una pila con ese nombre")
            else:
                self.crear_pila(nombre)

    def eliminar_pila(self):
        if not self.pila_seleccionada:
            messagebox.showinfo("Sin selección", "Selecciona una pila primero")
            return

        if len(self.pilas) == 1:
            messagebox.showwarning("No se puede", "Debe haber al menos una pila")
            return

        pila = self.pilas[self.pila_seleccionada]
        if pila.items:
            respuesta = messagebox.askyesno("Confirmar",
                                          f"La pila '{self.pila_seleccionada}' tiene {len(pila.items)} elementos.\n¿Eliminar de todos modos?")
            if not respuesta:
                return

        del self.pilas[self.pila_seleccionada]
        self.pila_seleccionada = list(self.pilas.keys())[0] if self.pilas else None

        if self.pila_seleccionada:
            self.pilas[self.pila_seleccionada].seleccionada = True

        self.reorganizar_pilas()
        self.actualizar_combo()
        self.redibujar_todo()

    def reorganizar_pilas(self):
        for idx, (nombre, pila) in enumerate(self.pilas.items()):
            pila.x_offset = 50 + (idx * 180)

    def seleccionar_pila_combo(self, nombre):
        if nombre in self.pilas:
            for n, p in self.pilas.items():
                p.seleccionada = (n == nombre)
            self.pila_seleccionada = nombre
            self.redibujar_todo()
            self.info_label.config(text=f"📍 Pila activa: '{nombre}'")

    def actualizar_combo(self):
        menu = self.combo_pilas['menu']
        menu.delete(0, 'end')

        for nombre in self.pilas.keys():
            menu.add_command(label=nombre,
                           command=lambda n=nombre: self.var_pila.set(n) or self.seleccionar_pila_combo(n))

        if self.pila_seleccionada:
            self.var_pila.set(self.pila_seleccionada)

    def redibujar_todo(self, extra=None):
        self.canvas.delete("all")
        for pila in self.pilas.values():
            pila.dibujar(extra)

    def apilar(self):
        if not self.pila_seleccionada or self.animando_global:
            return

        elemento = self.entry.get().strip()
        if not elemento:
            messagebox.showwarning("Campo vacío", "Escribe algo para apilar")
            return

        pila = self.pilas[self.pila_seleccionada]
        if len(pila.items) >= pila.max_elementos:
            messagebox.showwarning("Pila llena",
                                  f"La pila '{self.pila_seleccionada}' está llena")
            return

        self.animando_global = True
        self.redibujar_todo()

        if pila.animar_apilar(elemento):
            self.redibujar_todo("PUSH!")
            self.info_label.config(text=f"✅ '{elemento}' apilado en '{self.pila_seleccionada}'")
            self.entry.delete(0, tk.END)
            self.canvas.after(300, lambda: self.redibujar_todo())

        self.animando_global = False

    def desapilar(self):
        if not self.pila_seleccionada or self.animando_global:
            return

        pila = self.pilas[self.pila_seleccionada]
        if not pila.items:
            messagebox.showinfo("Pila vacía", f"La pila '{self.pila_seleccionada}' está vacía")
            return

        self.animando_global = True
        self.redibujar_todo()

        elemento = pila.animar_desapilar()
        if elemento:
            self.redibujar_todo("POP!")
            self.info_label.config(text=f"✅ '{elemento}' desapilado de '{self.pila_seleccionada}'")
            self.canvas.after(300, lambda: self.redibujar_todo())

        self.animando_global = False

    def ver_cima(self):
        if not self.pila_seleccionada:
            return

        pila = self.pilas[self.pila_seleccionada]
        if not pila.items:
            messagebox.showinfo("Pila vacía", f"La pila '{self.pila_seleccionada}' está vacía")
            return

        cima = pila.items[-1]
        self.info_label.config(text=f"👁️ peek() de '{self.pila_seleccionada}': '{cima}'")
        messagebox.showinfo("Método peek()", f"Pila: {self.pila_seleccionada}\n\nMétodo: peek()\nRetorna: '{cima}'\n\n(Consulta la cima sin desapilar)")

    def vaciar(self):
        if not self.pila_seleccionada:
            return

        pila = self.pilas[self.pila_seleccionada]
        if not pila.items:
            messagebox.showinfo("Pila vacía", f"La pila '{self.pila_seleccionada}' ya está vacía")
            return

        respuesta = messagebox.askyesno("Confirmar",
                                       f"¿Vaciar la pila '{self.pila_seleccionada}'?\n({len(pila.items)} elementos)")
        if not respuesta:
            return

        cantidad = len(pila.items)
        while pila.items:
            self.redibujar_todo()
            pila.animar_desapilar()
            time.sleep(0.1)

        self.redibujar_todo()
        self.info_label.config(text=f"🗑️ Pila '{self.pila_seleccionada}' vaciada ({cantidad} elementos)")

    def mover_elemento(self):
        if not self.pila_seleccionada:
            return

        pila_origen = self.pilas[self.pila_seleccionada]
        if not pila_origen.items:
            messagebox.showinfo("Pila vacía", "No hay elementos para mover")
            return

        otras_pilas = [n for n in self.pilas.keys() if n != self.pila_seleccionada]
        if not otras_pilas:
            messagebox.showinfo("Sin destino", "Necesitas crear otra pila primero")
            return

        destino = simpledialog.askstring("Mover elemento",
                                        f"¿A qué pila mover?\nDisponibles: {', '.join(otras_pilas)}",
                                        parent=self.root)

        if destino and destino in self.pilas:
            pila_destino = self.pilas[destino]
            if len(pila_destino.items) >= pila_destino.max_elementos:
                messagebox.showwarning("Pila llena", f"La pila '{destino}' está llena")
                return

            # Desapilar de origen
            self.redibujar_todo()
            elemento = pila_origen.animar_desapilar()

            # Apilar en destino
            time.sleep(0.2)
            self.redibujar_todo()
            pila_destino.animar_apilar(elemento)

            self.redibujar_todo()
            self.info_label.config(text=f"🔄 '{elemento}' movido de '{self.pila_seleccionada}' a '{destino}'")


def main():
    root = tk.Tk()
    root.title("🎀 Gestor de Múltiples Pilas 🎀")
    root.configure(bg="#fdf6f9")
    root.resizable(False, False)

    app = GestorMultiPilas(root)
    root.mainloop()

if __name__ == "__main__":
    main()