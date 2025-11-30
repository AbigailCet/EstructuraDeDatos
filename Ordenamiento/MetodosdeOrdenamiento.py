def ordenamiento_burbuja(arr):
    """Ordenamiento por burbuja con visualización paso a paso"""
    n = len(arr)
    arr_copia = arr.copy()
    print("\n" + "="*60)
    print("ORDENAMIENTO POR BURBUJA")
    print("="*60)
    print(f"Array inicial: {arr_copia}\n")
    
    paso = 1
    for i in range(n):
        hubo_cambio = False
        for j in range(0, n - i - 1):
            print(f"Paso {paso}:")
            print(f"  Comparando: {arr_copia[j]} y {arr_copia[j+1]}")
            
            if arr_copia[j] > arr_copia[j + 1]:
                print(f"  → {arr_copia[j]} > {arr_copia[j+1]}, intercambiando...")
                arr_copia[j], arr_copia[j + 1] = arr_copia[j + 1], arr_copia[j]
                hubo_cambio = True
                print(f"  Array: {arr_copia}")
            else:
                print(f"  → {arr_copia[j]} <= {arr_copia[j+1]}, no se intercambia")
                print(f"  Array: {arr_copia}")
            
            print()
            paso += 1
        
        if not hubo_cambio:
            print("  ¡Ya está ordenado! No hubo intercambios en esta pasada.\n")
            break
    
    print(f"Array final ordenado: {arr_copia}")
    print("="*60 + "\n")
    return arr_copia


def ordenamiento_insercion(arr):
    """Ordenamiento por inserción con visualización paso a paso"""
    arr_copia = arr.copy()
    print("\n" + "="*60)
    print("ORDENAMIENTO POR INSERCIÓN")
    print("="*60)
    print(f"Array inicial: {arr_copia}\n")
    
    paso = 1
    for i in range(1, len(arr_copia)):
        clave = arr_copia[i]
        j = i - 1
        
        print(f"Paso {paso}:")
        print(f"  Tomando elemento: {clave} (posición {i})")
        print(f"  Array actual: {arr_copia}")
        
        posicion_original = i
        movimientos = []
        
        while j >= 0 and arr_copia[j] > clave:
            arr_copia[j + 1] = arr_copia[j]
            movimientos.append(f"    → Moviendo {arr_copia[j]} de posición {j} a posición {j+1}")
            j -= 1
        
        if movimientos:
            print("  Moviendo elementos mayores:")
            for mov in movimientos:
                print(mov)
        
        arr_copia[j + 1] = clave
        
        if j + 1 != posicion_original:
            print(f"  → Insertando {clave} en posición {j+1}")
        else:
            print(f"  → {clave} ya está en su posición correcta")
        
        print(f"  Array: {arr_copia}")
        print()
        paso += 1
    
    print(f"Array final ordenado: {arr_copia}")
    print("="*60 + "\n")
    return arr_copia


def ordenamiento_seleccion(arr):
    """Ordenamiento por selección con visualización paso a paso"""
    arr_copia = arr.copy()
    print("\n" + "="*60)
    print("ORDENAMIENTO POR SELECCIÓN")
    print("="*60)
    print(f"Array inicial: {arr_copia}\n")
    
    paso = 1
    for i in range(len(arr_copia)):
        min_idx = i
        
        print(f"Paso {paso}:")
        print(f"  Buscando el mínimo desde posición {i}")
        print(f"  Array actual: {arr_copia}")
        
        for j in range(i + 1, len(arr_copia)):
            if arr_copia[j] < arr_copia[min_idx]:
                print(f"    → Nuevo mínimo encontrado: {arr_copia[j]} en posición {j}")
                min_idx = j
        
        if min_idx != i:
            print(f"  Intercambiando {arr_copia[i]} (pos {i}) con {arr_copia[min_idx]} (pos {min_idx})")
            arr_copia[i], arr_copia[min_idx] = arr_copia[min_idx], arr_copia[i]
        else:
            print(f"  {arr_copia[i]} ya está en su posición correcta")
        
        print(f"  Array: {arr_copia}")
        print()
        paso += 1
    
    print(f"Array final ordenado: {arr_copia}")
    print("="*60 + "\n")
    return arr_copia


def main():
    print("\n" + "🔢 "*10)
    print("    PROGRAMA DE ALGORITMOS DE ORDENAMIENTO")
    print("🔢 "*10 + "\n")
    
    # Solicitar números al usuario o generar automáticamente
    print("Opciones de entrada:")
    print("  1. Ingresar números manualmente")
    print("  2. Generar lista de 1000 números aleatorios")
    
    while True:
        opcion_entrada = input("\nTu elección (1-2): ").strip()
        
        if opcion_entrada == '1':
            while True:
                try:
                    entrada = input("Ingresa los números separados por espacios: ")
                    numeros = [int(x) for x in entrada.split()]
                    
                    if len(numeros) < 2:
                        print("⚠️  Por favor ingresa al menos 2 números.\n")
                        continue
                    
                    break
                except ValueError:
                    print("⚠️  Error: Ingresa solo números válidos separados por espacios.\n")
            
            print(f"\nNúmeros ingresados: {numeros}\n")
            break
            
        elif opcion_entrada == '2':
            import random
            numeros = [random.randint(1, 10000) for _ in range(1000)]
            print(f"\n✅ Se generaron 1000 números aleatorios entre 1 y 10000")
            print(f"Primeros 20 números: {numeros[:20]}...")
            print(f"Últimos 20 números: ...{numeros[-20:]}\n")
            break
        else:
            print("⚠️  Opción no válida. Por favor elige 1 o 2.")
    
    while True:
        print("\n" + "-"*60)
        print("Selecciona el algoritmo de ordenamiento:")
        print("  1. Ordenamiento por Burbuja")
        print("  2. Ordenamiento por Inserción")
        print("  3. Ordenamiento por Selección")
        print("  4. Ver los 3 métodos")
        print("  5. Ingresar nuevos números")
        print("  6. Salir")
        print("-"*60)
        
        opcion = input("\nTu elección (1-6): ").strip()
        
        if opcion == '1':
            ordenamiento_burbuja(numeros)
        elif opcion == '2':
            ordenamiento_insercion(numeros)
        elif opcion == '3':
            ordenamiento_seleccion(numeros)
        elif opcion == '4':
            ordenamiento_burbuja(numeros)
            input("Presiona Enter para continuar...")
            ordenamiento_insercion(numeros)
            input("Presiona Enter para continuar...")
            ordenamiento_seleccion(numeros)
        elif opcion == '5':
            while True:
                try:
                    entrada = input("\nIngresa los nuevos números separados por espacios: ")
                    numeros = [int(x) for x in entrada.split()]
                    
                    if len(numeros) < 2:
                        print("⚠️  Por favor ingresa al menos 2 números.")
                        continue
                    
                    print(f"\nNuevos números: {numeros}")
                    break
                except ValueError:
                    print("⚠️  Error: Ingresa solo números válidos.")
        elif opcion == '6':
            print("\n¡Gracias por usar el programa! 👋\n")
            break
        else:
            print("\n⚠️  Opción no válida. Por favor elige entre 1 y 6.")


if __name__ == "__main__":
    main()