
# FormasAB

Este proyecto compara dos formas de organizar y acceder a datos de alumnos y materias usando arreglos bidimensionales en Python.

## Estructura

El archivo `FormasAB.py` contiene funciones para crear y probar dos formas de almacenar calificaciones:

- **Forma A:**  
  - Las **filas** representan las materias.  
  - Las **columnas** representan los alumnos.  
  - Acceso: `A[materia][alumno]`

- **Forma B:**  
  - Las **filas** representan los alumnos.  
  - Las **columnas** representan las materias.  
  - Acceso: `B[alumno][materia]`

## Funciones principales

### `crear_forma_A(num_alumnos, nummaterias)`
Crea una matriz donde cada fila es una materia y cada columna es un alumno. Los valores son calificaciones aleatorias.

### `crear_forma_B(num_alumnos, nummaterias)`
Crea una matriz donde cada fila es un alumno y cada columna es una materia. Los valores son calificaciones aleatorias.

### `probar(num_alumnos, num_materias, repeticiones=100000)`
Realiza pruebas de rendimiento para comparar la creación y el acceso a los datos en ambas formas.  
- Mide el tiempo de creación de cada matriz.
- Mide el tiempo de acceso repetido a una celda específica (por ejemplo, alumno 321, materia 5).

## Ejecución

Al ejecutar el script, se realizan pruebas con diferentes tamaños de matrices y se muestran los resultados de tiempo para cada forma.

**Ejemplo de salida:**
```
Forma A (materias en filas): Creación 0.0123s, Acceso 0.0045s
Forma B (alumnos en filas) : Creación 0.0118s, Acceso 0.0042s
```

## Uso

Puedes modificar los parámetros en el bloque `if __name__ == "__main__":` para probar con diferentes cantidades de alumnos y materias.

---

Este proyecto es útil para analizar el rendimiento y la organización de datos en arreglos bidimensionales, especialmente en aplicaciones educativas o de gestión de información.
