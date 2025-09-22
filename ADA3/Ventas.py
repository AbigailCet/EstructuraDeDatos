class Ventas:
    departamentos = ["Mes", "Ropa", "Deportes", "Jugueteria"]
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio","Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    def __init__(self):
        
        self.matriz_ventas = []
        for mes in self.meses:
            fila = [mes] + [0 for _ in range(len(self.departamentos) - 1)]
            self.matriz_ventas.append(fila)

    def ingresar_venta(self,mes,departamento,monto):
        if mes in self.meses and departamento in self.departamentos:
            fila = self.meses.index(mes)
            columna = self.departamentos.index(departamento)
            self.matriz_ventas[fila][columna] += monto
            print(f"Venta ingresada: {monto} en {mes} para {departamento}.")
        else:
            print("Mes o departamento inválido.")

    def insertar_venta_departamento(self, departamento):
        if departamento in self.departamentos:
            columna = self.departamentos.index(departamento)
            for fila in self.matriz_ventas:
                fila[columna] = int(input(f"Ingrese ventas para {fila[0]} en {departamento}: "))
        else:
            print("Departamento inválido.")

    def eliminar_venta_departamento(self, departamento,mes):
        if departamento in self.departamentos and mes in self.meses:
            fila = self.meses.index(mes)
            columna = self.departamentos.index(departamento)
            self.matriz_ventas[fila][columna] = 0
            print(f"Venta eliminada en {mes} para {departamento}.")
        else:
            print("Mes o departamento inválido.")

    def mostrar_matriz(self):
        # Mostrar encabezados
        print("\t".join(f"{dep:<15}" for dep in self.departamentos))
        for fila in self.matriz_ventas:
            print(f"\t".join(f"{x:<15}" for x in fila))


ventas = Ventas()
ventas.mostrar_matriz()
ventas.ingresar_venta("Enero", "Ropa", 1500)
ventas.mostrar_matriz()
#ventas.insertar_venta_departamento("Deportes")
ventas.mostrar_matriz()
ventas.eliminar_venta_departamento("Ropa", "Enero")
ventas.mostrar_matriz()