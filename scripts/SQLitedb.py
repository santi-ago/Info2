#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 09:34:16 2018

@author: aya
"""

import sqlite3
ruta = ''
def conectar(path = ruta):
    conn = sqlite3.connect(path+'/db/Sistema.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Pacientes (Cedula INTEGER PRIMARY KEY, Nombre TEXT, Apellidos TEXT, Genero TEXT, Nacimiento TEXT)")
    conn.commit()
    return conn
def crear_paciente(CedulaP, NombreP, ApellidosP, GeneroP, NacimientoP):
    conn = conectar()
    cursor = conn.cursor()
#    cursor.execute('''INSERT INTO Pacientes(Cedula, Nombre, Apellidos, Genero, Nacimiento)
#                  VALUES(:cedula,:nombre,:apellidos,:genero,:nacimiento)''', {'cedula':CedulaP, 'nombre':NombreP, 'apellidos:'ApellidosP, 'genero':GeneroP, 'nacimiento':NacimientoP})
    cursor.execute('''
                  INSERT OR REPLACE INTO Pacientes(Cedula, Nombre, Apellidos, Genero, Nacimiento)
                  VALUES(:cedula,:nombre,:apellidos,:genero,:nacimiento)''', {'cedula':CedulaP, 'nombre':NombreP, 'apellidos':ApellidosP, 'genero':GeneroP, 'nacimiento':NacimientoP})
    
    conn.commit()
    return True


#crear_paciente(1037, 'Santiago', 'Gutierrez Perez', 'Masculino', '1995-07-19')
#crear_paciente(1036, 'Juan', 'Perez Gomez', 'Masculino', '1966-03-09')


'''
IF EXIST (SELECT Cedula FROM Pacientes where Cedula = :cedula) BEGIN
UPDATE Pacientes SET (Nombre = :nombre, :apellidos, :genero, Nacimiento) WHERE Cedula = :cedula
END ELSE BEGIN

'''

