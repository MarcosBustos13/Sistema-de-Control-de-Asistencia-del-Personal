import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    def __init__(self, parent):
        super().__init__(parent)
        self.estilos = Estilos()
        self.conexion = Conexion("ASISTENCIAS_JFS")
        self.resultados = None  # Para almacenar los resultados
        self.nombre_usuario = None  # Para almacenar el nombre del usuario

        self.configurar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def configurar_ventana(self):
        self.title("Reporte Individual")
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self.geometry("500x550")  # Aumentamos el tamaño para mostrar más información
        self.resizable(False, False)
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        ancho, alto = 500, 550
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        etiqueta_estilo = {"background": self.estilos.colores.get('fondo', '#000080'), "foreground": "white"}

        ttk.Label(main_frame, text="Cédula del usuario:", background=etiqueta_estilo["background"], foreground=etiqueta_estilo["foreground"]).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_cedula = ttk.Entry(main_frame)
        self.entry_cedula.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.entry_cedula.focus_set()

        ttk.Label(main_frame, text="Año:", background=etiqueta_estilo["background"], foreground=etiqueta_estilo["foreground"]).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_anio = ttk.Entry(main_frame)
        self.entry_anio.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(main_frame, text="Mes:", background=etiqueta_estilo["background"], foreground=etiqueta_estilo["foreground"]).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.combo_mes = ttk.Combobox(main_frame, values=[
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.combo_mes.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        ttk.Label(main_frame, text="Días hábiles:", background=etiqueta_estilo["background"], foreground=etiqueta_estilo["foreground"]).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.combo_dias_habiles = ttk.Combobox(main_frame, values=[str(i) for i in range(10, 31)])
        self.combo_dias_habiles.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        boton_frame = ttk.Frame(main_frame)
        boton_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(boton_frame, text="Calcular", command=self.calcular_asistencia).pack(side='left', padx=10)
        ttk.Button(boton_frame, text="Cancelar", command=self.cerrar).pack(side='left', padx=10)

        # Frame para mostrar los resultados
        self.resultado_frame = ttk.Frame(main_frame)
        self.resultado_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Cuadro de texto para mostrar los resultados
        self.text_resultado = tk.Text(self.resultado_frame, height=10, width=50, wrap=tk.WORD)
        self.text_resultado.pack()
        self.text_resultado.config(state=tk.DISABLED)  # Hacerlo de solo lectura

        # Frame para los botones de generar PDF y cerrar
        botones_frame = ttk.Frame(self.resultado_frame)
        botones_frame.pack(pady=10)

        ttk.Button(botones_frame, text="Generar PDF", command=self.generar_pdf).pack(side='left', padx=10)
        ttk.Button(botones_frame, text="Cerrar", command=self.cerrar).pack(side='left', padx=10)

    def calcular_asistencia(self):
        cedula = self.entry_cedula.get().strip()
        anio = self.entry_anio.get().strip()
        mes = self.combo_mes.get().strip()
        dias_habiles = self.combo_dias_habiles.get().strip()

        meses = {
            "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04",
            "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08",
            "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
        }

        if not cedula.isdigit():
            messagebox.showwarning("Advertencia", "La cédula debe contener solo números.")
            return

        if not anio.isdigit() or len(anio) != 4:
            messagebox.showwarning("Advertencia", "El año debe ser un número de 4 dígitos.")
            return

        if mes not in meses:
            messagebox.showwarning("Advertencia", "Debe seleccionar un mes válido.")
            return

        if not dias_habiles.isdigit():
            messagebox.showwarning("Advertencia", "Debe seleccionar la cantidad de días hábiles.")
            return

        try:
            if not self.conexion.conectar():
                raise Exception("Error de conexión a la base de datos")

            cursor = self.conexion.connection.cursor()

            # Obtener los nombres y apellidos del usuario desde la tabla USUARIOS
            cursor.execute(
                "SELECT primer_apellido, segundo_apellido, primer_nombre, segundo_nombre FROM USUARIOS WHERE cedula_id = ?",
                (cedula,)
            )
            usuario = cursor.fetchone()
            if not usuario:
                raise Exception("No se encontró el usuario con la cédula proporcionada.")

            # Concatenar nombres y apellidos para formar el nombre completo
            primer_apellido, segundo_apellido, primer_nombre, segundo_nombre = usuario
            nombre_completo = f"{primer_nombre} {segundo_nombre} {primer_apellido} {segundo_apellido}".strip()
            self.nombre_usuario = nombre_completo

            # Consulta para contar las asistencias
            cursor.execute(
                "SELECT COUNT(DISTINCT fecha) FROM ASISTENCIA WHERE cedula_id = ? AND YEAR(fecha) = ? AND MONTH(fecha) = ?",
                (cedula, int(anio), int(meses[mes]))
            )
            asistencias = cursor.fetchone()[0]
            inasistencias = int(dias_habiles) - asistencias
            self.conexion.desconectar()

            self.resultados = (cedula, self.nombre_usuario, mes, anio, asistencias, inasistencias)  # Guardar resultados
            resultado_texto = (
                f"Cédula: {cedula}\n"
                f"Nombre: {self.nombre_usuario}\n"
                f"Mes: {mes} {anio}\n"
                f"Asistencias: {asistencias}\n"
                f"Inasistencias: {inasistencias}"
            )

            # Mostrar los resultados en el cuadro de texto
            self.text_resultado.config(state=tk.NORMAL)
            self.text_resultado.delete(1.0, tk.END)
            self.text_resultado.insert(tk.END, resultado_texto)
            self.text_resultado.config(state=tk.DISABLED)

        except Exception as e:
            logging.error(f"Error al calcular la asistencia: {str(e)}")
            messagebox.showerror("Error", f"Error al calcular la asistencia: {str(e)}")

    def generar_pdf(self):
        if not self.resultados:
            messagebox.showwarning("Advertencia", "No hay resultados para generar el PDF.")
            return

        try:
            # Pedir al usuario dónde guardar el PDF
            ruta_archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")],
                title="Guardar PDF como"
            )
            if not ruta_archivo:
                return  # El usuario canceló la operación

            # Crear el PDF
            c = canvas.Canvas(ruta_archivo, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Escribir los resultados en el PDF
            c.drawString(100, 750, "Reporte de Asistencia Individual")
            c.drawString(100, 730, f"Cédula: {self.resultados[0]}")
            c.drawString(100, 710, f"Nombre: {self.resultados[1]}")
            c.drawString(100, 690, f"Mes: {self.resultados[2]} {self.resultados[3]}")
            c.drawString(100, 670, f"Asistencias: {self.resultados[4]}")
            c.drawString(100, 650, f"Inasistencias: {self.resultados[5]}")

            c.save()
            messagebox.showinfo("Éxito", f"El PDF se ha guardado en: {ruta_archivo}")

        except Exception as e:
            logging.error(f"Error al generar el PDF: {str(e)}")
            messagebox.showerror("Error", f"Error al generar el PDF: {str(e)}")

    def cerrar(self):
        try:
            # Desconectar la base de datos si está conectada
            if self.conexion and self.conexion.connection:
                self.conexion.desconectar()
        except Exception as e:
            logging.error(f"Error al cerrar la conexión: {str(e)}")
        
        # Cerrar la ventana
        self.destroy()

# Ejecutar la ventana
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    ventana = Ventana(root)
    ventana.mainloop()
