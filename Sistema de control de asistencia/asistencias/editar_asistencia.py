import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class VentanaEditarAsistencia(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Editar Asistencia")
        self.configure(background='#000080')
        self.geometry("450x300")
        self.resizable(False, False)
        self.centrar_ventana()
        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = 450
        alto = 300
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        main_frame = tk.Frame(self, bg='#000080')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        tk.Label(
            main_frame,
            text="Cédula:",
            font=('Helvetica', 12),
            fg='#FFFFFF',
            bg='#000080'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_cedula = tk.Entry(main_frame, width=25)
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(
            main_frame,
            text="Fecha (YYYY-MM-DD):",
            font=('Helvetica', 12),
            fg='#FFFFFF',
            bg='#000080'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_fecha = tk.Entry(main_frame, width=25)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        tk.Label(
            main_frame,
            text="Nueva Hora Entrada (HH:MM:SS):",
            font=('Helvetica', 12),
            fg='#FFFFFF',
            bg='#000080'
        ).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_entrada = tk.Entry(main_frame, width=25)
        self.entry_entrada.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        tk.Label(
            main_frame,
            text="Nueva Hora Salida (HH:MM:SS):",
            font=('Helvetica', 12),
            fg='#FFFFFF',
            bg='#000080'
        ).grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_salida = tk.Entry(main_frame, width=25)
        self.entry_salida.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Botones
        btn_frame = tk.Frame(main_frame, bg='#000080')
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        tk.Button(
            btn_frame,
            text="Cargar",
            command=self.cargar
        ).pack(side='left', padx=5)
        tk.Button(
            btn_frame,
            text="Guardar",
            command=self.guardar
        ).pack(side='left', padx=5)
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.cerrar
        ).pack(side='left', padx=5)

        # Ajustar las columnas para centrar los elementos
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)

    def cargar(self):
        cedula = self.entry_cedula.get().strip()
        fecha = self.entry_fecha.get().strip()
        if not cedula or not fecha:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        if not self.validar_fecha(fecha):
            messagebox.showwarning("Advertencia", "El formato de la fecha debe ser YYYY-MM-DD.")
            return
        try:
            # Aquí deberías agregar la lógica para cargar los datos de la base de datos
            # y mostrar los resultados en los campos correspondientes.
            # Simulación de datos cargados
            self.entry_entrada.delete(0, tk.END)
            self.entry_entrada.insert(0, "08:00:00")
            self.entry_salida.delete(0, tk.END)
            self.entry_salida.insert(0, "17:00:00")
            messagebox.showinfo("Información", "Datos cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")

    def guardar(self):
        cedula = self.entry_cedula.get().strip()
        fecha = self.entry_fecha.get().strip()
        nueva_entrada = self.entry_entrada.get().strip()
        nueva_salida = self.entry_salida.get().strip()
        if not cedula or not fecha or not nueva_entrada or not nueva_salida:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return
        if not self.validar_fecha(fecha):
            messagebox.showwarning("Advertencia", "El formato de la fecha debe ser YYYY-MM-DD.")
            return
        try:
            # Aquí deberías agregar la lógica para guardar los datos en la base de datos
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el registro: {str(e)}")

    def validar_fecha(self, fecha: str) -> bool:
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def cerrar(self):
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