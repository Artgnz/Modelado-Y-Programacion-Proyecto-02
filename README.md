# Modelado-y-Programación-Proyecto-01
Identificador de Figuras AAA es un proyecto hecho en python que permite identificar y clasificar figuras geométricas presentes en una imágen de tipo bmp

## Integrantes
    1. González Peñaloza Arturo
    2. Main Cerezo Asahel Said
    3. Raudry Rico Emilio Arsenio
    
## Prerequisitos
1. Contar con sistema operativo Linux, Mac OS o Windows.
2. [Instalar Python v.3.9](https://www.python.org/downloads/) de acuerdo al sistema operativo que use. 
Para verificar la versión usada, ejecute:
```bash
    python3 --version
``` 
3. Instalar [pip](https://pip.pypa.io/en/stable/installation) si es que no se cuenta con él en el entorno de Python usado. Utilizar el siguiente comando:
```bash
    python -m ensurepip --upgrade
``` 
4. Instalar la biblioteca [opencv](https://pypi.org/project/opencv-python/) con el siguiente comando:
```bash
    pip install opencv-python
``` 

## Instalación
Clone el repositorio:
```bash
    git clone https://github.com/Artgnz/Modelado-Y-Programacion-Proyecto-02.git
```
## Uso
Primero, colóquese en el directorio donde se encuentra este README, por ejemplo,
```bash
    cd Modelado-y-Programacion-Proyecto-02
```
Para ejecutar el programa:
```bash
    python3 main.py [ruta_de_imagen]
```
Ejemplo:
```bash
    python3 main.py imágenes/example_1.bmp
```

## Pruebas
    
1. Ejecutar el comando: 
```bash
    python3 clasificador/test_clasificador.py
```
También se puede utilizar el comando:
```bash
    pytest clasificador/test_clasificador.py
```

## Uso de bibliotecas externas.
1. opencv
La biblioteca opencv la usamos para leer la imagen que recibimos. De esta biblioteca usamos los siguientes métodos:
```
    imread(ruta)
```
que carga una imagen desde el archivo especificado y la regresa
```
cvtColor(im, cv2.COLOR_BGR2RGB)
```
para convertir la imagen de un espacio de color a otro, cambiamos de BGR a RGB
