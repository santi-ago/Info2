#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 2018

@author: Santiago
"""

import sys
from PyQt5.QtWidgets import *#QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtGui
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
conn = db.conectar(main_route)
cursor = conn.cursor()


class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi('gui/ventana principal.ui', self)
        self.actionPeriodograma.triggered.connect(self.GPeriodograma)
        self.actionCrear_paciente.triggered.connect(self.CrearPaciente)
        self.refrescarPacientes.clicked.connect(self.refrescar)
        
    def refrescar(self):
        query = "SELECT Cedula, Nombre, Apellidos, Genero, Nacimiento FROM Pacientes" #Consulta todos los datos de la tabla de pacientes
        result = cursor.execute(query) #Ejecuta la consulta
        self.tabla_pacientes.setRowCount(0) #Inicializa el grid en 0 filas
        for row_number, row_data in enumerate(result): #Ciclo para enumerar posicion y filas
            self.tabla_pacientes.insertRow(row_number) #Se agrega una fila al grid
            for column_number, data in enumerate(row_data): #Ciclo para enumerar columnas y datos
                self.tabla_pacientes.setItem(row_number, column_number, QTableWidgetItem(str(data))) #Se asigna en cada posicion su valor correspondiente
        
    def GPeriodograma(self):
        self.graf_periodograma = pd.Periodograma()
        self.graf_periodograma.show()
    def CrearPaciente(self):
        self.crear_paciente = pd.PacienteGUI() 
        self.crear_paciente.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Menu()
    widget.show()
    sys.exit(app.exec_())
