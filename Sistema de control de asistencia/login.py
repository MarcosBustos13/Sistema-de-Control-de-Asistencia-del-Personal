import tkinter as tk
from tkinter import messagebox
from core.conexion import Conexion
from OpSist import mostrar_opciones_sistema  # Importar la función correcta

def mostrar_ventana_login(parent):
    login = VentanaLogin(parent)
    login.mainloop()

class VentanaLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.geometry("300x200")
        self.configure(bg='navy')
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
        """Crea los elementos de la ventana de login."""
        label_style = {'bg': 'navy', 'fg': 'white', 'font': ('Helvetica', 10, 'bold')}
        tk.Label(self, text="Cédula:", **label_style).pack(pady=10)
        self.entry_usuario = tk.Entry(self, justify='center')
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()

        tk.Label(self, text="Contraseña:", **label_style).pack(pady=10)
        self.entry_contrasena = tk.Entry(self, show="*", justify='center')
        self.entry_contrasena.pack(pady=5)

        def on_entry_enter(event, next_entry):
            next_entry.focus()

        self.entry_usuario.bind("<Return>", lambda event: on_entry_enter(event, self.entry_contrasena))
        self.entry_contrasena.bind("<Return>", self.validar_usuario)

        frame_buttons = tk.Frame(self, bg='navy')
        frame_buttons.pack(pady=20)

        tk.Button(
            frame_buttons,
            text="Iniciar",
            bg="#FFFF00",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=10,
            height=3,
            command=self.validar_usuario
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            frame_buttons,
            text="Cerrar",
            bg="#FFFF00",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=12,
            height=3,
            command=self.quit
        ).pack(side=tk.LEFT, padx=8)

    def validar_usuario(self, event=None):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Debe ingresar cédula y contraseña")
            return

        conexion = Conexion('ASISTENCIAS_JFS')
        if conexion.conectar():
            try:
                cursor = conexion.connection.cursor()
                cursor.execute("SELECT * FROM USUARIOS WHERE cedula_id = ? AND contrasena = ?", (usuario, contrasena))
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("Éxito", "Conexión exitosa")
                    self.destroy()
                    # Mostrar la ventana de opciones del sistema
                    mostrar_opciones_sistema()
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar la consulta: {str(e)}")
            finally:
                cursor.close()
                conexion.connection.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    mostrar_ventana_login(root)
    root.mainloop()