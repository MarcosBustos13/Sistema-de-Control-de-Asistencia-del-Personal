import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sys
import os
import logging

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levellevel - %(message=s')

# Importaciones
try:
    from core.conexion import Conexion  # Clase Conexion
    from core.estilos import Estilos
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
        self.conexion = Conexion(db_name='ASISTENCIAS_JFS')  # Pasar el nombre de la base de datos
        
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.title("Eliminar Asistencia")
        self.configure(background='#000080')
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
        main_frame = tk.Frame(self, bg='#000080')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Campo de entrada para la cédula
        tk.Label(
            main_frame,
            text="Cédula:",
            font=('Helvetica', 12),
            fg='#FFFFFF',  # Color del texto
            bg='#000080'   # Color de fondo
        ).grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entry_cedula = tk.Entry(main_frame, width=20)
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_cedula.focus_set()

        # Campo de entrada para la fecha
        tk.Label(
            main_frame,
            text="Fecha (YYYY-MM-DD):",
            font=('Helvetica', 12),
            fg='#FFFFFF',  # Color del texto
            bg='#000080'   # Color de fondo
        ).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_fecha = tk.Entry(main_frame, width=20)
        self.entry_fecha.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Botones
        btn_frame = tk.Frame(main_frame, bg='#000080')
        btn_frame.grid(row=2, columnspan=2, pady=10)

        tk.Button(
            btn_frame,
            text="Eliminar",
            command=self.eliminar,
            bg="#FFFFFF",  # Fondo blanco
            fg="#000000"   # Texto negro
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.cerrar,
            bg="#FFFFFF",  # Fondo blanco
            fg="#000000"   # Texto negro
        ).pack(side='left', padx=5)

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
                cursor = self.conexion.connection.cursor()
                cursor.execute(
                    "DELETE FROM asistencias WHERE cedula_usuario = ? AND fecha = ?",
                    (self.entry_cedula.get(), self.entry_fecha.get())
                )
                self.conexion.connection.commit()
                self.conexion.desconectar()
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.destroy()
            except Exception as e:
                logging.error(f"Error al eliminar el registro: {str(e)}")
                messagebox.showerror("Error", f"Error al eliminar el registro: {str(e)}")

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
        app = VentanaEliminarAsistencia(root)
        app.mainloop()
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")
