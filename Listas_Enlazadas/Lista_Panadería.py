# panaderia_tk.py
# Panadería: registro de postres (arreglo ordenado) e ingredientes (lista enlazada) con Tkinter.
# Sin persistencia; todo vive en memoria mientras la app esté abierta.

from bisect import bisect_left
import tkinter as tk
from tkinter import ttk, messagebox

# ------------------- ESTRUCTURAS DE DATOS -------------------
def norm(s: str) -> str:
    return " ".join(s.strip().split())

class NodoIngrediente:
    def __init__(self, nombre: str, nxt=None):
        self.nombre = nombre
        self.next = nxt

class ListaIngredientes:
    def __init__(self):
        self.head = None

    def contiene(self, nombre: str) -> bool:
        p = self.head
        while p:
            if p.nombre.lower() == nombre.lower():
                return True
            p = p.next
        return False

    def insertar_alfabetico(self, nombre: str) -> bool:
        nombre = norm(nombre)
        if not nombre or self.contiene(nombre):
            return False
        if self.head is None or self.head.nombre.lower() > nombre.lower():
            self.head = NodoIngrediente(nombre, self.head)
            return True
        prev, cur = None, self.head  # prev = nodo anterior, cur = nodo actual
        while cur and cur.nombre.lower() < nombre.lower():
            prev, cur = cur, cur.next
        prev.next = NodoIngrediente(nombre, cur)
        return True

    def eliminar(self, nombre: str) -> bool:
        nombre = norm(nombre)
        if not self.head:
            return False
        if self.head.nombre.lower() == nombre.lower():
            self.head = self.head.next
            return True
        prev, cur = self.head, self.head.next
        while cur:
            if cur.nombre.lower() == nombre.lower():
                prev.next = cur.next
                return True
            prev, cur = cur, cur.next
        return False

    def a_lista(self):
        out, p = [], self.head
        while p:
            out.append(p.nombre)
            p = p.next
        return out

    # ---------- Depurar duplicados de ingredientes ----------
    def depurar_duplicados(self) -> int:
        """Elimina ingredientes repetidos (case-insensitive). Devuelve cuántos quitó."""
        vistos = set()
        prev, cur = None, self.head
        eliminados = 0
        while cur:
            k = cur.nombre.lower()
            if k in vistos:
                prev.next = cur.next
                cur = prev.next
                eliminados += 1
            else:
                vistos.add(k)
                prev, cur = cur, cur.next
        return eliminados

class Postre:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.ingredientes = ListaIngredientes()

class LibroDePostres:
    """Arreglo ordenado alfabéticamente por nombre (case-insensitive)."""
    def __init__(self):
        self.postres: list[Postre] = []

    def _idx(self, nombre: str) -> int:
        nombres = [p.nombre.lower() for p in self.postres]
        return bisect_left(nombres, nombre.lower())

    def _buscar(self, nombre: str):
        i = self._idx(nombre)
        if 0 <= i < len(self.postres) and self.postres[i].nombre.lower() == nombre.lower():
            return i, self.postres[i]
        return i, None

    def ingredientes_de(self, nombre_postre: str) -> list[str]:
        _, p = self._buscar(nombre_postre)
        if not p:
            raise KeyError(f"El postre '{nombre_postre}' no existe.")
        return p.ingredientes.a_lista()

    def agregar_ingredientes(self, nombre_postre: str, nuevos: list[str]):
        _, p = self._buscar(nombre_postre)
        if not p:
            raise KeyError(f"El postre '{nombre_postre}' no existe.")
        insertados, omitidos = [], []
        for ing in nuevos:
            ok = p.ingredientes.insertar_alfabetico(ing)
            (insertados if ok else omitidos).append(norm(ing))
        return insertados, omitidos

    def eliminar_ingrediente(self, nombre_postre: str, ingrediente: str):
        _, p = self._buscar(nombre_postre)
        if not p:
            raise KeyError(f"El postre '{nombre_postre}' no existe.")
        if not p.ingredientes.eliminar(ingrediente):
            raise ValueError(f"'{ingrediente}' no está en '{nombre_postre}'.")

    def alta_postre(self, nombre_postre: str, ingredientes: list[str]):
        nombre_postre = norm(nombre_postre)
        if not nombre_postre:
            raise ValueError("Nombre de postre vacío.")
        i, existe = self._buscar(nombre_postre)
        if existe:
            raise ValueError(f"El postre '{nombre_postre}' ya existe.")
        nuevo = Postre(nombre_postre)
        for ing in ingredientes:
            nuevo.ingredientes.insertar_alfabetico(ing)
        self.postres.insert(i, nuevo)

    def baja_postre(self, nombre_postre: str):
        i, existe = self._buscar(nombre_postre)
        if not existe:
            raise KeyError(f"El postre '{nombre_postre}' no existe.")
        self.postres.pop(i)

    def listar(self) -> list[str]:
        return [p.nombre for p in self.postres]

    # ---------- Depurar duplicados de postres ----------
    def depurar_duplicados_postres(self) -> dict:
        """Elimina postres repetidos por nombre y limpia ingredientes duplicados."""
        self.postres.sort(key=lambda p: p.nombre.lower())
        vistos = {}
        i = 0
        postres_eliminados = []
        ingredientes_eliminados_total = 0

        while i < len(self.postres):
            p = self.postres[i]
            p.nombre = norm(p.nombre)
            k = p.nombre.lower()
            if k in vistos:
                base = vistos[k]
                q = p.ingredientes.head
                while q:
                    base.ingredientes.insertar_alfabetico(q.nombre)
                    q = q.next
                postres_eliminados.append(p.nombre)
                self.postres.pop(i)
            else:
                vistos[k] = p
                ingredientes_eliminados_total += p.ingredientes.depurar_duplicados()
                i += 1

        return {
            "postres_quedaron": [p.nombre for p in self.postres],
            "postres_eliminados": postres_eliminados,
            "ingredientes_eliminados_total": ingredientes_eliminados_total,
        }

# ------------------- INTERFAZ TKINTER -------------------
class AppPanaderiaTk:
    def __init__(self, root):
        self.root = root
        self.root.title("Panadería — Registro de Postres e Ingredientes")
        self.libro = LibroDePostres()

        # NUEVO: estado del postre mostrado en la derecha
        self.postre_actual = None

        self._build_ui()
        self._seed_demo()

        # Depurar duplicados automáticamente al iniciar
        self.libro.depurar_duplicados_postres()
        self.refresh_postres()

    # ---------- UI ----------
    def _build_ui(self):
        self.root.geometry("900x520")
        self.root.minsize(780, 480)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        # Panel Postres (izquierda)
        left = ttk.Frame(self.root, padding=10)
        left.grid(row=0, column=0, sticky="nsew")
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        ttk.Label(left, text="Postres (orden alfabético)").grid(row=0, column=0, sticky="w")
        self.lst_postres = tk.Listbox(left, activestyle="dotbox")
        sb1 = ttk.Scrollbar(left, orient="vertical", command=self.lst_postres.yview)
        self.lst_postres.configure(yscrollcommand=sb1.set)
        self.lst_postres.grid(row=1, column=0, sticky="nsew")
        sb1.grid(row=1, column=1, sticky="ns")
        self.lst_postres.bind("<<ListboxSelect>>", self.on_select_postre)

        # Controles de alta/baja postre
        frm_postre = ttk.LabelFrame(left, text="Gestión de postres", padding=10)
        frm_postre.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,0))
        frm_postre.columnconfigure(1, weight=1)

        ttk.Label(frm_postre, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.ent_postre = ttk.Entry(frm_postre)
        self.ent_postre.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        ttk.Label(frm_postre, text="Ingredientes iniciales (coma):").grid(row=1, column=0, sticky="e", padx=5, pady=4)
        self.ent_ing_ini = ttk.Entry(frm_postre)
        self.ent_ing_ini.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        btn_alta = ttk.Button(frm_postre, text="Dar de ALTA", command=self.ui_alta_postre)
        btn_baja = ttk.Button(frm_postre, text="Dar de BAJA", command=self.ui_baja_postre)
        btn_alta.grid(row=2, column=0, padx=5, pady=6, sticky="ew")
        btn_baja.grid(row=2, column=1, padx=5, pady=6, sticky="ew")

        # Panel Ingredientes (derecha)
        right = ttk.Frame(self.root, padding=10)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        self.lbl_postre_sel = ttk.Label(right, text="Ingredientes de: (selecciona un postre)")
        self.lbl_postre_sel.grid(row=0, column=0, sticky="w")

        self.lst_ingredientes = tk.Listbox(right, activestyle="dotbox")
        sb2 = ttk.Scrollbar(right, orient="vertical", command=self.lst_ingredientes.yview)
        self.lst_ingredientes.configure(yscrollcommand=sb2.set)
        self.lst_ingredientes.grid(row=1, column=0, sticky="nsew")
        sb2.grid(row=1, column=1, sticky="ns")

        # Controles ingredientes
        frm_ing = ttk.LabelFrame(right, text="Gestión de ingredientes", padding=10)
        frm_ing.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,0))
        frm_ing.columnconfigure(1, weight=1)

        ttk.Label(frm_ing, text="Agregar (coma):").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.ent_ing = ttk.Entry(frm_ing)
        self.ent_ing.grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        btn_add_ing = ttk.Button(frm_ing, text="Agregar", command=self.ui_agregar_ingredientes)
        btn_del_ing = ttk.Button(frm_ing, text="Eliminar seleccionado", command=self.ui_eliminar_ingrediente)
        btn_add_ing.grid(row=1, column=0, padx=5, pady=6, sticky="ew")
        btn_del_ing.grid(row=1, column=1, padx=5, pady=6, sticky="ew")

        # Barra inferior (búsqueda rápida)
        bottom = ttk.Frame(self.root, padding=(10,0,10,10))
        bottom.grid(row=1, column=0, columnspan=2, sticky="ew")
        bottom.columnconfigure(2, weight=1)

        ttk.Label(bottom, text="Buscar por prefijo:").grid(row=0, column=0, padx=5)
        self.ent_busca = ttk.Entry(bottom)
        self.ent_busca.grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(bottom, text="Buscar", command=self.ui_buscar_prefijo).grid(row=0, column=2, padx=5, sticky="w")
        ttk.Button(bottom, text="Limpiar búsqueda", command=self.refresh_postres).grid(row=0, column=3, padx=5)
        ttk.Button(bottom, text="Depurar duplicados", command=self.ui_depurar).grid(row=0, column=4, padx=5)

    # ---------- Datos demo opcionales ----------
    def _seed_demo(self):
        try:
            self.libro.alta_postre("Arroz con leche", ["Leche", "Arroz", "Canela", "Azúcar"])
            self.libro.alta_postre("Brownie", ["Harina", "Cacao", "Huevo", "Mantequilla", "Azúcar"])
            self.libro.alta_postre("Carlota", ["Galleta María", "Leche condensada", "Limón"])
            # Duplicado para probar depuración:
            self.libro.alta_postre("brownie", ["Azúcar", "Cacao"])
        except Exception:
            pass
        self.refresh_postres()

    # ---------- Helpers ----------
    def refresh_postres(self, filtro=None):
        self.lst_postres.delete(0, tk.END)
        nombres = self.libro.listar() if not filtro else [
            n for n in self.libro.listar() if n.lower().startswith(filtro.lower())
        ]
        for n in nombres:
            self.lst_postres.insert(tk.END, n)
        self.lst_ingredientes.delete(0, tk.END)
        self.lbl_postre_sel.config(text="Ingredientes de: (selecciona un postre)")
        self.postre_actual = None  # <<< limpiar estado

    def refresh_ingredientes(self, nombre_postre):
        self.lst_ingredientes.delete(0, tk.END)
        try:
            ings = self.libro.ingredientes_de(nombre_postre)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        for ing in ings:
            self.lst_ingredientes.insert(tk.END, ing)
        self.lbl_postre_sel.config(text=f"Ingredientes de: {nombre_postre}")
        self.postre_actual = nombre_postre  # <<< recordar postre mostrado

    def get_postre_seleccionado(self):
        sel = self.lst_postres.curselection()
        if sel:
            return self.lst_postres.get(sel[0])
        return self.postre_actual  # <<< fallback si se perdió la selección

    # ---------- Callbacks ----------
    def on_select_postre(self, _event=None):
        nombre = self.get_postre_seleccionado()
        if nombre:
            self.refresh_ingredientes(nombre)

    def ui_alta_postre(self):
        nombre = norm(self.ent_postre.get())
        ing_line = self.ent_ing_ini.get().strip()
        ingredientes = [norm(x) for x in ing_line.split(",") if norm(x)]
        try:
            self.libro.alta_postre(nombre, ingredientes)
            self.libro.depurar_duplicados_postres()
            self.refresh_postres()
            self.ent_postre.delete(0, tk.END)
            self.ent_ing_ini.delete(0, tk.END)
            messagebox.showinfo("Éxito", f"Postre '{nombre}' dado de alta.")
        except Exception as e:
            messagebox.showerror("No se pudo dar de alta", str(e))

    def ui_baja_postre(self):
        nombre = self.get_postre_seleccionado() or norm(self.ent_postre.get())
        if not nombre:
            messagebox.showwarning("Atención", "Selecciona un postre o escribe su nombre.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Dar de BAJA el postre '{nombre}'?"):
            return
        try:
            self.libro.baja_postre(nombre)
            self.refresh_postres()
            messagebox.showinfo("Éxito", f"Postre '{nombre}' eliminado.")
        except Exception as e:
            messagebox.showerror("No se pudo eliminar", str(e))

    def ui_agregar_ingredientes(self):
        nombre = self.get_postre_seleccionado()
        if not nombre:
            messagebox.showwarning("Atención", "Selecciona un postre en la lista de la izquierda.")
            return
        linea = self.ent_ing.get().strip()
        if not linea:
            messagebox.showwarning("Atención", "Escribe al menos un ingrediente (separados por coma).")
            return
        nuevos = [norm(x) for x in linea.split(",") if norm(x)]
        try:
            insertados, omitidos = self.libro.agregar_ingredientes(nombre, nuevos)
            self.libro.depurar_duplicados_postres()
            self.refresh_ingredientes(nombre)
            self.ent_ing.delete(0, tk.END)
            msg = ""
            if insertados:
                msg += f"Agregados: {', '.join(insertados)}.\n"
            if omitidos:
                msg += f"Omitidos: {', '.join(omitidos)}."
            messagebox.showinfo("Resultado", msg or "Sin cambios.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_eliminar_ingrediente(self):
        nombre = self.get_postre_seleccionado()
        if not nombre:
            messagebox.showwarning("Atención", "Selecciona un postre.")
            return
        sel = self.lst_ingredientes.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un ingrediente de la lista.")
            return
        ing = self.lst_ingredientes.get(sel[0])
        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{ing}' de '{nombre}'?"):
            return
        try:
            self.libro.eliminar_ingrediente(nombre, ing)
            self.refresh_ingredientes(nombre)
            messagebox.showinfo("Éxito", f"Ingrediente '{ing}' eliminado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_buscar_prefijo(self):
        pref = norm(self.ent_busca.get())
        self.refresh_postres(filtro=pref if pref else None)

    def ui_depurar(self):
        rep = self.libro.depurar_duplicados_postres()
        self.refresh_postres()
        messagebox.showinfo(
            "Depuración completada",
            "✔ Limpieza realizada.\n"
            f"- Postres eliminados: {len(rep['postres_eliminados'])}\n"
            f"- Ingredientes duplicados eliminados: {rep['ingredientes_eliminados_total']}"
        )

# ------------------- MAIN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = AppPanaderiaTk(root)
    root.mainloop()
