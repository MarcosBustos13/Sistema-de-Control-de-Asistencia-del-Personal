import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
import pyodbc
from core.conexion import Conexion
from core.estilos import Estilos

# Configuración del logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class VentanaEntrada(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.widgets = {}
        self.estilos = Estilos()
        self.conexion = Conexion(db_name='ASISTENCIAS_JFS')
        self.connection = self.conexion.conectar()
        
        if not self.connection:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            self.destroy()
            return
        
        self.title("Registrar Hora de Entrada")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self._centrar_ventana()
        self._crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self.widgets['cedula_id'].focus()

    def _centrar_ventana(self):
        self.update_idletasks()
        ancho, alto = 400, 300
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_interfaz(self):
        self.fecha_hora = tk.StringVar()
        self._actualizar_fecha_hora()

        # Sección superior: Fecha y hora
        frame_superior = tk.Frame(self, bg=self.estilos.colores.get('fondo', '#000080'))
        frame_superior.pack(pady=10)

        tk.Label(frame_superior, 
                text=f"Día: {datetime.now().strftime('%A')}", 
                font=('Helvetica', 12), 
                fg='white', 
                bg=self.estilos.colores.get('fondo', '#000080')).pack(pady=2)

        tk.Label(frame_superior, 
                text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 
                font=('Helvetica', 12), 
                fg='white', 
                bg=self.estilos.colores.get('fondo', '#000080')).pack(pady=2)

        tk.Label(frame_superior, 
                text=f"Hora: {datetime.now().strftime('%H:%M:%S')}", 
                font=('Helvetica', 12), 
                fg='white', 
                bg=self.estilos.colores.get('fondo', '#000080')).pack(pady=2)

        # Campo de cédula
        frame_medio = tk.Frame(self, bg=self.estilos.colores.get('fondo', '#000080'))
        frame_medio.pack(pady=15)

        tk.Label(frame_medio, 
                text="Cédula ID*:", 
                font=('Helvetica', 12), 
                fg='white', 
                bg=self.estilos.colores.get('fondo', '#000080')).pack(pady=5)

        self.widgets['cedula_id'] = ttk.Entry(frame_medio, width=20)
        self.widgets['cedula_id'].pack(pady=5)

        # Botones
        frame_botones = tk.Frame(self, bg=self.estilos.colores.get('fondo', '#000080'))
        frame_botones.pack(pady=20)

        ttk.Button(frame_botones, 
                 text="Registrar", 
                 command=self._registrar_entrada).pack(side='left', padx=10)

        ttk.Button(frame_botones, 
                 text="Cancelar", 
                 command=self._cerrar).pack(side='left', padx=10)

    def _actualizar_fecha_hora(self):
        ahora = datetime.now()
        self.fecha_hora.set(f"Fecha y Hora: {ahora.strftime('%A, %d/%m/%Y %H:%M:%S')}")
        self.after(1000, self._actualizar_fecha_hora)

    def _registrar_entrada(self):
        cedula = self.widgets['cedula_id'].get().strip()
        if not cedula:
            messagebox.showwarning("Advertencia", "Ingrese la cédula del trabajador.")
            return

        cursor = None
        try:
            cursor = self.connection.cursor()

            # 1. Verificar existencia del usuario y obtener tipo_trabajador
            cursor.execute("SELECT tipo_trabajador FROM USUARIOS WHERE cedula_id = ?", (cedula,))
            usuario = cursor.fetchone()
            if not usuario:
                messagebox.showerror("Error", "Usuario no registrado.")
                return

            # 2. Validar registro duplicado
            fecha_actual = datetime.now().date()
            cursor.execute("SELECT id FROM ASISTENCIA WHERE cedula_id = ? AND fecha = ?", (cedula, fecha_actual))
            if cursor.fetchone():
                messagebox.showwarning("Advertencia", "Entrada ya registrada hoy.")
                return

            # 3. Insertar registro
            cursor.execute("""
                INSERT INTO ASISTENCIA 
                    (cedula_id, tipo_trabajador, dia, fecha, hora_entrada, hora_salida, observaciones)
                VALUES (?, ?, ?, ?, ?, NULL, NULL)
            """, (
                cedula,
                usuario[0],
                datetime.now().strftime("%A"),
                fecha_actual,
                datetime.now().time()
            ))

            self.connection.commit()
            messagebox.showinfo("Éxito", "Entrada registrada.")
            self.destroy()

        except pyodbc.Error as e:
            logging.error(f"Error SQL: {str(e)}")
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            self.connection.rollback()
        except Exception as e:
            logging.error(f"Error inesperado: {str(e)}")
            messagebox.showerror("Error", "Error inesperado.")
        finally:
            if cursor:
                cursor.close()

    def _cerrar(self):
        if self.connection:
            self.connection.close()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaEntrada(root)
    root.mainloop()
