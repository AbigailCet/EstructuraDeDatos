"""
Notas:

Una lista enlazada simple (Singly Linked List) es una estructura lineal compuesta por nodos.
Cada nodo contiene dos partes:
  - data: almacena el valor del elemento
  - next: referencia al siguiente nodo en la lista
A diferencia de una lista de Python, los elementos no están en posiciones contiguas en memoria.

Ventajas:
- Inserciones y eliminaciones eficientes sin necesidad de mover todos los elementos.
Desventajas:
- Acceso secuencial (no se puede acceder directamente a un índice como en una lista normal).
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class MyLinkedList:

    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self.size

    def append(self, data): # Agregar al final de la lista
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, data): #Agregar al inicio de la lista
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, position, data):# Insertar en una posición específica
        if position < 0 or position > self.size:
            raise IndexError("Posición fuera de rango.")
        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self.head
            for _ in range(position - 1):
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node
        self.size += 1

    def delete_at(self, position): #Eliminar en una posición específica
        if self.is_empty():
            raise IndexError("La lista está vacía.")
        if position < 0 or position >= self.size:
            raise IndexError("Posición fuera de rango.")
        if position == 0:
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(position - 1):
                prev = prev.next
            prev.next = prev.next.next
        self.size -= 1

    def delete(self, data): #Eliminar por valor
        if self.is_empty():
            raise IndexError("La lista está vacía.")
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return
        prev = self.head
        while prev.next and prev.next.data != data:
            prev = prev.next
        if prev.next is None:
            raise ValueError("Dato no encontrado en la lista.")
        prev.next = prev.next.next
        self.size -= 1

    def get(self, position): #Obtener dato en una posición específica
        if position < 0 or position >= self.size:
            raise IndexError("Posición fuera de rango.")
        current = self.head
        for _ in range(position):
            current = current.next
        return current.data

    def find(self, data): #Obtener la posición de un dato específico
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def to_list(self): #Convertir la lista enlazada a una lista de Python
        out = []
        current = self.head
        while current:
            out.append(current.data)
            current = current.next
        return out
    def clear(self): #Vaciar la lista
        self.head = None
        self.size = 0

    def info(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

if __name__ == "__main__":
    lista = MyLinkedList()

    while True:
        print("\n===== MENÚ LISTA ENLAZADA =====")
        print("1. Agregar al final (append)")
        print("2. Agregar al inicio (prepend)")
        print("3. Insertar en una posición específica")
        print("4. Eliminar por valor")
        print("5. Eliminar por posición")
        print("6. Buscar por valor (find)")
        print("7. Obtener dato por posición (get)")
        print("8. Mostrar lista (info)")
        print("9. Convertir lista a tipo Python (to_list)")
        print("10. Vaciar lista (clear)")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ")

        try:
            if opcion == "1":
                dato = int(input("Ingresa el número a agregar: "))
                lista.append(dato)
                print("Número agregado al final.")

            elif opcion == "2":
                dato = int(input("Ingresa el número a agregar al inicio: "))
                lista.prepend(dato)
                print("Número agregado al inicio.")

            elif opcion == "3":
                pos = int(input("Ingresa la posición donde insertar: "))
                dato = int(input("Ingresa el número: "))
                lista.insert_at(pos, dato)
                print("Número insertado correctamente.")

            elif opcion == "4":
                dato = int(input("Ingresa el número a eliminar: "))
                lista.delete(dato)
                print("Número eliminado correctamente.")

            elif opcion == "5":
                pos = int(input("Ingresa la posición a eliminar: "))
                lista.delete_at(pos)
                print("Nodo eliminado correctamente.")

            elif opcion == "6":
                dato = int(input("Número a buscar: "))
                pos = lista.find(dato)
                if pos != -1:
                    print(f"El número {dato} está en la posición {pos}.")
                else:
                    print(f"El número {dato} no se encontró en la lista.")

            elif opcion == "7":
                pos = int(input("Ingresa la posición: "))
                valor = lista.get(pos)
                print(f"El valor en la posición {pos} es: {valor}")

            elif opcion == "8":
                print("\nContenido de la lista:")
                lista.info()

            elif opcion == "9":
                print("Lista en formato Python:", lista.to_list())

            elif opcion == "10":
                lista.clear()
                print("Lista vaciada correctamente.")

            elif opcion == "0":
                print("Adiós")
                break

            else:
                print("Opción no válida. Intenta de nuevo.")

        except ValueError:
            print("Error: Debes ingresar un número entero válido.")
        except (IndexError, Exception) as e:
            print("Error:", e)

