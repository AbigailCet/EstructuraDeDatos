class MemoriaDinamica:
    def __init__(self):
        self.frutas = []
    
    def add_fruta(self,fruta):
        self.frutas.append(fruta)
        print(self.frutas)
    
    def remove_fruta(self,i):
        print(f"Eliminada: {self.frutas[i]}")
        self.frutas.pop(i)
        print(self.frutas)

m = MemoriaDinamica()
m.add_fruta("Mango")
m.add_fruta("Manzana")
m.add_fruta("Banana")
m.add_fruta("Uvas")
m.remove_fruta(0) 
#Si quiero eliminar manzana como indice 1 debo ir de mayor a menor índice, primero elimino manzana y luego como mango no cambiara de índice, lo elimino
m.remove_fruta(1)
m.add_fruta("Sandia")
