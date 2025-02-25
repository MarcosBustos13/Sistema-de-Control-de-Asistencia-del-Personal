import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
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
            messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")
            logging.error("No se pudo establecer conexión con la base de datos.")
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
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho, alto = 400, 300
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_interfaz(self):
        """Crea la interfaz gráfica de la ventana."""
        # Mostrar fecha y hora actual
        self.fecha_hora = tk.StringVar()
        self._actualizar_fecha_hora()

        # Día y fecha
        dia = tk.Label(self, text=f"Día: {datetime.now().strftime('%A')}", font=('Helvetica', 12), fg='white', bg=self.estilos.colores.get('fondo', '#000080'))
        dia.pack(pady=5)

        fecha = tk.Label(self, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", font=('Helvetica', 12), fg='white', bg=self.estilos.colores.get('fondo', '#000080'))
        fecha.pack(pady=5)

        hora = tk.Label(self, text=f"Hora: {datetime.now().strftime('%H:%M:%S')}", font=('Helvetica', 12), fg='white', bg=self.estilos.colores.get('fondo', '#000080'))
        hora.pack(pady=5)

        # Campo para la cédula
        cedula_label = tk.Label(self, text="Cédula ID*:", font=('Helvetica', 12), fg='white', bg=self.estilos.colores.get('fondo', '#000080'))
        cedula_label.pack(pady=5)

        self.widgets['cedula_id'] = ttk.Entry(self, width=20)
        self.widgets['cedula_id'].pack(pady=5)

        # Botones
        botones_frame = tk.Frame(self, bg=self.estilos.colores.get('fondo', '#000080'))
        botones_frame.pack(pady=20)

        ttk.Button(botones_frame, text="Registrar", command=self._registrar_entrada).pack(side='left', padx=10)
        ttk.Button(botones_frame, text="Cancelar", command=self._cerrar).pack(side='left', padx=10)

    def _actualizar_fecha_hora(self):
        """Actualiza la fecha y hora en la interfaz."""
        ahora = datetime.now()
        self.fecha_hora.set(f"Fecha y Hora: {ahora.strftime('%A, %d/%m/%Y %H:%M:%S')}")
        self.after(1000, self._actualizar_fecha_hora)  # Actualizar cada segundo

    def _registrar_entrada(self):
        """Registra la hora de entrada en la base de datos."""
        cedula = self.widgets['cedula_id'].get().strip()
        if not cedula:
            messagebox.showwarning("Advertencia", "Debe ingresar la cédula del trabajador.")
            return
        
        try:
            # Verificar si el usuario existe
            query = "SELECT id FROM USUARIOS WHERE cedula_id = ?"
            cursor = self.conexion.ejecutar_consulta(query, (cedula,))
            usuario = cursor.fetchone()
            
            if not usuario:
                messagebox.showerror("Error", "No se encontró un usuario con esa cédula.")
                return
            
            # Obtener la fecha y hora actual
            dia = datetime.now().strftime("%A")
            ahora = datetime.now()
            fecha = ahora.strftime("%Y-%m-%d")
            hora_entrada = ahora.strftime("%H:%M:%S")
            usuario_id = usuario[0]

            # Verificar si ya existe un registro para hoy
            query = "SELECT id FROM ASISTENCIA WHERE cedula_id = ? AND fecha = ?"
            cursor = self.conexion.ejecutar_consulta(query, (cedula, fecha))
            registro = cursor.fetchone()

            if registro:
                # Si ya existe un registro, no permitir otra entrada
                messagebox.showwarning("Advertencia", "Ya existe un registro de entrada para hoy.")
                return
            else:
                # Si no existe un registro, insertar uno nuevo
                query = """
                INSERT INTO ASISTENCIA (cedula_id, dia, fecha, hora_entrada, hora_salida, usuario, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                # Usar '00:00:00' como valor predeterminado para hora_salida
                self.conexion.ejecutar_consulta(query, (cedula, dia, fecha, hora_entrada, '00:00:00', usuario_id, None))
                logging.info(f"Insertando nuevo registro: cedula_id={cedula}, dia={dia}, fecha={fecha}, hora_entrada={hora_entrada}, usuario_id={usuario_id}")

            # Confirmar la transacción
            self.connection.commit()
            logging.info("Commit realizado exitosamente.")
            messagebox.showinfo("Éxito", "Entrada registrada exitosamente.")
            self._cerrar()
        except Exception as e:
            logging.error(f"Error al registrar la entrada: {str(e)}", exc_info=True)
            messagebox.showerror("Error", "No se pudo registrar la entrada.")

    def _cerrar(self):
        """Cierra la ventana y la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            logging.info("Conexión a la base de datos cerrada.")
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaEntrada(root)
    root.mainloop()
