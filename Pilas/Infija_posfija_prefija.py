class Pila:
    def __init__(self):
        self.items = []

    def apilar(self, elemento):
        self.items.append(elemento)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        else:
            raise IndexError("Subdesbordamiento: la pila está vacía.")

    def esta_vacia(self):
        return len(self.items) == 0
def evaluar_posfija(expresion):
    pila = Pila()
    operadores = {"+", "-", "*", "/", "^"}

    for simbolo in expresion.split():
        if simbolo not in operadores:
            pila.apilar(float(simbolo))
        else:
            # Se desapilan los dos operandos
            op2 = pila.desapilar()
            op1 = pila.desapilar()

            if simbolo == "+":
                pila.apilar(op1 + op2)
            elif simbolo == "-":
                pila.apilar(op1 - op2)
            elif simbolo == "*":
                pila.apilar(op1 * op2)
            elif simbolo == "/":
                pila.apilar(op1 / op2)
            elif simbolo == "^":
                pila.apilar(op1 ** op2)

    return pila.desapilar()

def evaluar_prefija(expresion):
    pila = Pila()
    operadores = {"+", "-", "*", "/", "^"}

    # Se recorre al revés (de derecha a izquierda)
    for simbolo in expresion.split()[::-1]:
        if simbolo not in operadores:
            pila.apilar(float(simbolo))
        else:
            op1 = pila.desapilar()
            op2 = pila.desapilar()

            if simbolo == "+":
                pila.apilar(op1 + op2)
            elif simbolo == "-":
                pila.apilar(op1 - op2)
            elif simbolo == "*":
                pila.apilar(op1 * op2)
            elif simbolo == "/":
                pila.apilar(op1 / op2)
            elif simbolo == "^":
                pila.apilar(op1 ** op2)

    return pila.desapilar()
def main():
    print("🎯 Evaluador de expresiones con PILAS 🎯")
    print("Elige el tipo de notación a evaluar:")
    print("1. Posfija (Postfix)")
    print("2. Prefija (Prefix)")
    opcion = input("Opción: ")

    expresion = input("\nIngresa la expresión (usa espacios entre símbolos): ")

    try:
        if opcion == "1":
            resultado = evaluar_posfija(expresion)
        elif opcion == "2":
            resultado = evaluar_prefija(expresion)
        else:
            print("❌ Opción no válida.")
            return

        print(f"\n Resultado final: {resultado}")

    except Exception as e:
        print(f"\nError durante la evaluación: {e}")


if __name__ == "__main__":
    main()
