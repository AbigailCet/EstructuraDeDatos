import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Opciones que verá el usuario
ALGORITMOS_UI = ["MD5", "SHA-256", "SHA-512"]
MAPEO_ALGORITMOS = {
    "MD5": "md5",
    "SHA-256": "sha256",
    "SHA-512": "sha512"
}

def calcular_hash_archivo(ruta_archivo, algoritmo="sha256", buffer_size=65536):
    """
    Calcula el hash de un archivo usando hashlib.
    Soporta:
      - MD5
      - SHA-256
      - SHA-512
    """
    try:
        hasher = hashlib.new(algoritmo)
    except ValueError:
        raise ValueError(f"Algoritmo de hash no válido: {algoritmo}")

    with open(ruta_archivo, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()

class AppHashArchivos:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de archivos y hashes")
        self.root.geometry("900x520")

        self.carpeta_base = None
        self.indice_a_ruta = {}

        self.crear_widgets()

    def crear_widgets(self):
        # Frame superior
        frame_top = ttk.Frame(self.root, padding=10)
        frame_top.pack(fill="x")

        btn_carpeta = ttk.Button(frame_top, text="Seleccionar carpeta", command=self.seleccionar_carpeta)
        btn_carpeta.pack(side="left")

        self.lbl_carpeta = ttk.Label(frame_top, text="Ninguna carpeta seleccionada")
        self.lbl_carpeta.pack(side="left", padx=10)

        # Selección de algoritmo
        frame_alg = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        frame_alg.pack(fill="x")

        lbl_alg = ttk.Label(frame_alg, text="Algoritmo de hash:")
        lbl_alg.pack(side="left")

        self.combo_algoritmo = ttk.Combobox(
            frame_alg,
            values=ALGORITMOS_UI,
            state="readonly",
            width=15
        )
        self.combo_algoritmo.set("SHA-256")
        self.combo_algoritmo.pack(side="left", padx=10)

        # Frame principal
        frame_main = ttk.Frame(self.root, padding=10)
        frame_main.pack(fill="both", expand=True)

        # Lista de archivos
        frame_lista = ttk.Frame(frame_main)
        frame_lista.pack(side="left", fill="both", expand=True)

        lbl_lista = ttk.Label(frame_lista, text="Archivos encontrados:")
        lbl_lista.pack(anchor="w")

        self.listbox_archivos = tk.Listbox(frame_lista, selectmode=tk.SINGLE)
        self.listbox_archivos.pack(side="left", fill="both", expand=True)

        scroll_lista = ttk.Scrollbar(frame_lista, orient="vertical", command=self.listbox_archivos.yview)
        scroll_lista.pack(side="right", fill="y")
        self.listbox_archivos.config(yscrollcommand=scroll_lista.set)

        # Panel de hash
        frame_hash = ttk.Frame(frame_main)
        frame_hash.pack(side="right", fill="both", expand=True)

        btn_hash = ttk.Button(
            frame_hash,
            text="Calcular hash del archivo seleccionado",
            command=self.mostrar_hash
        )
        btn_hash.pack(fill="x", pady=(0, 5))

        btn_hash_todos = ttk.Button(
            frame_hash,
            text="Calcular hash de TODOS los archivos",
            command=self.mostrar_hash_todos
        )
        btn_hash_todos.pack(fill="x", pady=(0, 10))

        self.lbl_archivo_sel = ttk.Label(frame_hash, text="Archivo seleccionado: ninguno")
        self.lbl_archivo_sel.pack(anchor="w", pady=(0, 5))

        self.lbl_alg_usado = ttk.Label(frame_hash, text="Algoritmo actual: SHA-256")
        self.lbl_alg_usado.pack(anchor="w")

        lbl_hash = ttk.Label(frame_hash, text="Resultado:")
        lbl_hash.pack(anchor="w")

        self.txt_hash = tk.Text(frame_hash, height=15)
        self.txt_hash.pack(fill="both", expand=True)

        # Eventos
        self.listbox_archivos.bind("<<ListboxSelect>>", self.actualizar_archivo_seleccionado)
        self.combo_algoritmo.bind("<<ComboboxSelected>>", self.actualizar_algoritmo_label)

    def actualizar_algoritmo_label(self, event=None):
        alg = self.combo_algoritmo.get()
        self.lbl_alg_usado.config(text=f"Algoritmo actual: {alg}")

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Selecciona una carpeta")
        if not carpeta:
            return

        self.carpeta_base = carpeta
        self.lbl_carpeta.config(text=f"Carpeta: {carpeta}")
        self.cargar_archivos()

    def cargar_archivos(self):
        self.listbox_archivos.delete(0, tk.END)
        self.indice_a_ruta.clear()
        self.txt_hash.delete("1.0", tk.END)
        self.lbl_archivo_sel.config(text="Archivo seleccionado: ninguno")

        if not self.carpeta_base:
            return

        indice = 0
        for root, dirs, files in os.walk(self.carpeta_base):
            for archivo in files:
                ruta_completa = os.path.join(root, archivo)
                ruta_relativa = os.path.relpath(ruta_completa, self.carpeta_base)

                self.listbox_archivos.insert(tk.END, ruta_relativa)
                self.indice_a_ruta[indice] = ruta_completa
                indice += 1

    def actualizar_archivo_seleccionado(self, event=None):
        seleccion = self.listbox_archivos.curselection()
        if not seleccion:
            self.lbl_archivo_sel.config(text="Archivo seleccionado: ninguno")
            return

        idx = seleccion[0]
        self.lbl_archivo_sel.config(text=f"Archivo seleccionado: {self.listbox_archivos.get(idx)}")

    def _algoritmo_actual(self):
        alg_ui = self.combo_algoritmo.get()
        return MAPEO_ALGORITMOS[alg_ui]

    def mostrar_hash(self):
        seleccion = self.listbox_archivos.curselection()
        if not seleccion:
            messagebox.showwarning("Sin archivo", "Selecciona un archivo primero.")
            return

        idx = seleccion[0]
        ruta = self.indice_a_ruta[idx]
        algoritmo = self._algoritmo_actual()

        try:
            hash_valor = calcular_hash_archivo(ruta, algoritmo=algoritmo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular el hash:\n{e}")
            return

        self.txt_hash.delete("1.0", tk.END)
        self.txt_hash.insert(tk.END, f"Archivo: {self.listbox_archivos.get(idx)}\n")
        self.txt_hash.insert(tk.END, f"Hash ({self.combo_algoritmo.get()}):\n{hash_valor}\n")

    def mostrar_hash_todos(self):
        if not self.indice_a_ruta:
            messagebox.showwarning("Sin archivos", "No hay archivos en la carpeta.")
            return

        algoritmo = self._algoritmo_actual()
        algoritmo_ui = self.combo_algoritmo.get()

        self.txt_hash.delete("1.0", tk.END)
        self.txt_hash.insert(tk.END, f"Hash de TODOS los archivos ({algoritmo_ui}):\n\n")

        total = len(self.indice_a_ruta)
        errores = 0

        for idx in range(total):
            ruta = self.indice_a_ruta[idx]
            nombre = self.listbox_archivos.get(idx)
            try:
                hash_valor = calcular_hash_archivo(ruta, algoritmo=algoritmo)
                self.txt_hash.insert(tk.END, f"[OK] {nombre}\n")
                self.txt_hash.insert(tk.END, f"     {hash_valor}\n\n")
            except Exception as e:
                errores += 1
                self.txt_hash.insert(tk.END, f"[ERROR] {nombre}\n")
                self.txt_hash.insert(tk.END, f"     {e}\n\n")

        self.txt_hash.insert(tk.END, f"\nFinalizado. Total archivos: {total}, Errores: {errores}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppHashArchivos(root)
    root.mainloop()
