
        # crear_respaldo.py
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil
from datetime import datetime
import logging

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Ventana(tk.Toplevel):
    """
    Ventana para crear respaldos de directorios.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Crear Respaldo")
        self.geometry("400x300")  # Tamaño ajustado
        self.configure(background="#001F3F")  # Fondo navy
        self.resizable(False, False)

        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "TLabel",
            background="#001F3F",  # Fondo navy
            foreground="#FFFFFF",  # Texto blanco
            font=("Arial", 12),
        )
        self.style.configure(
            "TButton",
            background="#FFFFFF",  # Fondo blanco
            foreground="#000000",  # Texto negro
            font=("Arial", 12, "bold"),
            padding=5,
        )
        self.style.map(
            "TButton",
            background=[("active", "#E0E0E0")],  # Color al hacer clic
        )
        self.style.configure(
            "TEntry",
            fieldbackground="white",
            foreground="black",
            font=("Arial", 12),
        )

        # Centrar la ventana
        self.centrar_ventana()

        # Contenedor principal
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Etiqueta de información
        lbl_info = ttk.Label(main_frame, text="Directorio a respaldar:", style="TLabel")
        lbl_info.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        # Campo de entrada para el directorio
        self.entry_directorio = ttk.Entry(main_frame, width=40, style="TEntry")
        self.entry_directorio.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Botón para seleccionar directorio
        btn_browse = ttk.Button(
            main_frame,
            text="Seleccionar Directorio",
            style="TButton",
            command=self.seleccionar_directorio
        )
        btn_browse.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Etiqueta para ubicación de destino
        lbl_destino = ttk.Label(main_frame, text="Ubicación de destino:", style="TLabel")
        lbl_destino.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")

        # Campo de entrada para la ubicación de destino
        self.entry_destino = ttk.Entry(main_frame, width=40, style="TEntry")
        self.entry_destino.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Botón para seleccionar ubicación de destino
        btn_destino = ttk.Button(
            main_frame,
            text="Seleccionar Destino",
            style="TButton",
            command=self.seleccionar_destino
        )
        btn_destino.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Botón para generar respaldo
        btn_respaldar = ttk.Button(
            main_frame,
            text="Generar Respaldo",
            style="TButton",
            command=self.crear_respaldo
        )
        btn_respaldar.grid(row=4, column=0, columnspan=2, pady=20)

        # Protocolo para cerrar la ventana
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def centrar_ventana(self):
        """
        Centra la ventana en la pantalla.
        """
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"+{x}+{y}")

    def seleccionar_directorio(self):
        """
        Abre un cuadro de diálogo para seleccionar un directorio.
        """
        directorio = filedialog.askdirectory()
        if directorio:
            self.entry_directorio.delete(0, tk.END)
            self.entry_directorio.insert(0, directorio)

    def seleccionar_destino(self):
        """
        Abre un cuadro de diálogo para seleccionar la ubicación de destino.
        """
        destino = filedialog.askdirectory()
        if destino:
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, destino)

    def crear_respaldo(self):
        """
        Crea un archivo ZIP con el contenido del directorio seleccionado.
        """
        directorio = self.entry_directorio.get().strip()
        destino = self.entry_destino.get().strip()

        if not directorio:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un directorio.")
            return

        if not os.path.exists(directorio):
            messagebox.showerror("Error", "El directorio no existe.")
            return

        if not destino:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una ubicación de destino.")
            return

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_respaldo = f"respaldo_{fecha}.zip"
        ruta_completa = os.path.join(destino, nombre_respaldo)

        try:
            # Crear el archivo ZIP
            shutil.make_archive(ruta_completa.replace(".zip", ""), "zip", directorio)
            logging.info(f"Respaldo creado: {ruta_completa}")
            messagebox.showinfo("Éxito", f"Respaldo creado: {nombre_respaldo}")
        except Exception as e:
            logging.error(f"No se pudo crear el respaldo: {str(e)}")
            messagebox.showerror("Error", f"No se pudo crear el respaldo:\n{str(e)}")

    def cerrar(self):
        """
        Cierra la ventana.
        """
        self.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        app = Ventana(root)
        app.mainloop()
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        messagebox.showerror("Error", "Ocurrió un error inesperado en la aplicación")