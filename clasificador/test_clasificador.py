import unittest
from clasificador import Clasificador
import cv2

class TestClasificador(unittest.TestCase):
    def test__promediarCoordenadas(self):
        """
        Prueba que permite conocer si se pueden promediar las coordenadas correctamente para
        obtener el centro de la figura.
        """
        clasificador = Clasificador()
        sumaCoordenadas = {"(255,255,255)": [1234, 2468], "(0,0,0)": [542, 876]}
        cantidadCoordenadas = {"(255,255,255)": 2, "(0,0,0)": 20}
        promedios = clasificador._Clasificador__promediarCoordenadas(sumaCoordenadas, cantidadCoordenadas)
        esperado = {"(255,255,255)":[617, 1234], "(0,0,0)":[27.1, 43.8]}
        self.assertEqual(promedios, esperado)


    def test__obtenerDistanciaContornos(self):
        """
        Prueba que permite conocer si las distancias del centro de una figura
        a su contorno se calculan correctamente.
        """
        clasificador = Clasificador()
        path = r'imágenes/example_1.bmp'
        im = cv2.imread(path)
        centros = {(78,106,123): [16, 49]}
        distancias = clasificador._Clasificador__obtenerDistanciaContornos(im, centros)
        distancias2 = distancias.get((78,106,123), [])
        distancia = distancias2[0]
        esperado = 11.0
        self.assertEqual(distancia, esperado)
        
    def test_clasificarFiguras(self):
        """
        Prueba que permite conocer si clasifica correctamente las figuras presentes
        en imágenes.
        """
        clasificador = Clasificador()
        tablaDePruebas = {"imágenes/example_1.bmp":{(123, 106, 78): 'C', (200, 165, 102): 'O', (150, 92, 50): 'T'},
                          "imágenes/example_2.bmp":{(94, 205, 43): 'O', (241, 160, 21): 'T', (52, 70, 228): 'T',
                                                    (255, 58, 58): 'T', (34, 165, 241): 'C', (255, 49, 136): 'O',
                                                    (181, 52, 228): 'C'},
                          "imágenes/example_3.bmp":{(251, 242, 54): 'T', (255, 76, 114): 'C', (199, 54, 251): 'C'}}
        for (ruta, esperado) in tablaDePruebas.items():
            obtenido = clasificador.clasificarFiguras(ruta)
            self.assertEqual(esperado,obtenido)
        
if __name__ == "__main__":
    unittest.main()
