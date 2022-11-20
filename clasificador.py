import cv2
import math
from statistics import mean

class Clasificador:

    @staticmethod
    def obtenerDistancias(centros, contornos):
        distancias = {}
        for color in centros:
            distanciasColor = []
            listaContornos = contornos[color]
            for tupla in listaContornos:
                distanciasColor.append(calcularDistancia(centros[color],listaContornos[tupla]))
            distancias[color] = distanciasColor
        return distancias

    @staticmethod
    def calcularDistancia(centro, contorno):
        return math.sqrt(((contorno[0]-centro[0])**2) + ((contorno[1]-centro[1])**2))

    @staticmethod
    def suavizarDistancias(distancias):
        distanciasSuavizadas = {}
        for color in distancias:
            distanciasSuavizadasColor = []
            listaDistancias = distancias[color]
            for i in listaDistancias:
                distanciasSuavizadasColor.push(statistics.mean(listaDistancias[i-2:i+3]))
                distanciasSuavizadas[color] = distanciasSuavizadasColor
        return distanciasSuavizadas

    @staticmethod
    def obtenerVertices(distancias):
        vertices = {}
        for color in distancias:
            indicesCresta = []
            indiceCresta = None
            valorCresta = None
            listaDistancias = distancias[color]
            promedio = statistics.mean(listaDistancias)
            for i, valor in listaDistancias:
                if valor > promedio:
                    if valorCresta == None or valor > valorCresta:
                        valorCresta = valor
                        indiceCresta = i
                    elif valor < valorCresta and valorCresta != None:
                        indicesCresta.push(indiceCresta)
                        indiceCresta = None
                        valorCresta = None
            if indiceCresta != None:
                indicesCresta.push(indiceCresta)
            vertices[color] = len(indicesCresta)
        return vertices    

    @staticmethod
    def clasificar(vertices):
        clasificacion = {}
        for color in vertices:
            if vertices[color]==3:
                clasificacion[color] = 'T'
            if vertices[color]==4:
                clasificacion[color] = 'C'
            if 5<=vertices[color]<=8:
                clasificacion[color] = 'X'
            if vertices[color]==0 or vertices[color]>8:
                clasificacion[color] = 'O'
        return clasificacion

    def __obtenerCentros(imagen):
        sumaCoordenadas = {}
        cantidadCoordenadas = {}
        colorFondo = imagen[0][0]
        for fila in range(len(imagen)):
            for col in range(len(imagen[fila])):
                color = tuple(imagen[fila][col])
                if (color != colorFondo).any():
                    viejaSuma = sumaCoordenadas.get(color, [0,0])
                    sumaCoordenadas[color] = [viejaSuma[0] + fila, viejaSuma[1] + col]
                    cantidadCoordenadas[color] = cantidadCoordenadas.get(color, 0) + 1
        return Clasificador.__promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas)

    @staticmethod
    def __promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas):
        promedios = {}
        for (color, coordenadas) in sumaCoordenadas.items():
            promedioX = round(coordenadas[0] / cantidadCoordenadas[color])
            promedioY = round(coordenadas[1] / cantidadCoordenadas[color])
            promedios[color] = [promedioX, promedioY]
        return promedios

    @staticmethod
    def __obtenerDistanciaContornos(im, centros):
        """
        Regresa un diccionario que contiene las distancias desde el centro de cada figura
        hasta cada punto de su contorno

        Parámetros
        ----------
            im: bitmap
                la imagen en la cual se buscan los contornos
            centros: diccionario
                contiene las coordenadas de los centros de cada figura
        
        Returns
        -------
            distancias: diccionario
                contiene las distancias desde el centro de cada figura
                hasta cada punto de su contorno
        """
        distancias = {}
        for (r,g,b) in centros:
            centro = centros.get((r,g,b), [])
            distancias[(r,g,b)] = Clasificador.__dda(im, centro)
        return distancias

    @staticmethod
    def __dda(im, centro):
        """
        Dado el centro de una figura calcula la distancia hasta cada uno de sus pixeles que conforman su contorno

        Parámetros
        ----------
            im: bitmap
                la imagen en la cual se encuentra la figura
            centro: lista
                contiene las coordenadas del centro de la figura
        
        Returns
        -------
            distancias: lista
                contiene las distancias desde cada uno de los pixeles del contorno hasta el centro de la figura
        """

        x = centro[0]
        y = centro[1]
        
        angulo = 0
        h = 10
        distancias = []
        while(angulo < 2*math.pi):
            xf = x + (h * math.cos(angulo))
            yf = y + (h * math.sin(angulo))
        
            dx = xf - x
            dy = yf - y
            
            pasos = max(abs(dx), abs(dy))
            distancia = 0
            llegue = False
            xa = x
            ya = y
            while(llegue == False):
                xa = xa + (dy/pasos)
                ya = ya + (dx/pasos)
                distancia = distancia + 1

                if (xa < 0) | (xa > len(im)-1) | (ya < 0) | (ya > len(im[0])-1):
                    llegue = True
                    angulo = angulo + math.pi/360
                    distancias.append(distancia)

                elif((im[round(xa)][round(ya)] != im[x][y]).any()):
                    llegue = True
                    angulo = angulo + math.pi/360
                    distancias.append(distancia)
            
        return distancias