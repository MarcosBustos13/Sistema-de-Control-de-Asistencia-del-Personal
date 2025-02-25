import tkinter as tk
from PIL import Image, ImageTk
import os

from login import mostrar_ventana_login

class VentanaInicio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Control de Asistencia")
        self.geometry("1550x850")
        self.resizable(False, False)
        self.configure(background="#000080")
        self.centrar_ventana()
        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea los elementos de la ventana de inicio."""
        # Cargar el logo del colegio con manejo seguro
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((200, 200), Image.LANCZOS)
                logo = ImageTk.PhotoImage(logo_image)
                # Mostrar el logo del colegio
                logo_label = tk.Label(self, image=logo, bg="#000080")
                logo_label.image = logo  # Mantener referencia para evitar que el garbage collector lo elimine
                logo_label.pack(pady=60)
            except Exception as e:
                print(f"Error al cargar el logo: {str(e)}")
                tk.Label(
                    self,
                    text="Logo no disponible",
                    font=("Helvetica", 14, 'bold'),
                    fg="white",
                    bg="#000080"
                ).pack(pady=40)
        else:
            print("El archivo del logo no fue encontrado.")
            tk.Label(
                self,
                text="Logo no disponible",
                font=("Helvetica", 14, 'bold'),
                fg="white",
                bg="#000080"
            ).pack(pady=40)

        # Mostrar el mensaje de bienvenida
        tk.Label(
            self,
            text="BIENVENIDOS AL SISTEMA DE CONTROL DE ASISTENCIA\n"
                 "U.E. LICEO BOLIVARIANO JUAN FÉLIX SÁNCHEZ",
            font=("Helvetica", 24, 'bold'),
            fg="white",
            bg="#000080",
            justify="center"
        ).pack(pady=50)

        # Crear un marco para los botones
        button_frame = tk.Frame(self, bg="#000080")
        button_frame.pack(side=tk.RIGHT, anchor=tk.N, padx=20)  # Reubicar el marco a la derecha y alinear al norte (arriba)

        # Botón "SIGUIENTE"
        btn_siguiente = tk.Button(
            button_frame,
            text="SIGUIENTE",
            bg="#FFFF00",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=15,
            height=2,
            command=self.abrir_login
        )
        btn_siguiente.pack(pady=20)  # Botón "SIGUIENTE"

        # Botón "SALIR"
        btn_salir = tk.Button(
            button_frame,
            text="SALIR",
            bg="#FFFF00",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=15,
            height=2,
            command=self.salir
        )
        btn_salir.pack(pady=20)  # Botón "SALIR"

    def abrir_login(self):
        """Abre la ventana de inicio de sesión."""
        print("Abriendo ventana de login...")
        mostrar_ventana_login(self)  # Abre la ventana de login

    def salir(self):
        """Cierra el programa."""
        self.quit()

if __name__ == "__main__":
    app = VentanaInicio()
    app.mainloop()
