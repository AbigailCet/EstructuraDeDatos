
import random

class Vectores:
    def __init__(self, longitud):
        self.longitud = longitud
        self.vector_A=[]
        self.vector_B=[]
        self.vector_C=[]

    def llenar_vector_A(self):
        self.vector_A= [random.randint(-100,100) for _ in range(self.longitud)]
        print(f"Vector A llenado correctamente {self.vector_A}")


    def llenar_vector_B(self):
        self.vector_B = [random.randint(-100,100) for _ in range(self.longitud)]
        print(f"Vector B llenado correctamente {self.vector_B}")


    def sumar_vectores (self):
        if self.validar_vectores ():
            self.vector_C = [a + b for a, b in zip(self.vector_A, self.vector_B)]
            print(f"Se realizó la suma: C = A + B es: {self.vector_C}")


    def restar_vectores(self):
        if self.validar_vectores():
            self.vector_C = [b - a for a, b in zip(self.vector_A, self.vector_B)]
            print(f"Se realizó la resta: C = B - A es: {self.vector_C}")


    def mostrar_vector(self, cual):
        while True:
            if cual == "A":
                if self.vector_A:
                    print("Vector A:", self.vector_A)
                else:
                    print("El vector A aún no ha sido llenado")
                break

            elif cual == "B":
                if self.vector_B:
                    print("Vector B:", self.vector_B)
                else:
                    print("El vector B aún no ha sido llenado")
                break

            elif cual == "C":
                if self.vector_C:
                    print("Vector C:", self.vector_C)
                else:
                    print("El vector C aún no ha sido llenado")
                break

            else:
                print("Opción inválida. Debes escribir A, B o C.")

    def validar_vectores(self):
        if not self.vector_A or not self.vector_B:
            print("Deben llenarse primero los vectores A y B")
            llenar = input("¿Desea llenarlos ahora? (s/n): ").lower()
            if llenar == "s":
                self.llenar_vector_A()
                self.llenar_vector_B()
                print("Los vectores A y B han sido llenados correctamente")
                return True
            else:
                print("Deben llenarse los vectores A y B para realizar las operaciones")
                return False
        return True


def menu():
    longitud = int(input("Ingrese la longitud de los vectores: "))
    v = Vectores(longitud)

    while True:
        print(" MENÚ")
        print("1. Llenar Vector A")
        print("2. Llenar Vector B")
        print("3. Realizar C=A+B")
        print("4. Realizar C=B-A")
        print("5. Mostrar Vector (A,B o C)")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                v.llenar_vector_A()
            case "2":
                v.llenar_vector_B()
            case "3":
                v.sumar_vectores()
            case "4":
                v.restar_vectores()
            case "5":
                cual = input("¿Qué vector desea mostrar (A, B o C)? ").upper()
                v.mostrar_vector(cual)
            case "6":
                print("Adiós")
                break
            case _:
                print("Opción inválida.")

if __name__ == "__main__":
    menu()

