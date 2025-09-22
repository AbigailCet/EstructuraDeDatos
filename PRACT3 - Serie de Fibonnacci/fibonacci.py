
#Fibonacci que imprima cada numero de la serie
def fibonaci(n:int)->int:
    if n<=0:
        return 0
    elif n==1:
        return 1
    else:
        return fibonaci(n-1)+fibonaci(n-2)
    

for i in range(11):
    print(fibonaci(i))