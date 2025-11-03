class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.sig = None
        self.ant = None

class Lista:
    def __init__(self):
        self.head = None
        self.tail = None
        self.posicion = None
    def avanzar(self, posiciones):
        if self.head is None or posiciones <= 0:
            return  # lista vacía o avance no válido

        # Si el cursor está fuera (None), lo colocamos en el primer nodo
        if self.posicion is None:
            self.posicion = self.head
            posiciones -= 1  # ya contamos este paso inicial

        # Avanzamos hasta que no queden pasos o lleguemos al final
        while posiciones > 0 and self.posicion.sig is not None:
            self.posicion = self.posicion.sig
            posiciones -= 1

    def retroceder(self, posiciones):
        if self.head is None or posiciones <= 0 or self.posicion is None:
            return  # nada que hacer

        # Retroceder hasta que no queden pasos o lleguemos al principio
        while posiciones > 0 and self.posicion.ant is not None:
            self.posicion = self.posicion.ant
            posiciones -= 1

    def insertar(self, dato):
        nuevo = Nodo(dato)

        # Caso 1: lista vacía
        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
            self.posicion = nuevo
            return

        # Caso 2: cursor está fuera (insertar al inicio)
        if self.posicion is None:
            nuevo.sig = self.head
            self.head.ant = nuevo
            self.head = nuevo
            self.posicion = nuevo
            return

        # Caso 3: insertar después del cursor actual
        nuevo.ant = self.posicion
        nuevo.sig = self.posicion.sig

        if self.posicion.sig is not None:
            self.posicion.sig.ant = nuevo #Siself.posicion.sig no es nulo, actualizar su enlace anterior al nuevo nodo 
        else: #si self posicion.sig es nulo (el ultimo), significa que estamos insertando al final de la lista
            self.tail = nuevo  # si insertamos al final, actualizar tail

        self.posicion.sig = nuevo
        self.posicion = nuevo

    def extraer(self):
        if self.posicion is None:
            return None  # nada que extraer

        dato = self.posicion.dato
        nodo_a_borrar = self.posicion

        # Actualizar enlaces
        if nodo_a_borrar.ant is not None:
            nodo_a_borrar.ant.sig = nodo_a_borrar.sig
        else:
            self.head = nodo_a_borrar.sig  # borramos el primero

        if nodo_a_borrar.sig is not None:
            nodo_a_borrar.sig.ant = nodo_a_borrar.ant
        else:
            self.tail = nodo_a_borrar.ant  # borramos el último

        # Avanzar la posición
        self.posicion = nodo_a_borrar.sig
        return dato

    def mostrar(self):
        actual = self.head
        print("Lista actual:", end=" ")
        while actual:
             # Si el nodo actual es donde está el cursor, le ponemos una marca visual
            marca = " ←pos" if actual == self.posicion else ""
            print(f"[{actual.dato}]{marca}", end=" <-> ")
            actual = actual.sig
        print("None\n")

if __name__ == "__main__":
    l = Lista()

    l.insertar("A")
    l.insertar("B")
    l.insertar("C")
    l.mostrar()

    l.retroceder(1)
    l.insertar("X")
    l.mostrar()

    dato = l.extraer()
    print(f"Extraído: {dato}")
    l.mostrar()

    l.avanzar(2)
    l.insertar("Z")
    l.mostrar()





