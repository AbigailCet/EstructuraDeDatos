from collections import deque

# ===== COLA basada en deque =====
class Cola:
    def __init__(self):
        self.items = deque()

    def encolar(self, elemento):
        self.items.append(elemento)        # O(1)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.popleft()    # O(1)

    def esta_vacia(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"{list(self.items)}"


# ===== Helpers de Entrada =====
def leer_entero(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("⚠️  Entrada inválida. Intenta de nuevo.")

def leer_servicio(max_servicios):
    while True:
        s = leer_entero(f"Selecciona servicio (1..{max_servicios}): ")
        if 1 <= s <= max_servicios:
            return s
        print(f"⚠️  Servicio fuera de rango. Debe estar entre 1 y {max_servicios}.")


# ===== Lógica de Negocio =====
def crear_servicios(n):
    """Crea diccionarios: colas por servicio y contadores de turnos por servicio."""
    colas = {i: Cola() for i in range(1, n + 1)}
    contadores = {i: 0 for i in range(1, n + 1)}  # turno incremental por servicio
    return colas, contadores

def llegada_cliente(colas, contadores, servicio):
    """Asigna un nuevo turno al servicio y lo encola."""
    contadores[servicio] += 1
    turno = contadores[servicio]
    colas[servicio].encolar(turno)
    print(f"✅ Llegó cliente. Asignado turno {turno} al servicio {servicio}.")

def atender_cliente(colas, servicio):
    """Desencola y muestra el turno llamado, si existe."""
    if colas[servicio].esta_vacia():
        print(f"ℹ️  No hay clientes en la cola del servicio {servicio}.")
    else:
        turno = colas[servicio].desencolar()
        print(f"📢 Atendiendo turno {turno} del servicio {servicio}.")

def mostrar_estado(colas):
    """Muestra todas las colas (front→back)."""
    print("\n=== Estado actual de colas ===")
    for s, cola in colas.items():
        print(f"Servicio {s}: {cola}")
    print("==============================\n")


# ===== Programa principal con menú match–case =====
def main():
    print("=== Sistema de Colas — Compañía de Seguros ===")
    n = 0
    while n < 1:
        n = leer_entero("¿Cuántos servicios habrá? (≥1): ")
        if n < 1:
            print("⚠️  Debe ser al menos 1.")

    colas, contadores = crear_servicios(n)

    while True:
        print("Menú:")
        print("  1) Llegada de cliente (C)")
        print("  2) Atender cliente     (A)")
        print("  3) Ver estado de colas")
        print("  4) Salir")
        opcion = input("Elige opción: ").strip()

        match opcion:
            case "1" | "C" | "c":
                servicio = leer_servicio(n)
                llegada_cliente(colas, contadores, servicio)

            case "2" | "A" | "a":
                servicio = leer_servicio(n)
                atender_cliente(colas, servicio)

            case "3":
                mostrar_estado(colas)

            case "4":
                print("👋 Saliendo…")
                break

            case _:
                print("⚠️  Opción inválida.")

if __name__ == "__main__":
    main()
