# eliminar_usuario.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import logging
import pyodbc
import sys
import os

# Ajustar la ruta para importar correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Importaciones
try:
    from core.conexion import Conexion  # Importar la clase correcta
    from core.estilos import Estilos
    logging.debug("Importaciones exitosas: Conexion y Estilos")
except ImportError as e:
    logging.error(f"Error al importar módulos: {str(e)}")
    sys.exit(1)

class Ventana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.estilos = Estilos()
        
        # Crear la conexión a la base de datos
        self.conexion = Conexion(db_name='ASISTENCIAS_JFS')
        self.connection = self.conexion.conectar()  # Establecer la conexión
        
        if not self.connection:
            messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")
            self.destroy()
            return
        
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.title("Eliminar Usuario")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))  # Fondo azul oscuro
        self.geometry("300x250")  # Tamaño ajustado
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 300  # Ancho fijo de la ventana
        alto = 250   # Alto fijo de la ventana
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea la interfaz gráfica."""
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Etiqueta "Nº de Cédula"
        ttk.Label(
            main_frame,
            text="Nº de Cédula:",
            font=('Helvetica', 14, 'bold'),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),  # Letras blancas
            background=self.estilos.colores.get('fondo', '#000080')  # Fondo azul oscuro
        ).grid(row=0, column=0, padx=5, pady=10, sticky='e')
        
        # Campo de entrada para la cédula
        self.entry_cedula = ttk.Entry(main_frame, style='FormEntry.TEntry')
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.entry_cedula.focus_set()
        
        # Botones "Eliminar" y "Cancelar"
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame,
            text="Eliminar",
            style='Danger.TButton',
            command=self.proceso_eliminacion
        ).pack(side='left', padx=10)
        
        ttk.Button(
            btn_frame,
            text="Cancelar",
            style='Cancel.TButton',
            command=self.cerrar
        ).pack(side='left', padx=10)

    def validar_cedula(self) -> bool:
        """Valida que la cédula sea válida."""
        cedula = self.entry_cedula.get().strip()
        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula debe contener solo números.")
            return False
        if len(cedula) < 6:
            messagebox.showerror("Error", "La cédula debe tener al menos 6 dígitos.")
            return False
        return True

    def verificar_existencia(self) -> bool:
        """Verifica si la cédula existe en la base de datos."""
        try:
            cursor = self.conexion.ejecutar_consulta(
                "SELECT COUNT(*) FROM USUARIOS WHERE cedula_id = ?", 
                (self.entry_cedula.get(),)
            )
            if cursor:
                return cursor.fetchone()[0] > 0
            return False
        except Exception as e:
            logging.error(f"Error en verificación: {str(e)}")
            messagebox.showerror("Error", "No se pudo verificar la existencia del usuario.")
            return False

    def proceso_eliminacion(self):
        """Procesa la eliminación del usuario."""
        if not self.validar_cedula():
            return
        if not self.verificar_existencia():
            messagebox.showinfo("Información", "Usuario no encontrado.")
            return
        if messagebox.askyesno(
            "Confirmar Eliminación", 
            "¿Está seguro de eliminar este usuario y todas sus asistencias?\nEsta acción no se puede deshacer!",
            icon='warning'
        ):
            self.eliminar_registros()

    def eliminar_registros(self):
        """Elimina el usuario y sus registros relacionados."""
        try:
            # Eliminar registros relacionados en ASISTENCIA
            self.conexion.ejecutar_consulta(
                "DELETE FROM ASISTENCIA WHERE usuario IN (SELECT id FROM USUARIOS WHERE cedula_id = ?)",
                (self.entry_cedula.get(),)
            )
            # Eliminar el usuario
            self.conexion.ejecutar_consulta(
                "DELETE FROM USUARIOS WHERE cedula_id = ?", 
                (self.entry_cedula.get(),)
            )
            # Registrar la acción en BITACORA
            self.conexion.ejecutar_consulta(
                "INSERT INTO BITACORA (usuario_id, accion) VALUES (?, ?)",
                (self.obtener_id_usuario_actual(), f"Eliminó al usuario con cédula {self.entry_cedula.get()}")
            )
            messagebox.showinfo("Éxito", "Usuario y registros relacionados eliminados correctamente.")
            self.destroy()
        except pyodbc.Error as e:
            logging.error(f"Error de base de datos: {str(e)}")
            messagebox.showerror("Error Crítico", "No se pudo completar la eliminación. Consulte el registro de errores.")
        except Exception as e:
            logging.error(f"Error inesperado: {str(e)}")
            messagebox.showerror("Error", str(e))

    def obtener_id_usuario_actual(self) -> int:
        """Obtiene el ID del usuario administrador."""
        # TODO: Implementar lógica para obtener el ID del usuario actual
        return 1  # Ejemplo temporal

    def cerrar(self):
        """Cierra la ventana y desconecta la base de datos."""
        if self.conexion:
            self.conexion.desconectar()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Ventana(root)
    root.mainloop()