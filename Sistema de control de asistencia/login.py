import tkinter as tk
from tkinter import messagebox
from core.conexion import Conexion
from OpSist import mostrar_opciones_sistema

def mostrar_ventana_login(parent):
    login = VentanaLogin(parent)
    login.mainloop()

class VentanaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        self.geometry("400x300")
        self.configure(bg='navy')
        self.centrar_ventana()
        self.crear_interfaz()
        self.parent = parent  # Guardamos referencia a la ventana principal

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea los elementos de la ventana de login."""
        label_style = {'bg': 'navy', 'fg': 'white', 'font': ('Helvetica', 12, 'bold')}
        tk.Label(self, text="Cédula:", **label_style).pack(pady=10)
        self.entry_usuario = tk.Entry(self, justify='center', font=('Helvetica', 12))
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()

        tk.Label(self, text="Contraseña:", **label_style).pack(pady=10)
        self.entry_contrasena = tk.Entry(self, show="*", justify='center', font=('Helvetica', 12))
        self.entry_contrasena.pack(pady=5)

        # Manejo de teclas "Enter"
        self.entry_usuario.bind("<Return>", lambda event: self.entry_contrasena.focus())
        self.entry_contrasena.bind("<Return>", self.validar_usuario)

        # Frame para los botones
        frame_buttons = tk.Frame(self, bg='navy')
        frame_buttons.pack(pady=20)

        tk.Button(
            frame_buttons,
            text="Iniciar",
            bg="#FFFF00",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=10,
            height=2,
            command=self.validar_usuario
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            frame_buttons,
            text="Cerrar",
            bg="#FF0000",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=10,
            height=2,
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=10)

    def validar_usuario(self, event=None):
        """Valida las credenciales del usuario contra la base de datos."""
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Debe ingresar cédula y contraseña.")
            return

        try:
            conexion = Conexion('ASISTENCIAS_JFS')  # Reemplaza con el nombre de tu base de datos
            if conexion.conectar():
                cursor = conexion.connection.cursor()
                query = "SELECT * FROM USUARIOS WHERE cedula_id = ? AND contrasena = ?"
                cursor.execute(query, (usuario, contrasena))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                    self.destroy()  # Cierra la ventana de login
                    self.parent.destroy()  # Cierra la ventana principal (main.py)
                    mostrar_opciones_sistema()  # Abre la ventana principal
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals() and conexion.connection:
                conexion.connection.close()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()
        mostrar_ventana_login(root)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")
