# reporte_individual.py
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import logging

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importaciones
try:
    from core.conexion import Conexion
    from core.estilos import Estilos
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
except ImportError as e:
    logging.error(f"Error al importar módulos: {str(e)}")
    sys.exit(1)

class Ventana(tk.Toplevel):
    """
    Ventana para generar el reporte individual de asistencias de un usuario.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.estilos = Estilos()
        self.conexion = Conexion("ASISTENCIAS_JFS")
        
        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.title("Reporte Individual")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self.geometry("400x250")
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 400
        alto = 250
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea la interfaz gráfica."""
        # Configurar estilos predeterminados
        estilo = ttk.Style()
        estilo.configure(
            'FormLabel.TLabel',
            background=self.estilos.colores.get('fondo', '#000080'),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            font=('Helvetica', 12)
        )
        estilo.configure(
            'FormEntry.TEntry',
            font=('Helvetica', 12)
        )

        # Contenedor principal
        main_frame = ttk.Frame(self, style='MainFrame.TFrame')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Etiqueta y campo de entrada para la cédula
        ttk.Label(
            main_frame,
            text="Cédula del usuario:",
            style='FormLabel.TLabel'
        ).grid(row=0, column=0, padx=10, pady=(30, 10), sticky='e')

        self.entry_cedula = ttk.Entry(main_frame, style='FormEntry.TEntry')
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=(30, 10), sticky='w')
        self.entry_cedula.focus_set()

        # Espacio para separar los botones
        boton_frame = ttk.Frame(main_frame)
        boton_frame.grid(row=1, column=0, columnspan=2, pady=(10, 30))

        # Botón Generar
        ttk.Button(
            boton_frame,
            text="Generar",
            style='Success.TButton',
            width=8,
            command=self.generar_reporte
        ).pack(side='left', padx=10)

        # Botón Cancelar
        ttk.Button(
            boton_frame,
            text="Cancelar",
            style='Danger.TButton',
            width=8,
            command=self.cerrar
        ).pack(side='left', padx=10)

        # Etiqueta para mostrar el resultado
        self.label_resultado = ttk.Label(main_frame, text="", style='Info.TLabel')
        self.label_resultado.grid(row=2, column=0, columnspan=2, pady=(0, 20))

    def validar_cedula(self, cedula: str) -> bool:
        """Valida que la cédula contenga solo números y tenga longitud válida."""
        if not cedula.isdigit():
            messagebox.showwarning("Advertencia", "La cédula debe contener solo números.")
            return False
        if len(cedula) < 6 or len(cedula) > 10:
            messagebox.showwarning("Advertencia", "La cédula debe tener entre 6 y 10 dígitos.")
            return False
        return True

    def generar_reporte(self):
        """Genera el reporte de asistencias del usuario."""
        cedula = self.entry_cedula.get().strip()

        if not self.validar_cedula(cedula):
            return

        try:
            if not self.conexion.conectar():
                raise Exception("Error de conexión a la base de datos")

            cursor = self.conexion.connection.cursor()

            # Consulta SQL para contar asistencias en el mes actual
            cursor.execute(
                "SELECT COUNT(*) FROM asistencias "
                "WHERE cedula_usuario = ? AND MONTH(fecha) = ?",
                (cedula, datetime.datetime.now().month)
            )
            asistencias = cursor.fetchone()[0]

            # Calcular días laborables dinámicamente
            dias_laborables = self.calcular_dias_laborables(datetime.datetime.now().year, datetime.datetime.now().month)
            inasistencias = dias_laborables - asistencias

            # Mostrar resultados
            resultado = f"Reporte Mensual:\n- Días Asistidos: {asistencias}\n- Inasistencias: {inasistencias}"
            self.label_resultado.config(text=resultado)

            self.conexion.desconectar()
        except Exception as e:
            logging.error(f"Error al generar el reporte: {str(e)}")
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")

    def calcular_dias_laborables(self, year: int, month: int) -> int:
        """Calcula dinámicamente los días laborables en un mes dado."""
        import calendar
        cal = calendar.Calendar()
        dias_laborables = 0
        for day in cal.itermonthdays(year, month):
            if day != 0 and calendar.weekday(year, month, day) < 5:  # Lunes a Viernes
                dias_laborables += 1
        return dias_laborables

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
        root.withdraw()  # Oculta la ventana raíz
        app = Ventana(root)
        app.mainloop()  # Ejecuta el bucle principal de la interfaz gráfica
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")