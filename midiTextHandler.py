
# n=21 es la nota # 1 de un piano
# n=108 es la nota # 88 de un piano, la ultima

texto = open('midi files/csv/music14.txt', 'r')
texto.seek(0)
text = texto.read()
#print(len(text))
text = text.splitlines()

data = []
textSplit = []
timePos = []
tiempoAux = ""
for i in range(len(text)):
    textSplit.append(text[i].split(', '))
    try:
        print(timePos.index(textSplit[i][1]))
    except:
        #print("Añadido a timePos")
        timePos.append(textSplit[i][1])
    if (text[i].rfind("Note_on_c, 0, ") > 5) and tiempoAux != textSplit[i][1]:

        pos = text[i].rfind("Note_on_c, 0, ")
        print("Tiempo :" + textSplit[i][1])
        print("i", i, "nota: " + text[i][pos+14:pos+16])
        print()
        data.append(text[i][pos+14:pos+16])
        tiempoAux = textSplit[i][1]

    else:
        if (text[i].rfind("Note_on_c, 0, ") > 5):
            if data:
                data[timePos.index(textSplit[i][1])] += text[i][pos+14:pos+16]
print()

print("Total de posiciones en el tiempo: ", len(timePos))
print(timePos)
print()

print("# de acordes: ", len(data))
print(data)
print()

stringAcordes = " ".join(data)
print("Cromosoma ideal generado: ", len(stringAcordes))
print(stringAcordes)



















"""
print("Manipulacion Diccionario: ")
auxAcorde = ""
arrayAcordes = []
for i in range(len(data)):
    print(data[i])
    for j in range(0, len(data[i]), 2):
        #print(data[i][j], data[i][j+1])
        aux = data[i][j] + data[i][j+1]
        print(aux)
        #print(notesDictionary[aux])
        print(notesDictionary[aux])
        auxAcorde += notesDictionary[aux]
    print(auxAcorde)
    arrayAcordes.append(auxAcorde+" ")
    auxAcorde = ""
    print()
"""

#print(arrayAcordes)
#stringAcordes = " ".join(arrayAcordes)
#print()
#print(stringAcordes)


#print()
#for x in notesDictionary:
#    print(x)
#    print(x, notesDictionary[x])



