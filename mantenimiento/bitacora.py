import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class ConexionBD:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
            return True
        except pyodbc.Error as e:
            messagebox.showerror("Error BD", f"Error de conexión:\n{str(e)}")
            return False

    def obtener_incidencias(self):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        b.id,
                        FORMAT(b.fecha, 'dd/MM/yyyy HH:mm') AS fecha,
                        u.cedula_id,
                        b.accion
                    FROM BITACORA b
                    INNER JOIN USUARIOS u ON b.usuario_id = u.id
                    ORDER BY b.fecha DESC
                """)
                return cursor.fetchall()
        except pyodbc.Error as e:
            messagebox.showerror("Error BD", f"Error al leer registros:\n{str(e)}")
            return []
        finally:
            self.conexion.commit()

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()

class VentanaBitacora(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bitácora del Sistema")
        self.geometry("1200x600")
        self.configure(bg='navy')  # Fondo navy
        self.conexion = ConexionBD('DESKTOP-E6O194D\\SQLEXPRESS', 'ASISTENCIAS_JFS')
        
        if not self.conexion.conectar():
            self.destroy()
            return
        
        self.crear_interfaz()
        self.actualizar_tabla()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self, bg='navy')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(main_frame, bg='navy')
        btn_frame.pack(pady=5, fill=tk.X)

        # Configurar estilo para botones
        style = ttk.Style()
        style.configure("Navy.TButton", 
                        background="navy", 
                        foreground="white",
                        font=('Arial', 10, 'bold'),
                        padding=5)
        style.map("Navy.TButton", 
                  background=[('active', '#000080')])

        ttk.Button(
            btn_frame,
            text="🔄 Actualizar",
            command=self.actualizar_tabla,
            style="Navy.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="❌ Cerrar",
            command=self.destroy,
            style="Navy.TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Configurar estilo de la tabla
        style.configure("Navy.Treeview", 
                        background="#f0f0f0", 
                        fieldbackground="#f0f0f0", 
                        foreground="black",
                        font=('Arial', 10))
        style.configure("Navy.Treeview.Heading", 
                        background="navy", 
                        foreground="white",
                        font=('Arial', 10, 'bold'))
        style.map("Navy.Treeview.Heading", 
                  background=[('active', '#000080')])

        # Tabla
        self.tabla = ttk.Treeview(
            main_frame,
            columns=("ID", "Fecha", "Cédula", "Acción"),
            show="headings",
            style="Navy.Treeview"
        )

        self.tabla.heading("ID", text="ID Registro")
        self.tabla.heading("Fecha", text="Fecha y Hora")
        self.tabla.heading("Cédula", text="Cédula del Usuario")
        self.tabla.heading("Acción", text="Acción realizada")

        self.tabla.column("ID", width=80, stretch=tk.NO)
        self.tabla.column("Fecha", width=150)
        self.tabla.column("Cédula", width=150)
        self.tabla.column("Acción", width=700)

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        registros = self.conexion.obtener_incidencias()
        if registros:
            for registro in registros:
                self.tabla.insert("", tk.END, values=(
                    registro[0],  # ID
                    registro[1],  # Fecha
                    registro[2],  # Cédula
                    registro[3]   # Acción
                ))

    def cerrar_aplicacion(self):
        if self.conexion:
            self.conexion.cerrar_conexion()
        self.destroy()

# Bloque de prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = VentanaBitacora(root)
    app.mainloop()
