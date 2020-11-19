import numpy as np
import scipy.special
import random as r
from functools import reduce
#import matplotlib.pyplot as plt


# Definicion de la clase Red Neuronal
class neuralNetwork:

    # Inicializar
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # Asignar numero de nodos en cada capa de entrada, capa oculta y capa de salida
        self.inputNodes = inputnodes
        self.hiddenNodes = hiddennodes
        self.outputNodes = outputnodes

        # matrices de uniones con pesos: weightsInput_Hidden y weightsHidden_Output... se aplica distribución normal
        self.weightsInput_Hidden = np.random.normal(0.0, pow(self.hiddenNodes,-0.5), (self.hiddenNodes, self.inputNodes))
        self.weightsHidden_Output = np.random.normal(0.0, pow(self.outputNodes,-0.5), (self.outputNodes, self.hiddenNodes))

        # Tasa de aprendizaje
        self.learningRate = learningrate

        # Funcion de activación sigmoidal
        self.activationFunction = lambda x: scipy.special.expit(x)
        pass

    # Entrenar red neuronal
    def train(self, inputs_list, targets_list):
        # DIMENSIONAR LISTA DE INPUTS
        # Convertir lista de inputs a un arreglo de 2 dimensiones
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # FLUJO HACIA HIDDEN LAYER
        # Calcular señales hacia capa oculta
        hidden_inputs = np.dot(self.weightsInput_Hidden, inputs)
        # Calcular las señales emergentes de la capa oculta
        hidden_outputs = self.activationFunction(hidden_inputs)

        # FLUJO HACIA OUTPUT LAYER
        # Calcular señales hacia capa de salida
        final_inputs = np.dot(self.weightsHidden_Output, hidden_outputs)
        # Calcular las señales emergentes de la capa de salida
        final_outputs = self.activationFunction(final_inputs)

        # CALCULO DEL ERROR EN OUTPUT LAYER
        # (target - actual)
        output_errors = targets - final_outputs
        # CALCULO DEL ERROR EN HIDDEN LAYER
        # output_errors se dividen por sus pesos y son recombinados en los NODOS de HIDDEN LAYER
        hidden_errors = np.dot(self.weightsHidden_Output.T, output_errors)

        #ACTUALIZAR PESOS
        # Actualizar los pesos para las aristas entre HIDDEN LAYER y OUTPUT LAYER
        self.weightsHidden_Output += self.learningRate * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        # Actualizar los pesos de las aristas entre INPUT LAYER y HIDDEN LAYER
        self.weightsInput_Hidden += self.learningRate * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))
        pass

    # dar una respuesta de los nodos de salida después de recibir una entrada
    def query(self, inputs_list):
        # DIMENSIONAR LISTA DE INPUTS
        # Convertir lista de inputs a un arreglo de 2 dimensiones

        inputs = np.array(inputs_list, ndmin=2).T

        # FLUJO HACIA HIDDEN LAYER
        # Calcular señales hacia capa oculta
        hidden_inputs = np.dot(self.weightsInput_Hidden, inputs)
        # Calcular las señales emergentes de la capa oculta
        hidden_outputs = self.activationFunction(hidden_inputs)

        # FLUJO HACIA OUTPUT LAYER
        # Calcular señales hacia capa de salida
        final_inputs = np.dot(self.weightsHidden_Output, hidden_outputs)
        # Calcular las señales emergentes de la capa de salida
        final_outputs = self.activationFunction(final_inputs)


        return final_outputs


# Evaluar rendimiento de la red neuronal
def rendimiento(data_list, info=False):
    scorecard = []
    for record in data_list:
        all_values = record
        correct_label = int(all_values[0])
        #print(record[1:], "representa a un acorde del tipo: ", correct_label)
        outputs = n.query((np.asfarray(record[1:]) / 1 * 0.99) + 0.01)
        label = np.argmax(outputs)

        '''
        print("acorde intervalos: ", record)
        for i in range(len(outputs)):
            print("tgt:", i, " ", outputs[i])
        print("Respuesta correcta: ", correct_label)
        print("Respuesta de la red: ",label)
        print()
        '''

        if (label == correct_label):
            scorecard.append(1)
        else:
            scorecard.append(0)
    scorecard_array = np.asarray(scorecard)
    if info == True:
        print("tamaño dataset: ", len(data_list))
        print("Score Card", scorecard)
        print("Performance: ", scorecard_array.sum() / scorecard_array.size)
    return (scorecard_array.sum() / scorecard_array.size)

# Funcion para clasificar un acorde
def predecirAcorde(inputs, info=False):
    prediction = (n.query(inputs)  / 1 * 0.99) + 0.01
    if (info == True):
        print("Tipo de acorde: ", chordDictionary[np.argmax(prediction)])
    return prediction


# MANIPULACION DE DATOS

# Funcion para concatenar numeros en string
def numConcat(num1, num2):
    num1 = str(num1)
    num2 = str(num2)
    num1 += num2
    return int(num1)

# Retorna el intervalo generado entre dos notas
def checkIntervalNumber(a, b):
    x = (abs(a - b)) % 12
    return x

# Retorna los intervalos en un acorde
def extraerIntervalos(dataList, info=False):
    intervalList = []

    # print(dataList[l][i])
    a = numConcat(dataList[0], dataList[1])
    b = numConcat(dataList[2], dataList[3])
    c = numConcat(dataList[4], dataList[5])
    d = numConcat(dataList[6], dataList[7])
    # print(a,b,c,d)

    i1 = checkIntervalNumber(a, b)
    i2 = checkIntervalNumber(a, c)
    i3 = checkIntervalNumber(a, d)

    intervalList.append(i1)
    intervalList.append(i2)
    intervalList.append(i3)

    if info == True:
        print(intervalList, '\n')
    return(intervalList)

# Ordena las notas de un acorde de menor a mayor
def sortNotes(progresion):
    #print(progresion)
    progresion_ordenada = []
    for acorde in progresion:
        chord = ''
        notes = []
        for i in range(0, len(acorde)-1, 2):
            x = ''
            x += acorde[i]
            x += acorde[i+1]
            notes.append(x)
        #print(notes)
        notes.sort()
        #print(notes)
        for note in range(len(notes)): chord += notes[note]
        #print(chord)
        progresion_ordenada.append(chord)
    return progresion_ordenada

# Transforma un conjunto de intervalos a una matriz de 36 columnas x 3 filas
def crearMatrizDeIntervalos(patron, indice=False):
    matriz = []
    if indice == True:
        indice = [patron[0]]
        matriz.append(indice)
        for i in range(3):
            aux = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            aux[patron[i+1]] = 1
            matriz.append(aux)
    if indice == False:
        for i in range(3):
            aux = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            aux[patron[i]] = 1
            matriz.append(aux)
    matriz = reduce(lambda x, y: x + y, matriz)
    return matriz

# Retorna una lista con los indices del diccionario de acordes
def examinarProgresion(progresion, info=False):
    global classification
    classification = []
    progresion = sortNotes(progresion)
    clasificacion_acordes = []
    for i in range(len(progresion)):
        aux = extraerIntervalos(progresion[i], info=False)
        prediction = predecirAcorde(crearMatrizDeIntervalos(aux), info=False)
        clasificacion_acordes.append(np.argmax(prediction))
        tipo_acorde = chordDictionary[np.argmax(prediction)]
        classification.append(tipo_acorde)
        if info==True:
            print("clasificacion acorde", i + 1, ":", tipo_acorde)
    return clasificacion_acordes


# ■■■■■■■ DATASET ■■■■■■■
# Dataset para entrenar red neuronal
data_list =[
            [0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [0,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [1,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [1,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [1,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [1,
             0,0,0,0,0,0,0,1,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [1,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [1,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [1,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [1,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
             0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [2,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [2,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [2,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [2,
             0,1,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [2,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [2,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [2,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [2,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [2,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [2,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [3,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [3,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [3,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [3,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [3,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [3,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [3,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [3,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [3,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [3,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [4,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [4,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [4,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [4,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [4,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [4,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [4,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [4,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [4,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0],
            [4,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [5,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [5,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [5,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [5,
             0,0,0,0,0,0,1,0,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [5,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0],
            [5,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [5,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [5,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [6,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [6,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [6,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [6,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [6,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [6,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0],
            [6,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [6,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [6,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [6,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0],
            [7,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [7,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [7,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [7,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [7,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [7,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [8,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [8,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [8,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0],
            [8,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [8,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [9,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0],
            [9,
             0,0,0,0,0,0,0,0,1,0,0,0,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [9,
             1,0,0,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [9,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [9,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0],
            [10,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [10,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [10,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [10,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [10,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [10,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [10,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [11,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [11,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [11,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [11,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [11,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [11,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1],
            [11,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [12,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [12,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [12,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [12,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [12,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [12,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [12,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [12,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,1,0,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [13,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [12, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [13,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [13,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [13,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [13,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [13,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [13,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [14,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [14,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [14,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,1,0,0,0,0,0,0,0],
            [15,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0],
            [15,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0],
            [15,
             0,0,0,0,0,1,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,1,0,0,0,0,0,0,0,0],
            [16,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [16,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [16,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1],
            [16,
             0,0,0,0,1,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [16,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [17,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [17,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,1,0,0,0,0,0],
            [17,
             0,0,0,0,0,0,1,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0],
            [17,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [17,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [18,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,1,0,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [18,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,1,0,0,0,0],
            [18,
             0,0,0,0,0,0,0,0,0,1,0,0,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,0,1],
            [18,
             0,0,0,1,0,0,0,0,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [18,
             0,0,0,0,0,0,0,1,0,0,0,0,
             0,0,0,0,0,0,0,0,0,0,1,0,
             0,0,0,0,0,0,0,0,0,1,0,0],
            [19, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [19, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [19, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [19, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [19, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [19, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
            ]

# Diccionario de acordes
chordDictionary = {
    0: "Tríada Mayor",
    1: "Tríada Menor",
    2: "Mayor 7",
    3: "Menor 7",
    4: "Dominante 7",
    5: "Tríada Disminuida",
    6: "Semi Disminuido",
    7: "Mayor 6",
    8: "Menor 6",
    9: "Tríada Aumentada",
    10: "Dominante 9",
    11: "Mayor 9",
    12: "Menor 9",
    13: "Dominante 11",
    14: "Mayor 11",
    15: "Menor 11",
    16: "Mayor 13",
    17: "Dominante 13",
    18: "Menor 13",
    19: "Incompatible"
}

#  CREAR 1 INSTANCIA DE RED NEURONAL
input_nodes = 36
hidden_nodes = 50
output_nodes = 20
learning_rate = 2
n = neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)

# ENTRENAR RED NEURONAL
epochs = 75
for e in range(epochs):
    # Iterar sobre cada subconjunto en data_list
    for record in range(len(data_list)):
        all_values = data_list[record]
        # Reescalamiento de los inputs
        inputs = (np.asfarray(all_values[1:]) / 1 * 0.99) + 0.01
        # Inicializar target output values
        targets = np.zeros(output_nodes) + 0.01
        # all_values[0] representa el valor objetivo para cada record
        targets[int(all_values[0])] = 0.99
        n.train(inputs,targets)
        pass

# TO DO
# GENERAR PROGRESIONES CON ALGORITMO GENETICO.
# Mientras que los tiempos fuertes y débiles no cumplan con ciertas características -> seguir iterando.
# Si el numero de épocas acabó, reproducir ADN
def generarProgresiones(tamanhoPoblacion):
    # Generacion de poblacion
    dataList = []
    switch = 0
    trigger = [0,0,0,0]
    c = 0
    while switch == 0 or tamanhoPoblacion != 0:
        c += 1
        #print("Counter", c)
        data = []
        for i in range(0, 4, 1):
            chord = ''
            notes_numbers = []
            notes = []
            for j in range(0, 4, 1):
                notesSet = set(notes_numbers)
                if j == 0:
                    x = r.randint(48, 72)
                if j > 0:
                    x = r.randint(48, 72)
                    # Que no existan notas repetidas en un acorde
                    while x in notesSet:
                        x = r.randint(48, 72)
                notes_numbers.append(x)
                x = str(x)
                notes.append(x)
            notes.sort()
            #print("notas en acorde: ", notes)
            for note in range(len(notes)): chord += notes[note]
            data.append(chord)
        clasificacion = examinarProgresion(data, info=False)
        trigger = geneticQuery(clasificacion)
        if trigger == [1,1,1,1]:
            dataList.append(data)
            switch = 1
            tamanhoPoblacion -= 1
            print("clasificacion", clasificacion, '\n', classification)
            print(data, '\n\n')
    return dataList

def geneticQuery(clasificacion):

   # print(clasificacion)
    trigger = [0,0,0,0]
    if clasificacion[0] == 12 or clasificacion[0] == 3:
        trigger[0] = 1
    if clasificacion[1] == 12:
        trigger[1] = 1
    if clasificacion[2] == 13 or clasificacion[2] == 10:
        trigger[2] = 1
    if clasificacion[3] == 12 or clasificacion[3] ==  2 or clasificacion[3] == 3:
        trigger[3] = 1
    #print("TRIGGER:",trigger)
    return trigger

    pass



# Obtener Rendimiento
print("Performance: ", rendimiento(data_list), '\n')

'''
# Pruebas de clasificación sobre red neuronal
progresion = ['57646254', '57646457', '49586553', '54616350']
clasificacion = examinarProgresion(progresion, info=True)
print(clasificacion)
'''
'''
for l in range(len(dataList)):
    print("DNA ", l)
    for j in range(len(dataList[l])):
        print("chord ", j+1, ":", dataList[l][j])
        chord = dataList[l][j]
        extraerIntervalos(chord)
'''



size = 5
generacion = generarProgresiones(size)
#print(generacion)

for prog in generacion:
    #print(prog)
    clasificacion = examinarProgresion(prog, info=False)
    #print(clasificacion)

'''
examinar = [['48636972', '52536072', '48495967', '54556170']]

for prog in examinar:
    #print(prog)
    clasificacion = examinarProgresion(prog, info=False)
    for j in range(len(prog)):
        #print("chord ", j + 1, ":", prog[j])
        chord = prog[j]
        #print(extraerIntervalos(chord))
    #print(clasificacion)
'''
print("Performance: ", rendimiento(data_list), '\n')


# Generar matrices para tomar nota manualmente e ingresar al dataset. Son combinaciones de notas
'''
for i in procesar:
    #print(i)
    print(crearMatrizDeIntervalos(i, indice=True))
'''

