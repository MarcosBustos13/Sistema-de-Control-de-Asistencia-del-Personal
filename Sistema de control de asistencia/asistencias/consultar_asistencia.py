# consultar_asistencia.py
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
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

class VentanaConsultarAsistencia(tk.Toplevel):
    """
    Ventana para consultar las asistencias de un usuario en determinadas fechas.
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
        self.title("Consultar Asistencia")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self.geometry("600x400")
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 600
        alto = 400
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
            text="Cédula del usuario:",
            font=('Helvetica', 12),
            foreground=self.estilos.colores.get('texto', '#FFFFFF'),
            background=self.estilos.colores.get('fondo', '#000080')
        ).grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.entry_cedula = ttk.Entry(main_frame, style='FormEntry.TEntry', width=20)
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_cedula.focus_set()

        # Botones para realizar la búsqueda y borrar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        ttk.Button(
            btn_frame,
            text="Buscar",
            style='Success.TButton',
            command=self.buscar
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text="Borrar",
            style='Danger.TButton',
            command=self.borrar
        ).pack(side='left', padx=5)

        # Treeview para mostrar los resultados
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Scrollbars para el Treeview
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Fecha", "Entrada", "Salida"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            style='Treeview'
        )

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Entrada", text="Hora de Entrada")
        self.tree.heading("Salida", text="Hora de Salida")

        self.tree.column("Fecha", width=150, anchor="center")
        self.tree.column("Entrada", width=150, anchor="center")
        self.tree.column("Salida", width=150, anchor="center")

        self.tree.grid(row=0, column=0, sticky='nsew')
        tree_scroll_y.grid(row=0, column=1, sticky='ns')
        tree_scroll_x.grid(row=1, column=0, sticky='ew')

        # Configuración responsive
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

    def buscar(self):
        """Realiza la búsqueda de asistencias en la base de datos."""
        cedula = self.entry_cedula.get().strip()

        if not cedula:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una cédula.")
            return

        try:
            if not self.conexion.conectar():
                raise Exception("Error de conexión a la base de datos")
            cursor = self.conexion.connection.cursor()

            # Consulta SQL para obtener las asistencias del usuario
            cursor.execute(
                "SELECT fecha, hora_entrada, hora_salida FROM ASISTENCIA WHERE usuario = (SELECT id FROM USUARIOS WHERE cedula_id = ?)",
                (cedula,)
            )
            resultados = cursor.fetchall()

            if resultados:
                # Limpiar el Treeview antes de insertar nuevos resultados
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Insertar los resultados en el Treeview
                for row in resultados:
                    fecha = row[0].strftime('%Y-%m-%d') if isinstance(row[0], datetime) else row[0]
                    entrada = row[1].strftime('%H:%M:%S') if isinstance(row[1], datetime) else row[1]
                    salida = row[2].strftime('%H:%M:%S') if isinstance(row[2], datetime) else row[2]
                    self.tree.insert("", "end", values=(fecha, entrada, salida))
            else:
                messagebox.showinfo("Información", "No se encontraron registros para la cédula proporcionada.")

            self.conexion.desconectar()
        except Exception as e:
            logging.error(f"Error al consultar la base de datos: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error al consultar la base de datos: {str(e)}")

    def borrar(self):
        """Limpia el campo de entrada y el Treeview para realizar otra búsqueda."""
        self.entry_cedula.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)

    def cerrar(self):
        """Cierra la ventana y desconecta la base de datos."""
        try:
            if self.conexion:
                if self.conexion.connection is not None and not self.conexion.connection.closed:
                    self.conexion.desconectar()
        except Exception as e:
            logging.error(f"Error al cerrar la conexión: {str(e)}")
        finally:
            self.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()
        app = VentanaConsultarAsistencia(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")