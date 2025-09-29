import tkinter as tk
from tkinter import simpledialog, messagebox #simpledialog permite mostrar cuadros emergentes, donde se puede escribir texto

root = tk.Tk() #creo la ventana principal
root.withdraw()  # Oculto la ventana principal para ver solo la emergente


class MemoriaEstatica:
    def __init__(self):
        self.calificaciones =  [0] *5 #ponemos el 0 para ocupar ya esos 5 espacios

    def capturar_calificaciones(self):
       
        for i in range(5):
            while True: 
                try:
                    self.calificaciones [i] = simpledialog.askfloat("Entrada", f"Ingrese la calificación {i + 1}:")
                    break
                except(ValueError, TypeError):
                    messagebox.showerror("Error", "Por favor ingrese un número válido.")
            
        

m = MemoriaEstatica()
m.capturar_calificaciones()
print(m.calificaciones)
