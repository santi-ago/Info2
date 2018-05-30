# -*- coding: utf-8 -*-
"""
@autores: Santiago Gutierrez Perez y Laura Cristina Toro Betancur

El archivo .py puede estar en cualquier carpeta, pero junto al archivo .py debe existir una carpeta
llamada "controles" que es donde estan los archivos .MAT que se cargaran en el script.

Se recomienda que las graficas las muestre en IPython porque si genera la grafica en una ventana aparte
tengra problemas y se puede bloquear debido a que matplotlib no grafica bien cuando esta en ciclos.
"""

#libreria de manejo de arreglos de grandes dimensiones (a diferencia de las listas basicas de python)
import numpy as np
# libreria para hacer graficos tipos matlab (pyplot)
import matplotlib.pyplot as plt
#soporta la carga de multiples tipos de archivos como .MAT
import scipy.io as sio
#libreria con rutinas de PDS
import scipy.signal as signal;

#Adquiere la ruta donde esta el archivo .py y guarda los archivos que terminen
#en .MAT ubicados en la carpeta "Controles" en una variable llamada registros.

def seleccion_registro(path):
    file = sio.loadmat(path) #Carga el archivo seleccionado por el usuario
    registro = file['data'] #Accede a los datos del archivo cargado
    return registro #Devuelve el archivo cargado y el nombre del registro.


def seleccion_canal(registro, canal):
    canal = canal-1
    canal_1 = registro[canal,:,:] #Selecciona el canal elegido por el usuario
    canal_continuo = np.reshape(canal_1,canal_1.shape[0]*canal_1.shape[1],order='F') #Vuelve el canal continuo
    return canal_continuo #Devuelve el canal continuo 

#Funcion para calcular datos de la correlacion
def correlacion(registro, canal_1, canal_2): 
    correlacion = signal.correlate(canal_1, canal_2, mode ='full') #Se usa la libreria scipy porque numpy estaba tardando mucho tiempo haciendo el calculo.
    return correlacion#Devuelve la correlacion y los numeros de los canales correspondientes

#Funcion para graficar Histograma
def histograma(canal_continuo): #Recibe el canal continuo, el nombre del registro y el numero del canal para realizar la grafica.
    nbins='auto' #'auto' permite que matplotlib decida la mejor distribucion para los nbins
    n,bins,p=plt.hist(canal_continuo,nbins,facecolor='m',alpha=0.8 )

#Se calculan los datos necesario para graficar el segmento
def segmento(canal_continuo, valor_min, valor_max):
    tiempo=np.arange(valor_min,valor_max, dtype = 'float') #Crea un arreglo entre el valor minimo y el valor maximo de tipo flotante
    intervalo=canal_continuo[valor_min:valor_max]#Selecciona el intervalo usando los datos ingresador por el usuario
    return tiempo, intervalo, valor_max, valor_min #Devuelve los valores necesarios para graficar el segmento fuera de la funcion.

#Funcion para calcular los valores necesarios para graficar el periodograma de Welch
def periodograma(canal_continuo, ventanas):
    win = signal.hamming(ventanas,True) #Se usa la funcion signal.hamming para suavizar la ventana.
    f_s = 1000 #Valor constante para los datos requeridos por la funcion signal.welch
    f, Pxx = signal.welch(canal_continuo, f_s, window=win, nfft=ventanas, return_onesided=True) #signal.welch se encarga de devolver los datos necesarios para graficar el periodograma usando los valores ingresados
    return f[f<50],Pxx[f<50] #Se devuelven los valores filtrados para que al momento de graficar se vean mejor.
