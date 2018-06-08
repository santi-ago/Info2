#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 09:34:16 2018

@author: aya
"""
#Libreria para manejo de bases de datos
import sqlite3
ruta = '/home/aya/Proyecto_final'
#Libreria para manipular arrays
import io
import numpy as np

def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)
# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)



#Funcion para crear y conectar a la base de datos
def conectar(path = ruta):
    conn = sqlite3.connect(path+'/db/Sistema.db', detect_types=sqlite3.PARSE_DECLTYPES) #Abre o crea la base de datos
    c = conn.cursor() #Asigna un cursor a una varuable
    #Si la base de datos no existe, crea las tablas
    c.execute("CREATE TABLE IF NOT EXISTS Pacientes (Cedula INTEGER PRIMARY KEY, Nombre TEXT, Apellidos TEXT, Genero TEXT, Nacimiento TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS Resultados (Cedula INTEGER, TipoGrafica TEXT, Fecha TEXT, Datos array)")
    conn.commit() #Guarda los cambios hechos
    return conn #Devuelve la coneccion lista para hacer consultas


#Inserta un paciente en la base de datos
def crear_paciente(conn, CedulaP, NombreP, ApellidosP, GeneroP, NacimientoP):
    cursor = conn.cursor()
    cursor.execute('''
                  INSERT OR REPLACE INTO Pacientes(Cedula, Nombre, Apellidos, Genero, Nacimiento)
                  VALUES(:cedula,:nombre,:apellidos,:genero,:nacimiento)''', {'cedula':CedulaP, 'nombre':NombreP, 'apellidos':ApellidosP, 'genero':GeneroP, 'nacimiento':NacimientoP})
    
    conn.commit()
    return True

#Verifica si el paciente ya existe en la base de datos
def verificar_paciente(conn, CedulaP):
    cursor = conn.cursor()
    a = cursor.execute('''SELECT Cedula FROM Pacientes WHERE Cedula =:cedula''', {'cedula':CedulaP})
    resultado = a.fetchall()
    if resultado == []:
        return False
    else:
        return True

#Elimina un paciente de la base de datos
def eliminar_paciente(conn, CedulaP):
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM Pacientes WHERE Cedula = :cedula''', {'cedula':CedulaP})
    conn.commit()
    return True

#Ingresa los datos usados en las graficas a la tabla Resultados
def addGrafica(conn, CedulaG, TipoG, FechaG, DatosG):
    cursor = conn.cursor()
    cursor.execute('''
                  INSERT INTO Resultados(Cedula, TipoGrafica, Fecha, Datos)
                  VALUES(:cedula,:grafica,:fecha,:datos)''', {'cedula':CedulaG, 'grafica':TipoG, 'fecha':FechaG, 'datos':DatosG})
    conn.commit()
    return True



#Selecciona los datos de la tabla Resultados
def getDatos(conn, CedulaG, TipoG, FechaG):
    cursor = conn.cursor()
    cursor.execute('''SELECT Datos FROM Resultados WHERE Cedula =:cedula AND TipoGrafica = :grafica AND Fecha = :fecha''', {'cedula':CedulaG, 'grafica':TipoG, 'fecha':FechaG})
    data = cursor.fetchone()[0] #Selecciona solo la posicion 0 de los datos
    return data #Devuelve los datos


