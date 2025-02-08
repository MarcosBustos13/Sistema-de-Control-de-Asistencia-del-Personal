# core/conexion.py
import pyodbc
import logging

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Guarda logs en un archivo
        logging.StreamHandler()          # También muestra logs en la consola
    ]
)

class Conexion:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def conectar(self):
        """Establece una conexión con la base de datos."""
        try:
            self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=EQUIPO1\\SQLEXPRESS;'
                f'DATABASE={self.db_name};'
                'Trusted_Connection=yes;'
            )
            logging.info("Conexión exitosa a la base de datos.")
            return self.connection
        except pyodbc.Error as e:
            logging.error(f"Error al conectar a la base de datos: {str(e)}")
            return None

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()
            logging.info("Conexión cerrada.")

    def ejecutar_consulta(self, query, params=None):
        """
        Ejecuta una consulta SQL.
        - Para consultas SELECT, devuelve un cursor con los resultados.
        - Para otras consultas (INSERT, UPDATE, DELETE), realiza commit.
        """
        if not self.connection:
            logging.error("No hay una conexión establecida con la base de datos.")
            raise ConnectionError("No hay una conexión establecida con la base de datos.")

        try:
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Si es una consulta SELECT, devolvemos el cursor
                if query.lstrip().upper().startswith("SELECT"):
                    return cursor
                else:
                    self.connection.commit()
                    logging.info("Consulta ejecutada y confirmada.")
        except pyodbc.Error as e:
            logging.error(f"Error al ejecutar la consulta: {str(e)}")
            self.connection.rollback()  # Revertir cambios en caso de error
        except Exception as e:
            logging.error(f"Error inesperado al ejecutar la consulta: {str(e)}")


