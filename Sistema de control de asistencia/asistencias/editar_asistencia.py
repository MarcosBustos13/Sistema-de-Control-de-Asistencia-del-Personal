# editar_asistencia.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importaciones
try:
    from core.conexion import Conexion
    from core.estilos import Estilos
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
except ImportError as e:
    logging.error(f"Error al importar módulos: {str(e)}")
    sys.exit(1)

class VentanaEditarAsistencia(tk.Toplevel):
    """
    Ventana para editar las asistencias de un usuario en una fecha determinada.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.estilos = Estilos()
        self.conexion = Conexion(db_name='ASISTENCIAS_JFS')
        
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.title("Editar Asistencia")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self.geometry("450x300")
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 450
        alto = 300
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea la interfaz gráfica."""
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Campo de entrada para la cédula
        ttk.Label(
            main_frame,
            text="Cédula:",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.entry_cedula = ttk.Entry(main_frame, width=25, style='FormEntry.TEntry')
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Campo de entrada para la fecha
        ttk.Label(
            main_frame,
            text="Fecha (YYYY-MM-DD):",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.entry_fecha = ttk.Entry(main_frame, width=25, style='FormEntry.TEntry')
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Botón para cargar los datos
        ttk.Button(
            main_frame,
            text="Cargar",
            style='Success.TButton',
            command=self.cargar
        ).grid(row=1, column=2, padx=5, pady=5, sticky='w')

        # Campos para editar la hora de entrada y salida
        ttk.Label(
            main_frame,
            text="Nueva Hora Entrada (HH:MM:SS):",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.entry_entrada = ttk.Entry(main_frame, width=25, style='FormEntry.TEntry')
        self.entry_entrada.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(
            main_frame,
            text="Nueva Hora Salida (HH:MM:SS):",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.entry_salida = ttk.Entry(main_frame, width=25, style='FormEntry.TEntry')
        self.entry_salida.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Botón para guardar los cambios
        ttk.Button(
            main_frame,
            text="Guardar",
            style='Success.TButton',
            command=self.guardar
        ).grid(row=4, column=0, columnspan=3, pady=10)

    def cargar(self):
        """Carga los datos de la asistencia para editar."""
        cedula = self.entry_cedula.get().strip()
        fecha = self.entry_fecha.get().strip()
        
        # Validar entradas
        if not cedula or not fecha:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        
        if not self.validar_fecha(fecha):
            messagebox.showwarning("Advertencia", "El formato de la fecha debe ser YYYY-MM-DD.")
            return
        
        try:
            if not self.conexion.conectar():
                raise Exception("Error de conexión a la base de datos")
            cursor = self.conexion.connection.cursor()
            cursor.execute(
                "SELECT hora_entrada, hora_salida FROM ASISTENCIA WHERE usuario = (SELECT id FROM USUARIOS WHERE cedula_id = ?) AND fecha = ?",
                (cedula, fecha)
            )
            datos = cursor.fetchone()
            
            if datos:
                self.entry_entrada.delete(0, tk.END)
                if datos[0] is not None:
                    self.entry_entrada.insert(0, datos[0])
                self.entry_salida.delete(0, tk.END)
                if datos[1] is not None:
                    self.entry_salida.insert(0, datos[1])
            else:
                messagebox.showinfo("Información", "No se encontró ningún registro con los datos proporcionados.")
                
            self.conexion.desconectar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")

    def guardar(self):
        """Guarda los cambios en la base de datos."""
        cedula = self.entry_cedula.get().strip()
        fecha = self.entry_fecha.get().strip()
        nueva_entrada = self.entry_entrada.get().strip()
        nueva_salida = self.entry_salida.get().strip()
        
        # Validar entradas
        if not cedula or not fecha or not nueva_entrada or not nueva_salida:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        
        if not self.validar_fecha(fecha):
            messagebox.showwarning("Advertencia", "El formato de la fecha debe ser YYYY-MM-DD.")
            return
        
        try:
            if not self.conexion.conectar():
                raise Exception("Error de conexión a la base de datos")
            cursor = self.conexion.connection.cursor()
            cursor.execute(
                "UPDATE ASISTENCIA SET hora_entrada = ?, hora_salida = ? WHERE usuario = (SELECT id FROM USUARIOS WHERE cedula_id = ?) AND fecha = ?",
                (nueva_entrada, nueva_salida, cedula, fecha)
            )
            self.conexion.connection.commit()
            self.conexion.desconectar()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el registro: {str(e)}")

    def validar_fecha(self, fecha: str) -> bool:
        """Valida que la fecha tenga el formato YYYY-MM-DD."""
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def cerrar(self):
        """Cierra la ventana y desconecta la base de datos."""
        try:
            if self.conexion:
                self.conexion.desconectar()
        except Exception as e:
            logging.error(f"Error al cerrar la conexión: {str(e)}")
        finally:
            self.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()
        app = VentanaEditarAsistencia(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")