import java.util.Scanner;

class Ventas {
    private String [] Departamentos = {"Ropa", "Deportes", "Jugueteria"};
    private String [] Meses = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
    private int [][] MatrizVentas;

    public Ventas() {
        MatrizVentas = new int[Meses.length][Departamentos.length];
    }

    public void ingresarVenta(String mes, String departamento, int monto) {
        int fila = obtenerIndice(Meses, mes);
        int columna = obtenerIndice(Departamentos, departamento);
        if (fila != -1 && columna != -1) {
            MatrizVentas[fila][columna] += monto;
            System.out.println("Venta ingresada: " + monto + " en " + mes + " para " + departamento + ".");
        } else {
            System.out.println("Mes o departamento inválido.");
        }
    }
    public void ingresarVentaDepartamento(String departamento, int monto){
        int columna = obtenerIndice(Departamentos, departamento);
        if (columna != -1) {
            for (int i = 0; i < Meses.length; i++) {
                MatrizVentas[i][columna] += monto;
            }
            System.out.println("Venta ingresada: " + monto + " para todo el año en " + departamento + ".");
        } else {
            System.out.println("Departamento inválido.");
        }
    }
    public void mostrarMatriz() {
        System.out.println("\t" + String.join("\t", Departamentos));
        for (int i = 0; i < MatrizVentas.length; i++) {
            System.out.print(Meses[i] + "\t");
            for (int j = 0; j < MatrizVentas[i].length; j++) {
                System.out.print(MatrizVentas[i][j] + "\t");
            }
            System.out.println();
        }
    }
    private int obtenerIndice(String[] array, String valor) {
        for (int i = 0; i < array.length; i++) {
            if (array[i].equalsIgnoreCase(valor)) {
                return i;
            }
        }
        return -1;
    }

    public void eliminarVenta(String mes, String departamento) {
        int fila = obtenerIndice(Meses, mes);
        int columna = obtenerIndice(Departamentos, departamento);
        if (fila != -1 && columna != -1) {
            MatrizVentas[fila][columna] = 0;
            System.out.println("Venta eliminada en " + mes + " para " + departamento + ".");
        } else {
            System.out.println("Mes o departamento inválido.");
        }
    }
}
public class Main {
    public static void main(String[] args) {
        Ventas ventas = new Ventas();
        Scanner scanner = new Scanner(System.in);
        ventas.ingresarVenta("Enero", "Ropa", 500);
        ventas.ingresarVenta("Febrero", "Deportes", 300);
        ventas.ingresarVenta("Marzo", "Jugueteria", 400);
        ventas.eliminarVenta("Febrero", "Deportes");
        for (int i = 0; i < 12; i++) {
            ventas.ingresarVentaDepartamento("Ropa", scanner.nextInt());
        }
        ventas.mostrarMatriz();
        scanner.close();
    }
}
