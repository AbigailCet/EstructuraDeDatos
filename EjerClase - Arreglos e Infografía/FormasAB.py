import random
import time
import cProfile

def crear_forma_A(num_alumnos: int, nummaterias: int):
    # Filas = materias, columnas = alumnos  → A[m][a]
    return [[random.randint(0, 100) for _ in range(num_alumnos)]
            for _ in range(nummaterias)]

def crear_forma_B(num_alumnos: int, nummaterias: int):
    # Filas = alumnos, columnas = materias  → B[a][m]
    return [[random.randint(0, 100) for _ in range(nummaterias)]
            for _ in range(num_alumnos)]

def probar(num_alumnos, num_materias, repeticiones=100000):
    print(f"\n=== Prueba con {num_alumnos} alumnos y {num_materias} materias ===")

    # Crear Forma A
    inicio = time.time()
    A = crear_forma_A(num_alumnos, num_materias)
    t_creacion_A = time.time() - inicio

    # Crear Forma B
    inicio = time.time()
    B = crear_forma_B(num_alumnos, num_materias)
    t_creacion_B = time.time() - inicio

    # Acceso: Alumno 321, Materia 5 (si existe)
    alumno = min(321, num_alumnos) - 1
    materia = min(5, num_materias) - 1

    inicio = time.time()
    for _ in range(repeticiones):
        _ = A[materia][alumno]
    t_acceso_A = time.time() - inicio

    inicio = time.time()
    for _ in range(repeticiones):
        _ = B[alumno][materia]
    t_acceso_B = time.time() - inicio

    # Resultados
    print(f"Forma A (materias en filas): Creación {t_creacion_A:.4f}s, Acceso {t_acceso_A:.4f}s")
    print(f"Forma B (alumnos en filas) : Creación {t_creacion_B:.4f}s, Acceso {t_acceso_B:.4f}s")
    
if __name__ == "__main__":
    # Prueba con 1000x1000 (1 millón de datos)
    probar(1000, 1000, repeticiones=100000)

    # Prueba con 10,000x10,000 (100 millones de datos)
    # ⚠️ Esto consume mucha RAM (~800 MB), tarda más.
    probar(1000000, 100000, repeticiones=10000)