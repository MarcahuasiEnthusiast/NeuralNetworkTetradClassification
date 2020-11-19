import numpy as np
from functools import reduce
import operator

patron1 = [2,4,11]
matriz = []

for i in range(len(patron1)):
    aux = [0,0,0,0,0,0,0,0,0,0,0,0]
    aux[patron1[i]] = 1
    print(aux)
    matriz.append(aux)

matriz = reduce(lambda x,y: x+y, matriz)
print(matriz)