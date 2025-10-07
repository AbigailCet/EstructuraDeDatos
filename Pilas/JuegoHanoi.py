class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            return None

    def esta_vacia(self):
        return len(self.items) == 0

    def ver_cima(self):
        return self.items[-1] if self.items else None

    def __repr__(self):
        return f"{self.nombre}: {self.items}"


def mover_disco(origen, destino):
    disco = origen.desapilar()
    destino.apilar(disco)
    print(f"➡ Mover disco {disco} de {origen.nombre} → {destino.nombre}")
    print_estado_torres()


def print_estado_torres():
    print(f"\n{torre_A}\n{torre_B}\n{torre_C}")
    print("-" * 30)


def torres_de_hanoi(n, origen, auxiliar, destino):
    if n == 1:
        mover_disco(origen, destino)
    else:
        # Paso 1: mover n-1 discos a la torre auxiliar
        torres_de_hanoi(n-1, origen, destino, auxiliar)

        # Paso 2: mover el disco más grande al destino
        mover_disco(origen, destino)

        # Paso 3: mover los n-1 discos de la auxiliar al destino
        torres_de_hanoi(n-1, auxiliar, origen, destino)


# --- Programa principal ---
print("🎯 Simulación del juego de las Torres de Hanói (3 discos)\n")


torre_A = Pila("Torre A")
torre_B = Pila("Torre B")
torre_C = Pila("Torre C")

for disco in range(3, 0, -1):
    torre_A.apilar(disco)

print("🏁 Estado inicial:")
print_estado_torres()

torres_de_hanoi(3, torre_A, torre_B, torre_C)

print("\n Juego completado. Todos los discos están en la Torre C.")