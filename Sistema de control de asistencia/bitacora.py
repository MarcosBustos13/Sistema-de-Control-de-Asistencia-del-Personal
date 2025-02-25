import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pyodbc

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ConexionBD:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.conexion = None

    def conectar(self):
        try:
            # Conexión con autenticación integrada de Windows
            self.conexion = pyodbc.connect(
                f"DRIVER={{SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
            print("Conexión exitosa a la base de datos.")
            return True
        except pyodbc.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False

    def insertar_incidencia(self, mensaje):
        if not self.conexion:
            print("No hay conexión a la base de datos.")
            return False
        try:
            with self.conexion.cursor() as cursor:
                # Query para insertar incidencias en la tabla BITACORA
                query = "INSERT INTO BITACORA (mensaje, fecha) VALUES (?, ?)"
                cursor.execute(query, (mensaje, datetime.now()))
                self.conexion.commit()  # Guardar los cambios
                print("Incidencia registrada correctamente.")
                return True
        except pyodbc.Error as e:
            print(f"Error al registrar incidencia: {e}")
            return False

    def consultar_incidencias(self):
        if not self.conexion:
            print("No hay conexión a la base de datos.")
            return []
        try:
            with self.conexion.cursor() as cursor:
                # Query para consultar todas las incidencias
                query = "SELECT mensaje, fecha FROM BITACORA ORDER BY fecha DESC"
                cursor.execute(query)
                return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error al consultar incidencias: {e}")
            return []

    def cerrar_conexion(self):
        if self.conexion:
            try:
                self.conexion.close()
                print("Conexión cerrada.")
            except pyodbc.Error as e:
                print(f"Error al cerrar la conexión: {e}")


class Ventana(tk.Toplevel):
    """
    Ventana para registrar y consultar incidencias en la bitácora.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.conexion_bd = ConexionBD("EQUIPO1\\SQLEXPRESS", "ASISTENCIAS_JFS")  # Nombre de la base de datos actualizado
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        self.title("Bitácora de Incidencias")
        self.configure(background="navy")  # Fondo azul oscuro
        self.geometry("600x500")  # Tamaño adecuado para la interfaz
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()  # Ancho actual de la ventana
        alto = self.winfo_height()  # Alto actual de la ventana
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{x}+{y}")

    def crear_interfaz(self):
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Área para mostrar las incidencias registradas
        ttk.Label(main_frame, text="Incidencias Registradas:", style='FormLabel.TLabel').grid(
            row=0, column=0, columnspan=2, pady=(10, 5), sticky='w'
        )
        self.text_incidencias = tk.Text(main_frame, height=15, width=70, wrap='word', state='disabled')
        self.text_incidencias.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Botón para refrescar las incidencias
        ttk.Button(
            main_frame,
            text="Refrescar",
            style='Info.TButton',
            command=self.consultar_incidencias
        ).grid(row=2, column=0, columnspan=2, pady=(5, 10))

        # Configurar estilos predeterminados
        estilo = ttk.Style()
        estilo.configure('FormLabel.TLabel', background="navy", foreground="white", font=('Helvetica', 12))
        estilo.configure('Info.TButton', background="navy", foreground="white", font=('Helvetica', 12))

    def consultar_incidencias(self):
        if not self.conexion_bd.conectar():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        incidencias = self.conexion_bd.consultar_incidencias()
        self.text_incidencias.config(state='normal')  # Habilitar edición temporalmente
        self.text_incidencias.delete(1.0, tk.END)  # Limpiar el área de texto

        if incidencias:
            for mensaje, fecha in incidencias:
                self.text_incidencias.insert(tk.END, f"{fecha}: {mensaje}\n")
        else:
            self.text_incidencias.insert(tk.END, "No hay incidencias registradas.\n")

        self.text_incidencias.config(state='disabled')  # Deshabilitar edición
        self.conexion_bd.cerrar_conexion()

    def registrar_incidencia_automatica(self, mensaje):
        """
        Registra una incidencia automáticamente desde otros módulos.
        """
        if not self.conexion_bd.conectar():
            print("No se pudo conectar a la base de datos para registrar la incidencia.")
            return

        if self.conexion_bd.insertar_incidencia(mensaje):
            print(f"Incidencia registrada automáticamente: {mensaje}")
        else:
            print("Error al registrar incidencia automáticamente.")

        self.conexion_bd.cerrar_conexion()

    def cerrar(self):
        try:
            if self.conexion_bd:
                self.conexion_bd.cerrar_conexion()
        except Exception as e:
            print(f"Error al cerrar la conexión: {str(e)}")
        finally:
            self.destroy()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana raíz
        app = Ventana(root)
        app.mainloop()  # Ejecuta el bucle principal de la interfaz gráfica
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")