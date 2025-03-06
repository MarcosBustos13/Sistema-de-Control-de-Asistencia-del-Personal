import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import logging
from core.conexion import Conexion

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VentanaConsultarAsistencia(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Consulta de Asistencias")
        self.geometry("800x500")
        self.configure(background="navy")
        self.conexion = Conexion('ASISTENCIAS_JFS')
        
        if not self.conexion.conectar():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            self.destroy()
            return
        
        self.crear_interfaz()
        self.centrar_ventana()
        self.entry_cedula.focus()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 800
        alto = 500
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea la interfaz gráfica de la ventana."""
        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Campo de búsqueda
        search_frame = ttk.Frame(main_frame, style='TFrame')
        search_frame.pack(pady=10)
        ttk.Label(search_frame, text="Cédula:", style='TLabel').pack(side=tk.LEFT, padx=5)
        self.entry_cedula = ttk.Entry(search_frame, width=15, font=('Arial', 12))
        self.entry_cedula.pack(side=tk.LEFT, padx=5)
        self.entry_cedula.bind("<Return>", lambda event: self.consultar_asistencia())

        # Botones Buscar, Limpiar y Cancelar
        btn_buscar = ttk.Button(search_frame, text="Buscar", command=self.consultar_asistencia, style='TButton')
        btn_buscar.pack(side=tk.LEFT, padx=5)
        btn_limpiar = ttk.Button(search_frame, text="Limpiar", command=self.limpiar_campos, style='TButton')
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        btn_cancelar = ttk.Button(search_frame, text="Cancelar", command=self.cerrar_conexion, style='TButton')
        btn_cancelar.pack(side=tk.LEFT, padx=5)

        # Tabla de resultados
        tree_frame = ttk.Frame(main_frame, style='TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Fecha", "Hora de Entrada", "Hora de Salida"),
            show="headings",
            height=15
        )
        self.tree.heading("Fecha", text="Fecha", anchor=tk.CENTER)
        self.tree.heading("Hora de Entrada", text="Hora de Entrada", anchor=tk.CENTER)
        self.tree.heading("Hora de Salida", text="Hora de Salida", anchor=tk.CENTER)
        self.tree.column("Fecha", width=200, anchor=tk.CENTER)
        self.tree.column("Hora de Entrada", width=200, anchor=tk.CENTER)
        self.tree.column("Hora de Salida", width=200, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def consultar_asistencia(self):
        cedula = self.entry_cedula.get().strip()
        logging.info(f"Cédula ingresada: {cedula}")

        if not cedula:
            messagebox.showwarning("Advertencia", "Por favor ingrese una cédula válida.")
            return

        if not cedula.isdigit():
            messagebox.showwarning("Error", "La cédula debe ser un valor numérico.")
            return

        try:
            if not self.conexion.connection:
                messagebox.showerror("Error", "No hay conexión a la base de datos.")
                return

            cursor = self.conexion.connection.cursor()
            query = """
                SELECT fecha AS Fecha,
                       MIN(hora_entrada) AS Entrada,
                       MAX(hora_salida) AS Salida
                FROM ASISTENCIA
                WHERE cedula_id = ?
                GROUP BY fecha
                ORDER BY fecha DESC
            """
            logging.info(f"Ejecutando consulta con cédula: {cedula}")
            cursor.execute(query, (cedula,))
            registros = cursor.fetchall()
            logging.info(f"Registros obtenidos: {registros}")

            self.tree.delete(*self.tree.get_children())

            if registros:
                for registro in registros:
                    fecha = registro.Fecha.strftime("%d/%m/%Y")
                    entrada = registro.Entrada.strftime("%H:%M:%S")
                    salida = registro.Salida.strftime("%H:%M:%S") if registro.Salida else "--"
                    self.tree.insert("", tk.END, values=(fecha, entrada, salida))
            else:
                messagebox.showinfo("Información", "No se encontraron registros para esta cédula.")
        except pyodbc.Error as e:
            logging.error(f"Error de base de datos: {str(e)}")
            messagebox.showerror("Error", f"Error al consultar: {str(e)}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def limpiar_campos(self):
        self.entry_cedula.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())

    def cerrar_conexion(self):
        try:
            if self.conexion and self.conexion.connection:
                self.conexion.desconectar()
        except Exception as e:
            logging.error(f"Error al cerrar la conexión: {str(e)}")
        finally:
            self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = VentanaConsultarAsistencia(root)
    root.mainloop()
