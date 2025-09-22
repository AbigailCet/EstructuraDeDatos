#Fibonacci sin recursividad
def fibonacci(n:int)->int:
    primer_valor, segundo_valor=0,1
    for _ in range(n):
        primer_valor, segundo_valor=segundo_valor,primer_valor+segundo_valor
    return primer_valor

for i in range(11):
    print(fibonacci(i))
#No tiene recursividad por que no se llama a si misma


import numpy as np

# Crear un vector (array unidimensional) con NumPy
vec1 = np.array([1, 2, 3])
print(vec1)         # salida: [1 2 3]
print(vec1.shape)   # salida: (3,)  -> dimensión 1D de longitud 3

# Crear una matriz (array bidimensional) con NumPy
matriz2 = np.array([[1, 2, 3],
                    [4, 5, 6]])
print(matriz2)
# salida: 
# [[1 2 3]
#  [4 5 6]]
print(matriz2.shape)  # salida: (2, 3) -> 2 filas, 3 columnas

lista_a = [1, 2, 3]
lista_b = [4, 5, 6]
# Suma con listas (usando comprensión, como vimos antes)
suma_listas = [x + y for x, y in zip(lista_a, lista_b)]

vec_a = np.array(lista_a)
vec_b = np.array(lista_b)
# Suma con NumPy (operación vectorizada)
suma_arrays = vec_a + vec_b

print(suma_listas)  # salida: [5, 7, 9]
print(suma_arrays)  # salida: [5 7 9]


