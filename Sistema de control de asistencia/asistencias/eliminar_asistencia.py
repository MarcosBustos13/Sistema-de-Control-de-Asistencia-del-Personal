# eliminar_asistencia.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
import sys
import os
import logging

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importaciones
try:
    from core.conexion import DBConexion
    from core.estilos import Estilos
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
except ImportError as e:
    logging.error(f"Error al importar módulos: {str(e)}")
    sys.exit(1)

class VentanaEliminarAsistencia(tk.Toplevel):
    """
    Ventana para eliminar una asistencia de un usuario en una fecha determinada.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.estilos = Estilos()
        self.conexion = DBConexion()
        
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.title("Eliminar Asistencia")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self.geometry("400x200")
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 400
        alto = 200
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
        ).grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.entry_cedula = ttk.Entry(main_frame, style='FormEntry.TEntry')
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_cedula.focus_set()

        # Campo de entrada para la fecha
        ttk.Label(
            main_frame,
            text="Fecha (YYYY-MM-DD):",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.entry_fecha = ttk.Entry(main_frame, style='FormEntry.TEntry')
        self.entry_fecha.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Botón para eliminar la asistencia
        ttk.Button(
            main_frame,
            text="Eliminar",
            style='Danger.TButton',
            command=self.eliminar
        ).grid(row=2, columnspan=2, pady=10)

    def validar_datos(self) -> bool:
        """Valida que los datos ingresados sean correctos."""
        cedula = self.entry_cedula.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not cedula.isdigit():
            messagebox.showwarning("Advertencia", "La cédula debe contener solo números.")
            return False

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Advertencia", "El formato de la fecha debe ser YYYY-MM-DD.")
            return False

        return True

    def eliminar(self):
        """Elimina el registro de asistencia de la base de datos."""
        if not self.validar_datos():
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar registro de asistencia?"):
            try:
                if not self.conexion.conectar():
                    raise Exception("Error de conexión a la base de datos")

                cursor = self.conexion.cursor()
                cursor.execute(
                    "DELETE FROM asistencias WHERE cedula_usuario = ? AND fecha = ?",
                    (self.entry_cedula.get(), self.entry_fecha.get())
                )
                self.conexion.commit()
                self.conexion.cerrar()
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.destroy()
            except Exception as e:
                logging.error(f"Error al eliminar el registro: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar el registro: {str(e)}")

    def cerrar(self):
        """Cierra la ventana y desconecta la base de datos."""
        try:
            if self.conexion:
                self.conexion.cerrar()
        except Exception as e:
            logging.error(f"Error al cerrar la conexión: {str(e)}")
        finally:
            self.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()
        app = VentanaEliminarAsistencia(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")