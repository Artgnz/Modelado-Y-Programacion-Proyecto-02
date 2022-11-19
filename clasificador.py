import cv2

class Clasificador:

    @staticmethod
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
