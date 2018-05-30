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
# Libreria para leer rutas y archivos en el sistema operativo
import os
#soporta la carga de multiples tipos de archivos como .MAT
import scipy.io as sio
#libreria con rutinas de PDS
import scipy.signal as signal;

#Adquiere la ruta donde esta el archivo .py y guarda los archivos que terminen
#en .MAT ubicados en la carpeta "Controles" en una variable llamada registros.

path = os.getcwd() + '\\controles'
files = os.listdir(path)
error = '\nIngreso un valor incorrecto, intentelo de nuevo.\n' #Error generico para valores incorrectos.
registros = []
for file in files:
    if file.endswith(".mat"):
        registros.append(file)


def seleccion_registro(path):

    file = sio.loadmat(path) #Carga el archivo seleccionado por el usuario
    registro = file['data'] #Accede a los datos del archivo cargado
    return registro #Devuelve el archivo cargado y el nombre del registro.

def seleccion_canal(registro):
    while True:
        try:
            x = int(input('El registro tiene {} canales, seleccione uno: '.format(registro.shape[0]))) #Muestra el numero de canales que tiene el registro y pide al usuario seleccionar uno
            if x in range(1, registro.shape[0]+1): # Valida que el canal este en el rango correcto de canales disponibles
                canal_1 = registro[x-1,:,:] #Selecciona el canal elegido por el usuario
                canal_continuo = np.reshape(canal_1,canal_1.shape[0]*canal_1.shape[1],order='F') #Vuelve el canal continuo
                return canal_continuo, x #Devuelve el canal continuo y el numero que hace referencia al canal elegido
            else:
                print('El valor ingresado no corresponde a ningun canal.\nIntentelo de nuevo.')
        except:
            print(error)

#Funcion para calcular datos de la correlacion
def correlacion(registro): 
    print('Primer canal.')
    canal_1, x1 = seleccion_canal(registro) #llama a la funcion y esta garantiza que el canal sea entregado de manera correcta
    print('Segundo canal.')
    canal_2, x2 = seleccion_canal(registro)
    correlacion = signal.correlate(canal_1, canal_2, mode ='full') #Se usa la libreria scipy porque numpy estaba tardando mucho tiempo haciendo el calculo.
    return correlacion, x1, x2 #Devuelve la correlacion y los numeros de los canales correspondientes


#Funcion para graficar Histograma
def histograma(canal_continuo, nreg, ncan): #Recibe el canal continuo, el nombre del registro y el numero del canal para realizar la grafica.
    media=np.mean(canal_continuo)
    nbins='auto' #'auto' permite que matplotlib decida la mejor distribucion para los nbins
    desviacion=np.std(canal_continuo)
    x= media + desviacion*(canal_continuo) 
    n,bins,p=plt.hist(x,nbins,facecolor='m',alpha=0.8 )
    #Se le da formato a la grafica del periodograma.
    plt.grid(True) 
    plt.xlabel ('valores') 
    plt.ylabel ('numero de muestras') 
    plt.title('Histograma del registro: {}, canal: {}'.format(nreg, ncan)) #Se adiciona al titulo el nombre del archivo analizado y el canal seleccionado.
    plt.show()

#Esta funcion permite calcular el promedio , el maximo y minimo valor del canal seleccionado por el usuario  
def prome_max_min(canal_continuo, ncan, nreg):
    print('Valores del registro {}, canal {}'.format(ncan, nreg))
    prom = np.sum(canal_continuo)/float(len(canal_continuo)) #Se calcula el promedio del canal
    print('\nEl promedio es: ' + str(prom))
    maxi = np.max(canal_continuo)#Se encuentra el maximo del canal
    print('El valor maximo es :' + str(maxi))
    minimo=np.min(canal_continuo)#Se encuentra el minimo del canal
    print('El valor minimo es :' + str(minimo))

#Se calculan los datos necesario para graficar el segmento
def segmento(canal_continuo):
    print('El canal tiene {} numero datos'.format(canal_continuo.shape[0])) #Muestra al usuario la cantidad de datos que tiene el canal
    while True: #Valida el primer valor entre 0 y el valor de datos del canal
        try:
            valor_min=int(input('ingrese el primer valor del intervalo: '))
            if valor_min >= 0 and valor_min in range(0,canal_continuo.shape[0]+1):
                break
            else:
                print('Ingreso un valor incorrecto.')
        except:
            print(error)
    while True: #Valida el ultimo valor entre el valor minimo escogido antes y el el valor de datos del canal
        try:
            valor_max=int(input('ingrese el ultimo valor del intervalo: '))
            if valor_max in range(valor_min + 1, canal_continuo.shape[0]+1):
                break
            else:
                print('Ingreso un valor incorrecto.')
        except:
            print(error)
    tiempo=np.arange(valor_min,valor_max, dtype = 'float') #Crea un arreglo entre el valor minimo y el valor maximo de tipo flotante
    intervalo=canal_continuo[valor_min:valor_max]#Selecciona el intervalo usando los datos ingresador por el usuario
    return tiempo, intervalo, valor_max, valor_min #Devuelve los valores necesarios para graficar el segmento fuera de la funcion.

#Funcion para calcular los valores necesarios para graficar el periodograma de Welch
def periodograma(canal_continuo):
    while True: #Valida que la opcion del usuario sea correcta.
        try:
            ventanas = int(input('Ingrese el numero de ventanas: '))
            if ventanas in range(0, canal_continuo.shape[0]): #La ventana no debe ser mayor que el numero de valores en el canal.
                break
            else:pus
                print('Ingreso un valor incorrecto para la ventana.\nIntentelo de nuevo.\n')
        except:
            print(error)
    win = signal.hamming(ventanas,True) #Se usa la funcion signal.hamming para suavizar la ventana.
    f_s = 1000 #Valor constante para los datos requeridos por la funcion signal.welch
    f, Pxx = signal.welch(canal_continuo, f_s, window=win, nfft=ventanas, return_onesided=True) #signal.welch se encarga de devolver los datos necesarios para graficar el periodograma usando los valores ingresados
    return f[f<50],Pxx[f<50] #Se devuelven los valores filtrados para que al momento de graficar se vean mejor.

while True: #Ciclo principal para garantizar que no se salga del programa a menos que el usuario escoja la opcion correcta.
    try: #Captura errores
        print('\n\nMenu principal.')
        print('(1) - Seleccionar un registro EGG.\n(2) - Salir')
        opcion_1 = int(input('\nSeleccione una opcion: '))
        if opcion_1 == 1:
            registro, nreg = seleccion_registro() #Guarda el registro y el nombre del registro seleccionado
            while True:
                try:
                    print('\nUsted selecciono el regsitro: {}\n'.format(nreg)) #Muestra nombre del registro seleccionado
                    print('registro de EEG.\n')
                    print('(1) - Analizar un canal del registro\n(2) - Graficar la correlacion entre dos canales del registro\n(3) - Volver al menu anterior.')    
                    opcion_2 = int(input('\nSeleccione una opcion: '))
                    if opcion_2 == 1:
                        canal, ncan = seleccion_canal(registro) #Guarda el canal y el nombre del canal seleccionado
                        while True:
                            print('\nUsted selecciono el canal: {} del registro {}\n'.format(ncan, nreg))
                            try:
                                print('(1) - Graficar un segmento de tiempo.\n(2) - Graficar un periodograma de Welch del canal\n(3) - Graficar el histograma de un canal\n(4) - Calcular el valor promedio, máximo, mínimo de un canal\n(5) - Volver al menu anterior')
                                opcion_3 = int(input('\nSeleccione una opcion: '))
                                if opcion_3 == 1:
                                    tiempo, intervalo, valor_max, valor_min = segmento(canal) #Guarda los valores que devuelve la funcion
                                    #Grafica el segmento de tiempo usando los valores arrojados por la funcion
                                    plt.grid(True)
                                    plt.xlabel('Intervalo')
                                    plt.title('Registro: {}, canal: {}. Segmento entre {} y {}'.format(nreg, ncan, valor_min, valor_max)) #Muestra en el titulo los datos del registro, canal, valor minimo y valor maximo
                                    plt.ylabel('Tiempo')
                                    plt.plot(tiempo,intervalo, 'g')
                                    plt.show()
                                elif opcion_3 == 2:
                                    periodo, frecuencias = periodograma(canal) #Guarda los valores que devuelve la funcion
                                    #Se grafica el periodograma usando los valores arrojados por la funcion
                                    plt.grid(True)
                                    plt.plot(periodo, frecuencias)
                                    plt.title('Periodograma del registro: {}, canal: {}'.format(nreg, ncan))
                                    plt.show()
                                elif opcion_3 == 3:
                                    histograma(canal, nreg, ncan) #Se le envia a la funcion el nombre del registro y el canal para que pueda graficar y poner el titulo de manera correcta
                                elif opcion_3 == 4:
                                    prome_max_min(canal, nreg, ncan) #se envian los datos a la funcion para realizar los calculos
                                elif opcion_3 == 5:
                                    break #Sale del menu actual y vuelve al anterior
                                else:
                                    print(error)
                            except:
                                print(error)
                    elif opcion_2 == 2:
                        corr, x1, x2 = correlacion(registro) #Guarda los valores que devuelve la funcion
                        #Grafica la correlacion entre los 2 canales seleccionados por el usuario
                        plt.grid(True)
                        plt.title('Correlacion entre el canal {} y el canal {} del registro {}'.format(x1, x2, nreg))
                        plt.plot(corr)
                        plt.show()
                    elif opcion_2 ==3:
                        break#Sale del menu actual y vuelve al anterior
                    else:
                        print(error)
                except:
                    print(error)                     
        elif opcion_1 == 2:
            print('Saliendo del programa.')
            break #Termina el ciclo principal y cierra el script
        else:
            print('Ingreso una opcion invalida.')
    except:
        print(error)        
