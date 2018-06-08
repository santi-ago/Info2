#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 09:55:40 2018

@author: aya
"""


from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtGui


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import graficas as gf
import SQLitedb as db
ruta = ''

class Periodograma(QDialog):
    def __init__(self, ruta):
        super(Periodograma, self).__init__()
        loadUi(ruta +'/gui/periodograma.ui', self)
        self.graficar.clicked.connect(self.graficar_periodograma)# se conecta con la funcion graficar_periodograma
        self.cargarRegistro.clicked.connect(self.seleccionar_registro)# se conecta con la funcion seleccionar registro
        self.canal.setValidator(QtGui.QIntValidator(0,8))# valida que el canal sea solo numero y este en ese rango
        self.ventanas.setValidator(QtGui.QIntValidator())
        validar_cedula = QtGui.QIntValidator()# valida que la cedula se solo numeros
        validar_cedula.setBottom(0)# asigna el valor minimo que puede tomar la cedula
        self.Cedula.setValidator(validar_cedula)
        self.__ruta = ''
        self.__ruta_raiz = ruta
        self.__registro = []
        self.__datos=[]
        self.guardar.clicked.connect(self.guardar_datos)# se conecta con la funcion guardar registro
        # a figure instance to plot on
        self.figure = Figure()#
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.plano.addWidget(self.canvas)
        self.show()
    #concta ruta con l,a base de datos para guardar los datos graficados 
    def guardar_datos(self):
        conn = db.conectar(self.__ruta_raiz)
        cedula = self.Cedula.text()
        #valida que no vaya haber ningun dato vacio al momento de guardar
        if self.__registro== [] or self.__ruta =='' or self.canal.text()=='' or self.ventanas.text()=='' or self.Cedula.text()=='':
            QMessageBox.about(self, 'Alerta', 'Faltan datos.')#  crea una ventana emergente
        else:
            existe=db.verificar_paciente(conn, int(cedula))
            if existe==True:
                canal_seleccionado = gf.seleccion_canal(self.__registro, int(self.canal.text()))
                periodo, frecuencias = gf.periodograma(canal_seleccionado, int(self.ventanas.text()))
                self.__datos.append(periodo) #agrega los resultados a una lista
                self.__datos.append(frecuencias)
                data = np.array(self.__datos) #Vuelve la lista en un array de numpy
                db.addGrafica(conn, cedula, 'Periodograma', self.fecha.text(), data)# mete los datos con los que se hace la grafica a la base de datos de resultados
                #ventana emergente para pregunrae si desea graficar otro registro
                buttonReply = QMessageBox.question(self, 'Alerta', "Desea graficar otro registro?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                conn.close()#cierra la base de datos
                if buttonReply == QMessageBox.Yes:
                    # limpia todos los datos para poder ingresar otro usuario
                     self.__registro== []
                     self.canal.setText('')
                     self.ventanas.setText('')
                     self.Cedula.setText('')
                     ax=self.figure.add_subplot(111)
                     ax.clear()
                     self.canvas.draw()
                     
                else:
                      QMessageBox.about(self, 'Alerta', 'Grafica guardada.')
                      self.destroy()
            elif existe==False:
                 QMessageBox.about(self, 'Alerta', 'El paciente no existe ,debe ingresar.')
                
                
     # selecciona la ruta y carga el registro   
    def seleccionar_registro(self):
        self.__ruta = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.__ruta.replace('/', '//')
        self.__registro = gf.seleccion_registro(self.__ruta)
#        file = sio.loadmat(self.__ruta) #Carga el archivo seleccionado por el usuario
#        self.__registro = file['data']
    # grafica el periodograma de un canal seleccionado del registro
    def graficar_periodograma(self):
        canal_seleccionado = gf.seleccion_canal(self.__registro, int(self.canal.text()))# aigna a una variable la selccion canal de la libreria graficas
        periodo, frecuencias = gf.periodograma(canal_seleccionado, int(self.ventanas.text()))
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data

        ax.grid(True)
        ax.plot(periodo, frecuencias)
#        ax.title('Periodograma del registro: {}, canal: {}'.format(nreg, ncan))

        # refresh canvas
        self.canvas.draw()

class Correlacion(QDialog):
    def __init__(self, ruta):
        super(Correlacion, self).__init__()
        loadUi(ruta +'/gui/correlacion.ui', self)
        self.__ruta_raiz = ruta
        self.graficar.clicked.connect(self.graficar_correlacion)# se conecta con la funcion graficar_correlacion
        self.cargarRegistro.clicked.connect(self.seleccionar_registro)# se conecta con la funcion seleccionar_registro
        self.canal_1.setValidator(QtGui.QIntValidator(0,8))
        self.canal_2.setValidator(QtGui.QIntValidator(0,8))
        validar_cedula = QtGui.QIntValidator()# valida que la cedula se solo numeros
        validar_cedula.setBottom(0)# asigna el valor minimo que puede tomar la cedula
        self.cedula.setValidator(validar_cedula)
        self.__ruta = ''
        self.__registro = []
        self.guardar.clicked.connect(self.guardar_datos)
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.plano.addWidget(self.canvas)
        self.show()
    def guardar_datos(self):
         if self.__registro== [] or self.__ruta =='' or self.canal_1.text()=='' or self.canal_2.text()=='' or self.cedula.text()=='':
            QMessageBox.about(self, 'Alerta', 'Faltan datos.')
         else:
             canal1 = gf.seleccion_canal(self.__registro, int(self.canal_1.text()))# aigna a una variable la selccion canal de la libreria graficas
             canal2 = gf.seleccion_canal(self.__registro, int(self.canal_2.text()))
             datos = gf.correlacion(self.__registro, canal1, canal2)# guarda los datos de la correlacion entre los dos canles eljidos
             cedula = self.cedula.text()
             conn = db.conectar(self.__ruta_raiz)#conecta la base de datos con la ruta
             db.addGrafica(conn, cedula, 'Correlacion', self.fecha.text(), datos) #mete los datos con los que se hace la grafica a la base de datos de resultados
             conn.close()
             
             buttonReply = QMessageBox.question(self, 'Alerta', "Desea graficar otro registro?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
             if buttonReply == QMessageBox.Yes:
                 self.__registro== []
                 self.canal_1.setText('')
                 self.canal_2.setText('')
                 self.cedula.setText('')
                 ax=self.figure.add_subplot(111)
                 ax.clear()
                 self.canvas.draw()
             else:
                 QMessageBox.about(self, 'Alerta', 'Grafica guardada.')
                 self.destroy()

                
        
    def seleccionar_registro(self):
        self.__ruta = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.__ruta.replace('/', '//')
        self.__registro = gf.seleccion_registro(self.__ruta)
    #grafica la correlacion entre dos canles de un registro
    def graficar_correlacion(self):
        canal1 = gf.seleccion_canal(self.__registro, int(self.canal_1.text()))
        canal2 = gf.seleccion_canal(self.__registro, int(self.canal_2.text()))
        datos = gf.correlacion(self.__registro, canal1, canal2)
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        ax.grid(True)
        ax.plot(datos)
#        ax.title('Periodograma del registro: {}, canal: {}'.format(nreg, ncan))
        # refresh canvas
        self.canvas.draw()
        
class Histograma(QDialog):
    def __init__(self, ruta):
        super(Histograma, self).__init__()
        loadUi(ruta +'/gui/histograma.ui', self)
        self.__ruta_raiz = ruta
        self.graficar.clicked.connect(self.graficar_histograma)# se conecta con la funcion graficar_histograma
        self.cargarRegistro.clicked.connect(self.seleccionar_registro)# se conecta con la funcion seleccionar_registro
        self.canal.setValidator(QtGui.QIntValidator(0,8))
        validar_cedula = QtGui.QIntValidator()# valida que la cedula se solo numeros
        validar_cedula.setBottom(0)# asigna el valor minimo que puede tomar la cedula
        self.cedula.setValidator(validar_cedula)
        self.__ruta = ''
        self.__registro = []
        self.guardar.clicked.connect(self.guardar_datos)
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.plano.addWidget(self.canvas)
        self.show()
    def guardar_datos(self):
         if self.__registro== [] or self.__ruta =='' or self.canal.text()==''  or self.cedula.text()=='':
            QMessageBox.about(self, 'Alerta', 'Faltan datos.')
         else:
             canal = gf.seleccion_canal(self.__registro, int(self.canal.text()))
             cedula = self.cedula.text()
             conn = db.conectar(self.__ruta_raiz)
             db.addGrafica(conn, cedula, 'Histograma', self.fecha.text(), canal)
             conn.close()
             
             buttonReply = QMessageBox.question(self, 'Alerta', "Desea graficar otro registro?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
             if buttonReply == QMessageBox.Yes:
                 self.__registro== []
                 self.canal.setText('')
                 self.cedula.setText('')
                 ax=self.figure.add_subplot(111)
                 ax.clear()
                 self.canvas.draw()
             else:
                 QMessageBox.about(self, 'Alerta', 'Grafica guardada.')
                 self.destroy()
    
    def seleccionar_registro(self):
        self.__ruta = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.__ruta.replace('/', '//')
        self.__registro = gf.seleccion_registro(self.__ruta)
    #grafica el histograma de un canal de un registro
    def graficar_histograma(self):

        canal = gf.seleccion_canal(self.__registro, int(self.canal.text()))

        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        ax.grid(True)
        nbins = 'auto'
        ax.hist(canal,nbins,facecolor='m',alpha=0.8 )
#        ax.title('Periodograma del registro: {}, canal: {}'.format(nreg, ncan))
        # refresh canvas
        self.canvas.draw()
    
class Segmento(QDialog):
    def __init__(self, ruta):
        super(Segmento, self).__init__()
        loadUi(ruta +'/gui/segmento.ui', self)
        self.__ruta_raiz = ruta
        self.graficar.clicked.connect(self.graficar_segmento)# se conecta con la funcion graficar_segmento
        self.cargarRegistro.clicked.connect(self.seleccionar_registro)
        self.__ruta = ''
        self.__registro = []
        # a figure instance to plot on
        self.figure = Figure()
        self.datos=[]
        self.guardar.clicked.connect(self.guardar_datos)
        self.intervalo_1.setValidator(QtGui.QIntValidator())# valida que esolo
        self.intervalo_2.setValidator(QtGui.QIntValidator())
        self.canal.setValidator(QtGui.QIntValidator(0,8))
        validar_cedula = QtGui.QIntValidator()# valida que la cedula se solo numeros
        validar_cedula.setBottom(0)# asigna el valor minimo que puede tomar la cedula
        self.cedula.setValidator(validar_cedula)
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.plano.addWidget(self.canvas)
        self.show()
    def guardar_datos(self):
         if self.__registro== [] or self.__ruta =='' or self.canal.text()=='' or self.intervalo_1.text()=='' or self.intervalo_2.text()=='' or self.cedula.text()=='':
            QMessageBox.about(self, 'Alerta', 'Faltan datos.')
         else:
            canal = gf.seleccion_canal(self.__registro, int(self.canal.text()))
            tiempo, intervalo = gf.segmento(canal, int(self.intervalo_1.text()), int(self.intervalo_2.text()))
            self.datos.append(tiempo)
            self.datos.append(intervalo)
            cedula = self.cedula.text()
             
            data = np.array(self.datos) #Vuelve la lista en un array de numpy
            conn = db.conectar(self.__ruta_raiz)
            db.addGrafica(conn, cedula, 'Segmento', self.fecha.text(), data)
            conn.close()
            
            buttonReply = QMessageBox.question(self, 'Alerta', "Desea graficar otro registro?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                 self.__registro== []
                 self.canal.setText('')
                 self.intervalo_1.setText('')
                 self.intervalo_2.setText('')
                 self.cedula.setText('')
                 ax=self.figure.add_subplot(111)
                 ax.clear()
                 self.canvas.draw()
            else:
                 QMessageBox.about(self, 'Alerta', 'Grafica guardada.')
                 self.destroy()
            
        
    def seleccionar_registro(self):
        self.__ruta = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.__ruta.replace('/', '//')
        self.__registro = gf.seleccion_registro(self.__ruta)
    def graficar_segmento(self):
        canal = gf.seleccion_canal(self.__registro, int(self.canal.text()))
        tiempo, intervalo = gf.segmento(canal, int(self.intervalo_1.text()), int(self.intervalo_2.text()))

        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        ax.grid(True)
        ax.plot(tiempo, intervalo)
        ax.set_title('Segmento')
#        ax.title('Periodograma del registro: {}, canal: {}'.format(nreg, ncan))
        # refresh canvas
        self.canvas.draw()
    
class PacienteGUI(QDialog):
    def __init__(self, ruta):
        super(PacienteGUI, self).__init__()
        loadUi(ruta +'/gui/PacienteGUI.ui', self)
        self.__ruta = ruta
        validador = QtGui.QDoubleValidator()
        validador.setBottom(0)
        validador.setDecimals(0)
        self.Guardar.clicked.connect(self.guardarPaciente)
        self.Cedula.setValidator(validador)
        
    def getGenero(self):
        if self.Masculino.isChecked():
            genero = 'Masculino'
        elif self.Femenino.isChecked():
            genero = 'Femenino'
        else:
            genero = 'No especifica'
        return genero
    
    def guardarPaciente(self):
        cedula = self.Cedula.text()
        nombre = self.Nombre.text()
        apellidos = self.Apellidos.text()
        birth = self.Birth.text()
        genero = self.getGenero()
        conn = db.conectar(self.__ruta)
        db.crear_paciente(conn, cedula, nombre, apellidos, genero, birth)
      
        buttonReply = QMessageBox.question(self, 'Alerta', "Desea ingresr otro paciente?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            QMessageBox.about(self, 'Alerta', 'Paciente ingresado o actualizado.')
            self.Cedula.setText('')
            self.Nombre.setText('')
            self.Apellidos.setText('')
            
        else:
            QMessageBox.about(self, 'Alerta', 'Paciente ingresado o actualizado.')
            self.destroy()
 


class EliminarPaciente(QDialog):
    def __init__(self, ruta):
        super(EliminarPaciente, self).__init__()
        loadUi(ruta +'/gui/eliminar paciente.ui', self)
        self.__ruta = ruta
        validador = QtGui.QDoubleValidator()
        validador.setBottom(0)
        validador.setDecimals(0)
        self.Cedula.setValidator(validador)
        self.Eliminar.clicked.connect(self.eliminarPaciente)
    
    def eliminarPaciente(self):
        conn = db.conectar(self.__ruta)
        cedula = self.Cedula.text()
        if cedula == '':
            QMessageBox.about(self, 'Alerta', 'No se ingreso cedula.')
        else:
            existe = db.verificar_paciente(conn, int(cedula))
            if existe == True:
                db.eliminar_paciente(conn, int(cedula))
                buttonReply = QMessageBox.question(self, 'Alerta', "Desea eliminar otro paciente?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    QMessageBox.about(self, 'Alerta', 'paciente eliminado')
                    self.Cedula.setText('')
                
                else:
                    QMessageBox.about(self, 'Alerta', 'Paciente eliminado.')
                    self.destroy()
            elif existe == False:
                QMessageBox.about(self, 'Alerta', 'Paciente no existe.')
class ConsultarH(QDialog):
    def __init__(self, ruta):
        super(ConsultarH, self).__init__()
        loadUi(ruta +'/gui/consultar.ui', self)
        self.__ruta = ruta
        validar_cedula = QtGui.QIntValidator()
        validar_cedula.setBottom(0)
        self.Cedula.setValidator(validar_cedula)
        self.consultar.clicked.connect(self.mostrar)
        self.Cedula.setValidator(validar_cedula)
        self.graficar.clicked.connect(self.graficarConsulta)
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        
        self.canvas = FigureCanvas(self.figure)
        self.plano.addWidget(self.canvas)
        self.show()
    
    
    def graficarConsulta(self):
        conn = db.conectar(self.__ruta)
        cedula = self.Cedula.text()
        tipo = self.tipoGrafica.currentText()
        fecha = self.fechaConsulta.text()
        if cedula == '':
            QMessageBox.about(self, 'Alerta', 'No se ingreso cedula.')
        else:
            existe = db.verificar_paciente(conn, int(cedula))
            if existe == True:
                if tipo =='Correlacion':
                                            
                    datos = db.getDatos(conn, int(cedula), tipo, fecha)
                    
                    
                    ax = self.figure.add_subplot(111)
                    # discards the old graph
                    ax.clear()
                    # plot data
                    ax.grid(True)
                    ax.plot(datos)
                    # refresh canvas
                    self.canvas.draw()

                elif tipo == 'Periodograma':
                    datos = db.getDatos(conn, int(cedula), tipo, fecha)
                    periodo, frecuencias = datos[0], datos[1]
                    
                    ax = self.figure.add_subplot(111)
                    # discards the old graph
                    ax.clear()
                    # plot data
                    ax.grid(True)
                    ax.plot(periodo, frecuencias)
                    # refresh canvas
                    self.canvas.draw()

                elif tipo == 'Histograma':
                    datos = db.getDatos(conn, int(cedula), tipo, fecha)
                    
                    ax = self.figure.add_subplot(111)
                    # discards the old graph
                    ax.clear()
                    # plot data
                    ax.grid(True)
                    nbins = 'auto'
                    ax.hist(datos,nbins,facecolor='m',alpha=0.8 )
                    # refresh canvas
                    self.canvas.draw()
                elif tipo == 'Segmento':
                    datos = db.getDatos(conn, int(cedula), tipo, fecha)
                    tiempo, intervalo = datos[0], datos[1]
                    
                    ax = self.figure.add_subplot(111)
                    # discards the old graph
                    ax.clear()
                    # plot data
                    ax.grid(True)
                    ax.plot(tiempo, intervalo)
                    # refresh canvas
                    self.canvas.draw()
            elif existe == False:
                QMessageBox.about(self, 'Alerta', 'Paciente no existe.')
    def mostrar(self):
        conn = db.conectar(self.__ruta)
        cedula = self.Cedula.text()
        if cedula == '':
            QMessageBox.about(self, 'Alerta', 'No se ingreso cedula.')
        else:
            existe = db.verificar_paciente(conn, int(cedula))
            if existe == True:
                conn = db.conectar(self.__ruta)
                cursor = conn.cursor()
                query = "SELECT TipoGrafica, Fecha FROM Resultados WHERE Cedula= :cedula" #Consulta todos los datos de la tabla de pacientes
                result = cursor.execute(query, {'cedula':cedula}) #Ejecuta la consulta
                self.tabla_consultar.setRowCount(0) #Inicializa el grid en 0 filas
                for row_number, row_data in enumerate(result): 
                    self.tabla_consultar.insertRow(row_number)
                    for column_number, data in enumerate(row_data): 
                        self.tabla_consultar.setItem(row_number, column_number, QTableWidgetItem(str(data))) #Se asigna en cada posicion su valor correspondiente
                ax=self.figure.add_subplot(111)
                ax.clear()
                self.canvas.draw()
            elif existe == False:
                QMessageBox.about(self, 'Alerta', 'Paciente no existe.')


