
# Fibonacci en Python

Este proyecto contiene dos implementaciones para calcular la serie de Fibonacci en Python: una versión **recursiva** y otra **iterativa** (sin recursividad). Además, incluye ejemplos de operaciones con vectores y matrices usando listas y la librería NumPy.

---

## 1. Fibonacci Recursivo (`fibonacci.py`)

### Funcionamiento

La función `fibonaci(n)` calcula el n-ésimo número de la serie de Fibonacci usando **recursividad**.  
- Si `n <= 0`, retorna 0 (caso base).
- Si `n == 1`, retorna 1 (caso base).
- Para otros valores, retorna la suma de los dos valores anteriores: `fibonaci(n-1) + fibonaci(n-2)`.

El script imprime los primeros 11 números de la serie:

```python
for i in range(11):
    print(fibonaci(i))
```

### Ventajas y desventajas

- **Ventaja:** Código sencillo y fácil de entender.
- **Desventaja:** Muy ineficiente para valores grandes de `n` porque recalcula muchas veces los mismos valores (complejidad exponencial).

---

## 2. Fibonacci Iterativo (`fibonacciSinRec.py`)

### Funcionamiento

La función `fibonacci(n)` calcula el n-ésimo número de la serie de Fibonacci usando un **bucle** (sin recursividad).  
- Usa dos variables para almacenar los dos últimos valores de la serie.
- Actualiza los valores en cada iteración del bucle.
- Retorna el valor final después de `n` iteraciones.

El script imprime los primeros 11 números de la serie:

```python
for i in range(11):
    print(fibonacci(i))
```

### Ventajas y desventajas

- **Ventaja:** Mucho más eficiente que la versión recursiva (complejidad lineal).
- **Desventaja:** El código puede ser menos intuitivo para quienes recién aprenden recursividad.

---




