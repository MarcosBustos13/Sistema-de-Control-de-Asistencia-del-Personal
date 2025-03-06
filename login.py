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
        self.parent = parent

    def centrar_ventana(self):
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        label_style = {'bg': 'navy', 'fg': 'white', 'font': ('Helvetica', 12, 'bold')}
        tk.Label(self, text="Cédula:", **label_style).pack(pady=10)
        self.entry_usuario = tk.Entry(self, justify='center', font=('Helvetica', 12))
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.focus()

        tk.Label(self, text="Contraseña:", **label_style).pack(pady=10)
        self.entry_contrasena = tk.Entry(self, show="*", justify='center', font=('Helvetica', 12))
        self.entry_contrasena.pack(pady=5)

        self.entry_usuario.bind("<Return>", lambda event: self.entry_contrasena.focus())
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
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        
        if not usuario or not contrasena:
            messagebox.showwarning("Advertencia", "Debe ingresar cédula y contraseña.")
            return
	
        try:
            conexion = Conexion('ASISTENCIAS_JFS')
            if conexion.conectar():
                cursor = conexion.connection.cursor()
                
                # 1. Validar usuario
                query_usuario = "SELECT id FROM USUARIOS WHERE cedula_id = ? AND contrasena = ?"
                cursor.execute(query_usuario, (usuario, contrasena))
                user = cursor.fetchone()

                if user:
                    # 2. Insertar en bitácora (SOLO ESTE BLOQUE ES NUEVO)
                    query_bitacora = """
                        INSERT INTO BITACORA (usuario_id, accion) 
                        VALUES (?, 'Inicio de sesión exitoso')
                    """
                    cursor.execute(query_bitacora, (user[0],))
                    conexion.connection.commit()
                    
                    # 3. Comportamiento original
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                    self.destroy()
                    self.parent.destroy()
                    mostrar_opciones_sistema()  # Se llama SIN argumentos como en la versión original
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
