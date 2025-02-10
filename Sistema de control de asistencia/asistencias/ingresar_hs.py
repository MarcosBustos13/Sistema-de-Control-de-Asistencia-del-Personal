# ingresar_hs.py
import tkinter as tk
import sys
import os
from tkinter import ttk, messagebox
from datetime import datetime, timezone
import logging
import pyodbc

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Importaciones
try:
    from core.conexion import Conexion 
    from core.estilos import Estilos
    logging.debug("Importaciones exitosas: Conexion y Estilos")
except ImportError as e:
    logging.error(f"Error al importar módulos: {str(e)}")
    sys.exit(1)

class Ventana(tk.Toplevel):
    """
    Ventana para registrar la hora de entrada y salida de un trabajador.
    """
    def __init__(self, parent):
        super().__init__(parent)
        logging.debug("Inicializando VentanaHoraEntrada")
        self.parent = parent
        self.title("Registro de Hora de Entrada y Salida")
        self.estilos = Estilos()
        self.conexion = Conexion(db_name='ASISTENCIAS_JFS')  # Conexión a la base de datos
        self.conexion.conectar()
        
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        """
        Configura la ventana principal.
        """
        logging.debug("Configurando ventana")
        self.title("Registro de Hora de Entrada y Salida")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))  # Fondo azul oscuro
        self.geometry("450x200")  # Tamaño ajustado
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        """
        Centra la ventana en la pantalla.
        """
        logging.debug("Centrando ventana")
        self.update_idletasks()
        ancho = 450  # Ancho fijo de la ventana
        alto = 200   # Alto fijo de la ventana
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """
        Crea la interfaz gráfica.
        """
        logging.debug("Creando interfaz gráfica")
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Cabecera informativa
        ttk.Label(
            main_frame,
            text=f"Fecha: {datetime.now(timezone.utc).strftime('%d/%m/%Y')}",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=0, columnspan=2, pady=5)
        ttk.Label(
            main_frame,
            text=f"Hora actual: {datetime.now(timezone.utc).strftime('%H:%M:%S')}",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=1, columnspan=2, pady=5)
        
        # Campo para ingresar la cédula
        ttk.Label(
            main_frame,
            text="Cédula del usuario:",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_cedula = ttk.Entry(main_frame, width=18, style='FormEntry.TEntry')  # Ajustar el ancho del campo de entrada
        self.entry_cedula.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        self.entry_cedula.focus_set()
        
        # Botones
        btn_frame = ttk.Frame(main_frame, style='MainFrame.TFrame')
        btn_frame.grid(row=3, columnspan=2, pady=10)
        ttk.Button(
            btn_frame,
            text="H-Entrada",
            style='Success.TButton',
            command=self.procesar_registro,
            width=10  # Ajustar el ancho del botón
        ).pack(side='left', padx=5)
        ttk.Button(
            btn_frame,
            text="H-Salida",
            style='Success.TButton',
            command=self.procesar_salida,
            width=10  # Ajustar el ancho del botón
        ).pack(side='left', padx=5)
        ttk.Button(
            btn_frame,
            text="Cerrar",
            style='Danger.TButton',
            command=self.cerrar,
            width=10  # Ajustar el ancho del botón
        ).pack(side='left', padx=5)

    def validar_cedula(self, cedula: str) -> bool:
        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula debe contener solo números.")
            return False
        if len(cedula) < 6:
            messagebox.showerror("Error", "La cédula debe tener al menos 6 dígitos.")
            return False
        return True

    def verificar_registro_existente(self) -> bool:
        try:
            with self.conexion.ejecutar_consulta(
                """SELECT 1 FROM ASISTENCIA 
                WHERE usuario = (SELECT id FROM USUARIOS WHERE cedula_id = ?)
                AND fecha = CAST(GETDATE() AS DATE)""",
                (self.entry_cedula.get(),)
            ) as cursor:
                return cursor.fetchone() is not None
        except Exception as e:
            logging.error(f"Error en verificación: {str(e)}")
            return False

    def obtener_usuario_id(self) -> int:
        try:
            with self.conexion.ejecutar_consulta(
                "SELECT id FROM USUARIOS WHERE cedula_id = ?",
                (self.entry_cedula.get(),)
            ) as cursor:
                resultado = cursor.fetchone()
                return resultado[0] if resultado else None
        except Exception as e:
            logging.error(f"Error obteniendo usuario: {str(e)}")
            return None

    def procesar_registro(self):
        logging.debug("Procesando registro de entrada")
        cedula = self.entry_cedula.get().strip()
        
        if not self.validar_cedula(cedula):
            return
        if self.verificar_registro_existente():
            messagebox.showwarning("Advertencia", "Ya existe un registro de entrada para hoy.")
            return
        usuario_id = self.obtener_usuario_id()
        if not usuario_id:
            messagebox.showerror("Error", "Usuario no registrado en el sistema.")
            return
        try:
            fecha_actual = datetime.now(timezone.utc).date()
            hora_actual = datetime.now(timezone.utc).time()
            dia_formateado = fecha_actual.strftime('%d/%m/%Y')
            query = """
            INSERT INTO ASISTENCIA (usuario, fecha, hora_entrada, hora_salida, observaciones, dia)
            VALUES (?, CAST(GETDATE() AS DATE), CAST(GETDATE() AS TIME), '00:00:00', 'Entrada registrada', ?)
            """
            
            logging.debug(f"Ejecutando query: {query}")
            logging.debug(f"Con parámetros: usuario_id={usuario_id}, dia_formateado={dia_formateado}")
            cursor = self.conexion.connection.cursor()
            cursor.execute(query, (usuario_id, dia_formateado))
            self.conexion.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Éxito", "Hora de entrada registrada correctamente")
            self.entry_cedula.delete(0, tk.END)
        except Exception as e:
            logging.error(f"Error al registrar entrada: {str(e)}")
            messagebox.showerror("Error", f"No se pudo registrar la entrada: {str(e)}")

    def procesar_salida(self):
        logging.debug("Procesando registro de salida")
        cedula = self.entry_cedula.get().strip()
        
        if not self.validar_cedula(cedula):
            return
        usuario_id = self.obtener_usuario_id()
        if not usuario_id:
            messagebox.showerror("Error", "Usuario no registrado en el sistema.")
            return
        try:
            query = """
            UPDATE ASISTENCIA
            SET hora_salida = CAST(GETDATE() AS TIME)
            WHERE usuario = ? AND fecha = CAST(GETDATE() AS DATE)
            """
            
            logging.debug(f"Ejecutando query: {query}")
            logging.debug(f"Con parámetros: usuario_id={usuario_id}")
            cursor = self.conexion.connection.cursor()
            cursor.execute(query, (usuario_id,))
            self.conexion.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Éxito", "Hora de salida registrada correctamente")
            self.entry_cedula.delete(0, tk.END)
        except Exception as e:
            logging.error(f"Error al registrar salida: {str(e)}")
            messagebox.showerror("Error", f"No se pudo registrar la salida: {str(e)}")

    def cerrar(self):
        logging.debug("Cerrando ventana")
        try:
            if self.conexion:
                self.conexion.desconectar()  # Utiliza el método desconectar
        except Exception as e:
            logging.error(f"Error al cerrar la conexión: {str(e)}")
        finally:
            self.destroy()

if __name__ == "__main__":
    logging.debug("Ejecutando el script principal")
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    app = Ventana(root)
    app.mainloop()