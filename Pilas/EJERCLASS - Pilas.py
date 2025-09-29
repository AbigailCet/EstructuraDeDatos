class Pila:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()

# Función para verificar si una palabra es palíndromo
def es_palindromo(palabra):
    pila = Pila()

    # Paso 1: apilamos cada letra
    for letra in palabra:
        pila.apilar(letra)

    # Paso 2: reconstruimos la palabra sacando de la pila
    invertida = ""
    while not pila.esta_vacia():
        invertida += pila.desapilar()

    # Paso 3: comparamos
    return palabra == invertida

# Ejemplo de uso
print(es_palindromo("oso"))     # True
print(es_palindromo("radar"))   # True
print(es_palindromo("casa"))    # False
