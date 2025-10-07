from collections import deque

class Cola:
    def __init__(self):
        self.items = deque()

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.popleft()

    def esta_vacia(self):
        return len(self.items) == 0

    def __repr__(self):
        return f"{list(self.items)}"


# === PROGRAMA PRINCIPAL ===

# Diccionario con las colas de cada servicio
colas = {
    1: Cola(),
    2: Cola(),
    3: Cola()
}
print("Sistema de colas - Compañía de Seguros")
print("Comandos:")
print("  Cn = llega cliente al tipo de servicio n  (ej: C1)")
print("  An = atender cliente del servicio n  (ej: A2)")
print("  S = salir\n")

#Flujo principal del programa

while True:

#restringimos y limpiamos el input
    comando = input("Ingrese comando: ").strip().upper()

    if comando == "S":
        print("Saliendo del sistema...")
        break
    if len(comando) != 2 or not comando[1].isdigit():
        print("⚠️  Comando inválido. Ejemplo: C1, A2, S")
        continue

#Ejecutamos el comando
    letra = comando[0] #la posición 0 del comando es la letra
    servicio = int(comando[1]) #la posición 1 del comando es el número de servicio

    if servicio not in colas:
        print("⚠️  Servicio no válido (solo existen 1, 2 y 3)")
        continue

    #contadores para cada servicio
    contador_servicio = {1: 0, 2: 0, 3: 0}

    # Cliente nuevo
    if letra == "C":
        contador_servicio[servicio] += 1
        numero_cliente = contador_servicio[servicio]
        colas[servicio].encolar(numero_cliente)
        print(f"Cliente {numero_cliente} agregado a la cola del servicio {servicio}")

    # Atender cliente
    elif letra == "A":
        if colas[servicio].esta_vacia():
            print(f"No hay clientes en la cola del servicio {servicio}")
        else:
            cliente = colas[servicio].desencolar()
            print(f"Atendiendo al cliente {cliente} del servicio {servicio}")

    # Estado de las colas (opcional, para depuración visual)
    print(f"Estado actual: {colas}\n")
