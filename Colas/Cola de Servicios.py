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


# === CONFIGURACIÓN INICIAL ===
while True:
    try:
        n = int(input("¿Cuántos servicios habrá? (≥1): ").strip())
        if n >= 1:
            break
        print("Debe ser al menos 1.")
    except ValueError:
        print("Ingresa un número entero válido.")

# Diccionario con las colas de cada servicio y contadores de turnos
colas = {i: Cola() for i in range(1, n + 1)}
contador_servicio = {i: 0 for i in range(1, n + 1)}

print("\nSistema de colas - Compañía de Seguros")
print("Menú (comandos):")
print("  Cn = llega cliente al servicio n   (ej: C1, C12)")
print("  An = atender cliente del servicio n (ej: A2, A10)")
print("  S  = salir\n")

# === FLUJO PRINCIPAL ===
while True:
    comando = input("Ingrese comando: ").strip().upper()

    if comando == "S":
        print("Saliendo del sistema...")
        break

    if len(comando) < 2:
        print("Comando inválido. Ejemplo: C1, A2, S")
        continue

    letra = comando[0]          # 'C' o 'A'
    resto = comando[1:]         # '1', '12', etc.

    if not resto.isdigit():
        print(" Debe indicar número de servicio. Ejemplo: C1, A2")
        continue

    servicio = int(resto)
    if servicio not in colas:
        print(f" Servicio no válido (solo existen 1..{n})")
        continue

    # === OPERACIONES ===
    if letra == "C":
        contador_servicio[servicio] += 1
        turno = contador_servicio[servicio]
        colas[servicio].encolar(turno)
        print(f"Llegó cliente. Asignado turno {turno} al servicio {servicio}.")

    elif letra == "A":
        if colas[servicio].esta_vacia():
            print(f"No hay clientes en la cola del servicio {servicio}.")
        else:
            turno = colas[servicio].desencolar()
            print(f" Atendiendo turno {turno} del servicio {servicio}.")

    else:
        print(" Opción inválida. Usa Cn, An o S.")
        continue

    # Estado de las colas
    print(f"Estado actual: {colas}\n")
