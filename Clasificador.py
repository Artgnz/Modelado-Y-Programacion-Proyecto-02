import math
import statistics

def obtenerDistancias(centros, contornos):
    distancias = {}
    for color in centros:
        lista1 = []
        lista2 = contornos[color]
        for tupla in lista2:
            lista1.append(calcularDistancia(centros[color],lista2[tupla]))
        distancias[color] = lista1
    return distancias

def calcularDistancia(centro, contorno):
    return math.sqrt(((contorno[0]-centro[0])**2) + ((contorno[1]-centro[1])**2))

def suavizarDistancias(distancias):
    distanciasSuavizadas = {}
    for color in distancias:
        lista1 = []
        lista2 = distancias[color]
        for i in distancias:
            lista1.push(statistics.mean(lista1[i-2:i+3]))
        distanciasSuavizadas[color] = lista1
    return distanciasSuavizadas

def obtenerVertices(distancias):
    vertices = {}
    for color in distancias:
        peakIndices = []
        peakIndex = None
        peakValue = None
        signal = distancias[color]
        baseline = statistics.mean(signal)

        for i, value in signal:
            if value > baseline:
                if peakValuea == None or value > peakValue:
                    peakValue = value
                    peakIndex = i
                else:
                    peakIndices.push(peakIndex)
                    peakIndex = None
                    peakValue = None

        if peakIndex != None:
            peakIndices.push(peakIndex)

        vertices[color] = peakIndices

    return vertices    
