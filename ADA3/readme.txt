# Ventas

Este proyecto contiene la clase `Ventas`, que gestiona una matriz bidimensional para almacenar y manipular las ventas de diferentes departamentos por mes. Hay implementaciones tanto en **Python** como en **Java**.

---

## Estructura de la matriz

- **Filas:** Cada fila representa un mes del año.
- **Columnas:** Las columnas corresponden a los departamentos: Ropa, Deportes y Juguetería.

---

## Implementación en Python

### Métodos principales

#### `__init__()`
Inicializa la matriz de ventas con los meses y departamentos. Cada celda de ventas comienza en cero.

#### `ingresar_venta(mes, departamento, monto)`
Agrega una venta al departamento y mes especificados, sumando el monto al valor actual.

- **Parámetros:**  
  - `mes`: Nombre del mes (ej. "Enero").
  - `departamento`: Nombre del departamento (ej. "Ropa").
  - `monto`: Valor de la venta a agregar.

#### `insertar_venta_departamento(departamento)`
Permite ingresar manualmente las ventas de un departamento para cada mes mediante la consola.

- **Parámetro:**  
  - `departamento`: Nombre del departamento.

#### `eliminar_venta_departamento(departamento, mes)`
Elimina (pone a cero) la venta de un departamento en un mes específico.

- **Parámetros:**  
  - `departamento`: Nombre del departamento.
  - `mes`: Nombre del mes.

#### `mostrar_matriz()`
Muestra la matriz completa de ventas en formato, con los nombres de los departamentos como encabezados y los meses como filas.

**Ejemplo de uso:**

```python
ventas = Ventas()
ventas.mostrar_matriz()
ventas.ingresar_venta("Enero", "Ropa", 1500)
ventas.mostrar_matriz()
ventas.eliminar_venta_departamento("Ropa", "Enero")
ventas.mostrar_matriz()
```

---

## Implementación en Java

### Métodos principales

#### `Ventas()`
Constructor que inicializa la matriz de ventas con los meses y departamentos. Cada celda de ventas comienza en cero.

#### `ingresarVenta(mes, departamento, monto)`
Agrega una venta al departamento y mes especificados, sumando el monto al valor actual.

- **Parámetros:**  
  - `mes`: Nombre del mes (ej. "Enero").
  - `departamento`: Nombre del departamento (ej. "Ropa").
  - `monto`: Valor de la venta a agregar.

#### `ingresarVentaDepartamento(departamento, monto)`
Agrega el mismo monto de venta para un departamento en todos los meses del año.

- **Parámetro:**  
  - `departamento`: Nombre del departamento.
  - `monto`: Valor de la venta a agregar en cada mes.

#### `eliminarVenta(mes, departamento)`
Elimina (pone a cero) la venta de un departamento en un mes específico.

- **Parámetros:**  
  - `mes`: Nombre del mes.
  - `departamento`: Nombre del departamento.

#### `mostrarMatriz()`
Muestra la matriz completa de ventas en formato, con los nombres de los departamentos como encabezados y los meses como filas.

**Ejemplo de uso:**

```java
Ventas ventas = new Ventas();
ventas.ingresarVenta("Enero", "Ropa", 500);
ventas.ingresarVenta("Febrero", "Deportes", 300);
ventas.ingresarVenta("Marzo", "Jugueteria", 400);
ventas.eliminarVenta("Febrero", "Deportes");
ventas.mostrarMatriz();
```

---

Ambas implementaciones permiten gestionar las ventas por mes y departamento de forma sencilla y visual.
