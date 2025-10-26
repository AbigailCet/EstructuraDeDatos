class Order:
    def __init__(self, customer, qtty):
        self.__customer = customer
        self.__qtty = qtty

    def print(self):
        print(f"Customer:{self.__customer}")
        print(f"Quantity:{self.__qtty}")
        print("------------")

class Node:
     def __init__(self, data):
         self.data = data # Referencia al Order(data guarda el custumer y qtty)
         self.next = None #Referencia al siguiente nodo

class Queue:
    def __init__(self):
        self.front = None # Primer nodo (head)
        self.tail = None  # Último nodo (tail)
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self.front is None

    def enqueue(self, data): # Agregar al final (tail)
        new_node = Node(data)
        if self.is_empty():
            self.front = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node # Apuntar el actual tail al nuevo nodo
            self.tail = new_node #Convertir el nuevo nodo en el tail
        self._size += 1

    def peek(self): # Ver el frente sin eliminar
        if self.is_empty():
            return None
        return self.front.data

    def dequeue(self): # Eliminar del frente (front)
        if self.is_empty():
            return None
        removed_node = self.front #Guardo el nodo a eliminar
        self.front = removed_node.next #Muevo el front al siguiente nodo
        if self.front is None: #Si la cola queda vacía, actualizo el tail a no hay
            self.tail = None
        self._size  -= 1
        return removed_node.data


    def get_nth(self, position): #posición del elemento a obtener
        if position <= 0 or position > self._size:
            return None
        current = self.front
        index = 1
        while index < position:
            current = current.next
            index += 1

        return current.data #Retorno el Order no el Node

    def printInfo(self):
        print("********** QUEUE DUMP **********")
        print(f"Size: {self._size}")
        print("-------------------------------")
        current = self.front
        index = 1 #Index es solo un contador para mostrar la posición
        while current is not None:
            print(f"Elemento {index}:")
            current.data.print()
            current = current.next
            index += 1
        print("*******************************")
        print()

if __name__ == "__main__":
    # 1. Crear la cola
    q = Queue()

    # 2. Crear pedidos
    o1 = Order("cust1", 20)
    o2 = Order("cust2", 30)
    o3 = Order("cust3", 40)
    o4 = Order("cust4", 50)
    # 3. Enqueue de cada orden, mostrando el estado después
    print(">>> Enqueue o1")
    q.enqueue(o1)
    q.printInfo()

    print(">>> Enqueue o2")
    q.enqueue(o2)
    q.printInfo()

    print(">>> Enqueue o3")
    q.enqueue(o3)
    q.printInfo()

    # 4. Ver el frente (front / peek)
    print(">>> Front (peek sin sacar):")
    first = q.peek()
    if first:
        print("Elemento en el frente:")
        first.print()

    # 5. Dequeue (sacar uno)
    print(">>> Dequeue:")
    removed = q.dequeue()
    if removed:
        print("Elemento removido:")
        removed.print()

    print("Estado de la cola después del dequeue:")
    q.printInfo()

     # 6️. Agregar otro elemento (enqueue)
    print(">>> Enqueue o4")
    q.enqueue(o4)
    q.printInfo()

    print(">>> get_nth(3):")   # debería regresarte el tercer elemento
    nth = q.get_nth(3)
    if nth:
        print("Elemento en la posición 3:")
        nth.print()
    else:
        print("Posición inválida.")
