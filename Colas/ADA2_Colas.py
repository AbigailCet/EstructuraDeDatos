class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)

    def esta_vacia(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"Cola(front→back): {self.items}"

def sumar_colas(colaA, colaB):
    colaResultado = Cola()

    while not colaA.esta_vacia() and not colaB.esta_vacia():
        elementoA = colaA.desencolar()
        elementoB = colaB.desencolar()
        colaResultado.encolar(elementoA + elementoB)

    return colaResultado

n=int(input(f"Ingrese la cantidad de elementos que tendrá cada cola: "))
colaA = Cola()
valoresA = input(f"Ingrese los {n} elemnetos de la cola A separados por espacios: ").split()
for v in valoresA:
    colaA.encolar(int(v))

colaB = Cola()
valoresB = input(f"Ingrese los {n} elementos de la cola B separados por espacios: ").split()
for v in valoresB:
    colaB.encolar(int(v))

resultado = sumar_colas(colaA, colaB)
print("\nCola Resultado:", resultado)
