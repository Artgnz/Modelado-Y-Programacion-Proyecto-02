import cv2
import math
from statistics import mean

class Clasificador:
    """
    Clase que clasifica las figuras presentes en imágenes.
    """

    @staticmethod
    def __reordenarDistanciasDesdeMin(distanciasFiguras):
        """
        Reordena las distancias de cada figura de tal forma que la distancia mínima esté al
        inicio y se preserve el orden, rota las distancias.

        Parámetros
        ----------
        distanciasFiguras (dict): contiene las distancias asociadas a cada figura.

        Returns
        ----------
        distanciasOrdenadas (dict): contiene las distancias asociadas a cada figura de tal
                                    forma que la distancia mínima esté al inicio.
        """
        distanciasOrdenadas = {}
        for (color, distancias) in distanciasFiguras.items():
            minimo, id = min((minimo, id) for (id, minimo) in enumerate(distancias))
            distanciasOrdenadas[color] = distancias[id:] + distancias[:id]
        return  distanciasOrdenadas

    @staticmethod
    def __suavizarDistancias(distancias):
        """
        Suaviza las distancias de cada figura.

        Parámetros
        ----------
        distancias (dict): contiene las distancias asociadas a cada figura.

        Returns
        ----------
        distanciasSuavizadas (dict): contiene las distancias suavizadas asociadas
                                     a cada figura.
        """
        # tamanoVentanaInferior = 12
        tamanoVentanaInferior = 8
        # tamanoVentanaSuperior = 7
        tamanoVentanaSuperior = 4
        distanciasSuavizadas = {}
        for color in distancias:
            distanciasColor = distancias[color]
            distanciasSuavizadasColor = []
            mitadSuperior = Clasificador.__suavizarArribaDePromedio(distanciasColor, tamanoVentanaSuperior)
            mitadInferior = Clasificador.__suavizarAbajoDePromedio(distanciasColor, tamanoVentanaInferior)
            for i in range(len(distanciasColor)):
                if distanciasColor[i] == mitadSuperior[i]:
                    distanciasSuavizadasColor.append(mitadInferior[i])
                else:
                    distanciasSuavizadasColor.append(mitadSuperior[i])
            distanciasSuavizadas[color] = distanciasSuavizadasColor
        return distanciasSuavizadas

    @staticmethod
    def __suavizarArribaDePromedio(distancias, tamanoVentana):
        """
        Suaviza las distancias que tienen un valor mayor o igual al promedio de las
        distancias multiplicado por una constante. Para suavizar las distancias calcula el
        promedio de los tamanoVentana elementos antes y después de la distancia.

        Parámetros
        ----------
        distancias (list): Distancias de la figura.
        tamanoVentana (int): Cantidad de distancias a considerar antes y después de cada
                             distancia.

        Returns
        ----------
        distanciasSuavizadas (int): Contiene las distancias suavizadas.
        """
        distanciasSuavizadas = []
        distanciasExpandidas = distancias[-tamanoVentana:] + distancias + distancias[0:tamanoVentana]
        promedio = mean(distancias)
        promedio *= 1.45
        for i in range(tamanoVentana, len(distancias) + tamanoVentana):
            ventana = distanciasExpandidas[i - tamanoVentana : i + tamanoVentana + 1]
            if distanciasExpandidas[i] >= promedio:
                distancia = mean(ventana)
                distanciasSuavizadas.append(round(distancia,2))
            else:
                distanciasSuavizadas.append(distanciasExpandidas[i])
        return distanciasSuavizadas

    @staticmethod
    def __suavizarAbajoDePromedio(distancias, tamanoVentana):
        """
        Suaviza las distancias que tienen un valor menor al promedio de las distancias
        multiplicado por una constante. Para suavizar las distancias calcula el promedio
        de los tamanoVentana elementos antes y después de la distancia.

        Parámetros
        ----------
        distancias (list): Distancias de la figura.
        tamanoVentana (int): Cantidad de distancias a considerar antes y después de cada
                             distancia.

        Returns
        ----------
        distanciasSuavizadas (int): Contiene las distancias suavizadas.
        """
        distanciasSuavizadas = []
        distanciasExpandidas = distancias[-tamanoVentana:] + distancias + distancias[0:tamanoVentana]
        promedio = mean(distancias)
        promedio *= 1.45
        for i in range(tamanoVentana, len(distancias) + tamanoVentana):
            ventana = distanciasExpandidas[i - tamanoVentana : i + tamanoVentana + 1]
            if distanciasExpandidas[i] < promedio:
                distancia = mean(ventana)
                distanciasSuavizadas.append(round(distancia,2))
            else:
                distanciasSuavizadas.append(distanciasExpandidas[i])
        return distanciasSuavizadas

    @staticmethod
    def __obtenerVertices(distancias):
        """
        Consigue la cantidad de vértices de cada figura.

        Parámetros
        ----------
        distancias (dict): Distancias asociadas a cada figura.

        Returns
        ----------
        vertices (dict): Cantidad de vértices de cada figura.
        """
        vertices = {}
        for color in distancias:
            indicesCresta = []
            indiceCresta = None
            valorCresta = None
            listaDistancias = distancias[color]
            # tamanoVentana = 10
            tamanoVentana = 7
            for i in range(tamanoVentana, len(listaDistancias) - tamanoVentana):
                if (Clasificador.__esPico(i, listaDistancias,tamanoVentana)):
                    # if (not Clasificador.__estaCercaDeCresta(indicesCresta, i, 5)):
                    if (not Clasificador.__estaCercaDeCresta(indicesCresta, i, 3)):
                        indicesCresta.append(i)
            vertices[color] = len(indicesCresta)
        return vertices

    @staticmethod
    def __esPico(indice, distancias, tamanoVentana):
        """
        Determina si distancias[indice] es pico considerando tamanoVentana
        distancias adelante y después de índice y observando que ninguna de
        las distancias consideradas sea mayor que distancias[indice].

        Parámetros
        ----------
        indice (int): Índice de la distancia.
        distancias (list): Lista de distancias.
        tamanoVentana (int): Tamaño de la ventana a considerar.

        Returns
        ----------
        (bool): Si distancias[indice] es pico.
        """
        for i in range(indice - tamanoVentana, indice):
            if (distancias[indice] < distancias[i]):
                return False
        for i in range(indice, indice + tamanoVentana):
            if (distancias[indice] < distancias[i]):
                return False
        return True

    @staticmethod
    def __estaCercaDeCresta(indicesCresta, indice, tamanoVentana):
        """
        Determina si indice está cerca de una cresta considerando
        tamanoVentana de distancia.

        Parámetros
        ----------
        indicesCresta (list): Índices de las crestas
        indice (int): Índice de la distancia.
        tamanoVentana (int): Tamaño de la ventana a considerar.

        Returns
        ----------
        (bool): Si indice está cerca de alguna cresta
        """
        for indiceCresta in indicesCresta:
            if indiceCresta - tamanoVentana  <= indice and indiceCresta + tamanoVentana >= indice:
                return True
        return False

    @staticmethod
    def __clasificar(vertices):
        """
        Asocia los colores de acuerdo a la cantidad de vértices que tienen.

        Parámetros
        ----------
        vertices (dict): cantidad de vértices asociados a cada color.

        Returns
        ----------
        clasificacion (dict): clasificación asociada a cada color
        """
        clasificacion = {}
        for color in vertices:
            if vertices[color]==3:
                clasificacion[color] = 'T'
            elif vertices[color]==4:
                clasificacion[color] = 'C'
            elif 5<=vertices[color]<=8 or 1 <= vertices[color] <= 2:
                clasificacion[color] = 'X'
            else:
                clasificacion[color] = 'O'
        return clasificacion

    @staticmethod
    def __obtenerCentros(imagen):
        """
        Obtiene los centros de las figuras presentes en la imagen.

        Parámetros
        ----------
        imagen (numpy.ndarray): Matriz representando a la imagen.

        Returns
        ----------
        coordenadas (dict): coordenadas de los centros asociadas a cada figura.
        """
        sumaCoordenadas = {}
        cantidadCoordenadas = {}
        colorFondo = imagen[0][0]
        for fila in range(len(imagen)):
            for col in range(len(imagen[fila])):
                color = tuple(imagen[fila][col])
                if (color != colorFondo).any():
                    viejaSuma = sumaCoordenadas.get(color, [0,0])
                    sumaCoordenadas[color] = [viejaSuma[0] + col, viejaSuma[1] + fila]
                    cantidadCoordenadas[color] = cantidadCoordenadas.get(color, 0) + 1
        coordenadas = Clasificador.__promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas)
        return coordenadas

    @staticmethod
    def __promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas):
        """
        Calcula el promedio de las coordenadas asociadas a cada figura.

        Parámetros
        ----------
        sumaCoordenadas (dict): Suma de las coordenadas asociadas a cada figura.
        cantidadCoordenadas (dict): Cantidad de coordenadas asociadas a cada figura.

        Returns
        ----------
        promedios (dict): Promedios de las coordenadas asociadas a cada figura.
        """
        promedios = {}
        for (color, coordenadas) in sumaCoordenadas.items():
            promedioX = coordenadas[0] / cantidadCoordenadas[color]
            promedioY = coordenadas[1] / cantidadCoordenadas[color]
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

        h = 20
        distancias = []
        while(angulo < 2*math.pi):
            xf = x + (h * math.cos(angulo))
            yf = y + (h * math.sin(angulo))

            dx = xf - x
            dy = yf - y

            pasos = max(abs(dx), abs(dy))
            llegue = False
            xa = x
            ya = y
            while(llegue == False):
                xa = xa + (dx/pasos)
                ya = ya + (dy/pasos)
                # Fórmula de distancia entre dos puntos.
                distancia = math.sqrt(((xa-x)**2) + ((ya-y)**2))
                if (ya < 0) | (ya > len(im)-1) | (xa < 0) | (xa > len(im[0])-1):
                    llegue = True
                    angulo = angulo + 2 *math.pi/360
                    distancias.append(distancia)

                elif ((im[round(ya)][round(xa)] != im[round(y)][round(x)]).any()):
                    llegue = True
                    angulo = angulo + 2 * math.pi/360
                    distancias.append(distancia)
        return distancias

    @staticmethod
    def clasificarFiguras(ruta):
        """
        Dada la ruta de una imagen, clasifica las figuras geométricas
        que se encuentran en ella.

        Parámetros
        ----------
        ruta (string): Ruta de la imagen.

        Returns
        ----------
        clasificaciones (dict): Clasificaciones de las figuras presentes en la imagen.
        """
        im = cv2.imread(ruta)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        centros = Clasificador.__obtenerCentros(im)
        distancias = Clasificador.__obtenerDistanciaContornos(im, centros)
        distancias = Clasificador.__reordenarDistanciasDesdeMin(distancias)
        for i in range(2):
            distancias = Clasificador.__suavizarDistancias(distancias)
        vertices = Clasificador.__obtenerVertices(distancias)
        clasificaciones = Clasificador.__clasificar(vertices)
        return clasificaciones
