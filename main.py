#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 2018

@author: Santiago
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi

# Libreria para leer rutas y archivos en el sistema operativo
import os
#Se asigna la ruta actual a una variable
main_route = os.getcwd()
#Se agrega al PATH la direccion de los scripts para importarlos
sys.path.append(main_route+'/scripts')
#Se importan los scripts
import periodograma as pd
import SQLitedb as db
pd.ruta = main_route
db.ruta = main_route



class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi('gui/ventana principal.ui', self)
        self.actualizarPacientes.clicked.connect(self.actualizar)
                
        self.actionPeriodograma.triggered.connect(self.GPeriodograma)
        self.actionCorrelacion.triggered.connect(self.GCorrelacion)
        self.actionHistrograma.triggered.connect(self.GHistograma)
        self.actionSegmento.triggered.connect(self.GSegmento)
        
        self.actionCrear_paciente.triggered.connect(self.CrearPaciente)
        self.actionEliminar_paciente.triggered.connect(self.EliminarPaciente)
        self.actionVer_historial.triggered.connect(self.consultar)

      
    def actualizar(self):
        conn = db.conectar(main_route)
        cursor = conn.cursor()
        query = "SELECT Cedula, Nombre, Apellidos, Genero, Nacimiento FROM Pacientes" #Consulta todos los datos de la tabla de pacientes
        result = cursor.execute(query) #Ejecuta la consulta
        self.tabla_pacientes.setRowCount(0) #Inicializa el grid en 0 filas
        for row_number, row_data in enumerate(result): #Ciclo para enumerar posicion y filas
            self.tabla_pacientes.insertRow(row_number) #Se agrega una fila al grid
            for column_number, data in enumerate(row_data): #Ciclo para enumerar columnas y datos
                self.tabla_pacientes.setItem(row_number, column_number, QTableWidgetItem(str(data))) #Se asigna en cada posicion su valor correspondiente
        conn.close()
        
    def GPeriodograma(self):
        self.graf_periodograma = pd.Periodograma(main_route)
        self.graf_periodograma.show()
    def GCorrelacion(self):
        self.graf_correlacion = pd.Correlacion(main_route)
        self.graf_correlacion.show()
    def GHistograma(self):
        self.graf_histograma = pd.Histograma(main_route)
        self.graf_histograma.show()
    def GSegmento(self):
        self.graf_segmento = pd.Segmento(main_route)
        self.graf_segmento.show()
        
    def consultar(self):
        self.consulta_historial=pd.ConsultarH(main_route)
        self.consulta_historial.show()
    def CrearPaciente(self):
        self.crear_paciente = pd.PacienteGUI(main_route) 
        self.crear_paciente.show()
    def EliminarPaciente(self):
        self.eliminar_paciente = pd.EliminarPaciente(main_route)
        self.eliminar_paciente.show()
        
app = QApplication(sys.argv)
widget = Menu()
widget.show()
sys.exit(app.exec_())
