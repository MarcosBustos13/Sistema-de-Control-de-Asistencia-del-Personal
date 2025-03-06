# core/conexion.py

import pyodbc
import logging

class Conexion:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def conectar(self):
        try:
            self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-E6O194D\\SQLEXPRESS;'
                f'DATABASE={self.db_name};'
                'Trusted_Connection=yes;'
            )
            print("Conexión exitosa a la base de datos.")
            return self.connection
        except pyodbc.Error as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            logging.error(f"Error al conectar a la base de datos: {str(e)}")
            return None

    def desconectar(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

    def ejecutar_consulta(self, query, params=None):
        try:
            if not self.connection:
                raise Exception("No hay una conexión establecida con la base de datos.")
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            # Si es una consulta SELECT, devolvemos el cursor para leer los datos
            if query.lstrip().upper().startswith("SELECT"):
                return cursor
            else:
                self.connection.commit()
                cursor.close()
                return None
        except pyodbc.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
            logging.error(f"Error al ejecutar la consulta: {str(e)}")
            return None
        except Exception as e:
            print(f"Error en la ejecución de la consulta: {str(e)}")
            logging.error(f"Error en la ejecución de la consulta: {str(e)}")
            return None


