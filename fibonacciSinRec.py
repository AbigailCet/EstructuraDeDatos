#Fibonacci sin recursividad
def fibonacci(n:int)->int:
    primer_valor, segundo_valor=0,1
    for _ in range(n):
        primer_valor, segundo_valor=segundo_valor,primer_valor+segundo_valor
    return primer_valor

for i in range(11):
    print(fibonacci(i))
#No tiene recursividad por que no se llama a si misma