# respaldo.restaurar.py
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil
import logging

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Ventana(tk.Toplevel):
    """
    Ventana para restaurar respaldos.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Restaurar Respaldo")
        self.geometry("400x300")  # Tamaño ajustado
        self.configure(background="#001F3F")  # Fondo navy
        self.resizable(False, False)

        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configurar_estilos()

        # Centrar la ventana
        self.centrar_ventana()

        # Contenedor principal
        main_frame = ttk.Frame(self, style="MainFrame.TFrame")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Etiqueta de información
        lbl_info = ttk.Label(main_frame, text="Archivo de respaldo (.zip):", style="FormLabel.TLabel")
        lbl_info.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="w")

        # Campo de entrada para el archivo
        self.entry_archivo = ttk.Entry(main_frame, width=40, style="FormEntry.TEntry")
        self.entry_archivo.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Botón para seleccionar archivo
        btn_browse = ttk.Button(
            main_frame,
            text="Seleccionar Archivo",
            style="FormButton.TButton",
            command=self.seleccionar_archivo
        )
        btn_browse.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Etiqueta para ubicación de destino
        lbl_destino = ttk.Label(main_frame, text="Directorio de destino:", style="FormLabel.TLabel")
        lbl_destino.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="w")

        # Campo de entrada para la ubicación de destino
        self.entry_destino = ttk.Entry(main_frame, width=40, style="FormEntry.TEntry")
        self.entry_destino.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Botón para seleccionar ubicación de destino
        btn_destino = ttk.Button(
            main_frame,
            text="Seleccionar Destino",
            style="FormButton.TButton",
            command=self.seleccionar_destino
        )
        btn_destino.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Botón para restaurar
        btn_restaurar = ttk.Button(
            main_frame,
            text="Restaurar",
            style="FormButton.TButton",
            command=self.restaurar_respaldo
        )
        btn_restaurar.grid(row=4, column=0, columnspan=2, pady=20)

        # Protocolo para cerrar la ventana
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def _configurar_estilos(self):
        """Configura los estilos para los widgets."""
        self.style.configure(
            "FormLabel.TLabel",
            background="#001F3F",  # Fondo navy
            foreground="#FFFFFF",  # Texto blanco
            font=("Arial", 12),
        )
        self.style.configure(
            "FormEntry.TEntry",
            fieldbackground="white",  # Fondo blanco
            foreground="black",       # Texto negro
            font=("Arial", 12),
        )
        self.style.configure(
            "FormButton.TButton",
            background="#FFFFFF",     # Fondo blanco
            foreground="#000000",     # Texto negro
            font=("Arial", 12, "bold"),
            padding=5,
        )
        self.style.map(
            "FormButton.TButton",
            background=[("active", "#E0E0E0")],  # Color al hacer clic
        )
        self.style.configure(
            "MainFrame.TFrame",
            background="#001F3F",  # Fondo navy
        )

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

    def seleccionar_archivo(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo ZIP.
        """
        archivo = filedialog.askopenfilename(filetypes=[("Archivos ZIP", "*.zip")])
        if archivo:
            self.entry_archivo.delete(0, tk.END)
            self.entry_archivo.insert(0, archivo)

    def seleccionar_destino(self):
        """
        Abre un cuadro de diálogo para seleccionar la ubicación de destino.
        """
        destino = filedialog.askdirectory()
        if destino:
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, destino)

    def restaurar_respaldo(self):
        """
        Restaura un archivo ZIP en el directorio especificado.
        """
        archivo = self.entry_archivo.get().strip()
        destino = self.entry_destino.get().strip()

        if not archivo:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo.")
            return

        if not os.path.exists(archivo):
            messagebox.showerror("Error", "El archivo no existe.")
            return

        if not destino:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un directorio de destino.")
            return

        try:
            # Extraer el archivo ZIP
            shutil.unpack_archive(archivo, destino)
            logging.info(f"Respaldo restaurado en: {destino}")
            messagebox.showinfo("Éxito", f"Respaldo restaurado en: {destino}")
        except Exception as e:
            logging.error(f"No se pudo restaurar el respaldo: {str(e)}")
            messagebox.showerror("Error", f"No se pudo restaurar el respaldo:\n{str(e)}")

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