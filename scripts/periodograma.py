#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 09:55:40 2018

@author: aya
"""

import sys
from PyQt5.QtWidgets import *#QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import graficas as gf
import SQLitedb as db
ruta = ''

class Periodograma(QDialog):
    def __init__(self):
        super(Periodograma, self).__init__()
        loadUi(ruta +'/gui/periodograma.ui', self)
#        self.canal.SetValidator(QtGui.QIntValidator(1, 8))
        self.graficar.clicked.connect(self.graficar_periodograma)
        self.cargarRegistro.clicked.connect(self.seleccionar_registro)
        self.__ruta = ''
        self.__registro = []
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.plano.addWidget(self.canvas)
        self.show()
        
    def seleccionar_registro(self):
        self.__ruta = QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.__ruta.replace('/', '//')
        self.__registro = gf.seleccion_registro(self.__ruta)
#        file = sio.loadmat(self.__ruta) #Carga el archivo seleccionado por el usuario
#        self.__registro = file['data']
    def graficar_periodograma(self):
        canal_seleccionado = gf.seleccion_canal(self.__registro, int(self.canal.text()))
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

class PacienteGUI(QDialog):
    def __init__(self):
        super(PacienteGUI, self).__init__()
        loadUi(ruta +'/gui/PacienteGUI.ui', self)
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
        db.crear_paciente(cedula, nombre, apellidos, genero, birth)
        QMessageBox.about(self, 'Alerta', 'Paciente ingresado o actualizado.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PacienteGUI()
    widget.show()
    sys.exit(app.exec_())