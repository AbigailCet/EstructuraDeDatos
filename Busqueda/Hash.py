import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

def calcular_hash_archivo(ruta_archivo, buffer_size=65536):
    """
    Calcula el hash SHA-256 de un archivo.
    Lee el archivo en bloques para soportar archivos grandes.
    """
    try:
        hasher = hashlib.new("sha256")  # Solo SHA-256
    except ValueError:
        raise ValueError("Error al crear el hash con SHA-256")

    with open(ruta_archivo, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()

def recorrer_carpeta_y_hashear(ruta_carpeta):
    """
    Recorre una carpeta (incluyendo subcarpetas) y muestra
    el hash SHA-256 de cada archivo.
    """
    if not os.path.isdir(ruta_carpeta):
        print(f"❌ La ruta '{ruta_carpeta}' no es una carpeta válida.")
        return

    print(f"\nCarpeta: {ruta_carpeta}")
    print(f"Algoritmo de hash: SHA-256")
    print("-" * 80)

    for root, dirs, files in os.walk(ruta_carpeta):
        for nombre_archivo in files:
            ruta_completa = os.path.join(root, nombre_archivo)
            try:
                hash_archivo = calcular_hash_archivo(ruta_completa)
                tamano = os.path.getsize(ruta_completa)

                print(f"Archivo : {ruta_completa}")
                print(f"Tamaño : {tamano} bytes")
                print(f"Hash   : {hash_archivo}")
                print("-" * 80)
            except PermissionError:
                print(f"⚠️  Sin permiso para leer: {ruta_completa}")
            except Exception as e:
                print(f"⚠️  Error con '{ruta_completa}': {e}")

def seleccionar_carpeta_y_ejecutar():
    """
    Abre un cuadro de diálogo para seleccionar una carpeta
    y, si se selecciona, ejecuta el cálculo de hashes.
    """
    # Creamos una ventana de Tkinter oculta, solo para usar el diálogo
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    carpeta = filedialog.askdirectory(title="Selecciona una carpeta para calcular hashes")
    if not carpeta:
        messagebox.showinfo("Sin carpeta", "No se seleccionó ninguna carpeta.")
        root.destroy()
        return

    # Opcional: mensaje de confirmación
    messagebox.showinfo("Carpeta seleccionada", f"Se calcularán hashes en:\n{carpeta}")
    root.destroy()

    # Ejecutamos la lógica en consola
    recorrer_carpeta_y_hashear(carpeta)

if __name__ == "__main__":
    seleccionar_carpeta_y_ejecutar()
