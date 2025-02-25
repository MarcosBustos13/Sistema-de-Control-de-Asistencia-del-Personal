import tkinter as tk
from tkinter import Menu, messagebox
import os

# Asegúrate de que este módulo existe y es accesible
try:
    from core.estilos import Estilos
except ImportError:
    print("Advertencia: No se pudo importar el módulo 'core.estilos'. Usando valores predeterminados.")
    class Estilos:
        def __init__(self):
            self.colores = {"fondo": "#000080"}

class MainApp:
    def __init__(self, root):
        print("Inicializando MainApp")
        self.root = root
        self.estilos = Estilos()  # Instancia de estilos
        self.configurar_ventana_principal()
        self.crear_interfaz()
        self.crear_menu_completo()

    def configurar_ventana_principal(self):
        """Configura la ventana principal de la aplicación."""
        print("Configurando ventana principal")
        self.root.title("Sistema de Control de Asistencias")
        self.root.configure(bg=self.estilos.colores.get("fondo", "#000080"))  # Fondo azul oscuro
        self.root.geometry("1550x870")
        self.root.minsize(1000, 600)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.centrar_ventana(1550, 870)

    def centrar_ventana(self, ancho, alto):
        """Centra la ventana en la pantalla."""
        print("Centrando ventana en la pantalla")
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea los elementos de la interfaz gráfica."""
        print("Creando interfaz")
        main_frame = tk.Frame(self.root, bg=self.estilos.colores.get("fondo", "#000080"))
        main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        # Título del liceo
        titulo_liceo = tk.Label(
            main_frame,
            text="U.E. Liceo Bolivariano José Félix Sánchez",
            font=('Helvetica', 24, 'bold'),
            fg="#FFFFFF",
            bg=self.estilos.colores.get("fondo", "#000080")
        )
        titulo_liceo.pack(pady=20)

        # Logo con manejo seguro
        try:
            ruta_logo = os.path.join(os.path.dirname(__file__), "logo.png")
            if os.path.exists(ruta_logo):
                self.logo = tk.PhotoImage(file=ruta_logo)
                lbl_logo = tk.Label(main_frame, image=self.logo, bg=self.estilos.colores.get("fondo", "#000080"))
                lbl_logo.image = self.logo  # Mantener referencia
                lbl_logo.pack(pady=20)
            else:
                print("El archivo del logo no fue encontrado.")
                messagebox.showwarning("Advertencia", "El archivo del logo no fue encontrado.")
        except Exception as e:
            print(f"Error al cargar el logo: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar el logo: {str(e)}")

    def crear_menu_completo(self):
        """Crea el menú principal con estilos consistentes."""
        print("Creando menú completo")
        menu_principal = Menu(self.root)

        # Menú Usuarios
        submenu_usuario = self.crear_submenu_usuarios()
        menu_principal.add_cascade(label="Registrar Usuario", menu=submenu_usuario)

        # Menú Asistencia
        submenu_asistencias = self.crear_submenu_asistencias()
        menu_principal.add_cascade(label="Registrar Asistencia", menu=submenu_asistencias)

        # Menú Reportes
        submenu_reportes = self.crear_submenu_reportes()
        menu_principal.add_cascade(label="Reportes", menu=submenu_reportes)

        # Menú Mantenimiento
        submenu_mantenimiento = self.crear_submenu_mantenimiento()
        menu_principal.add_cascade(label="Mantenimiento", menu=submenu_mantenimiento)

        # Configurar el menú en la ventana principal
        self.root.config(menu=menu_principal)

    def crear_submenu_usuarios(self):
        """Crea el submenú de usuarios."""
        submenu = Menu(self.root, tearoff=0)
        submenu.add_command(label="Ingresar", command=lambda: self.abrir_modulo('usuarios.ingresar_usuario'))
        submenu.add_command(label="Consultar", command=lambda: self.abrir_modulo('usuarios.consultar_usuario'))
        submenu.add_command(label="Editar", command=lambda: self.abrir_modulo('usuarios.editar_usuario'))
        submenu.add_command(label="Eliminar", command=lambda: self.abrir_modulo('usuarios.eliminar_usuario'))
        return submenu

    def crear_submenu_asistencias(self):
        """Crea el submenú de asistencias."""
        submenu = Menu(self.root, tearoff=0)
        submenu.add_command(label="Ingresar Entrada", command=lambda: self.abrir_modulo('asistencias.ingresar_he', clase_ventana='VentanaEntrada'))
        submenu.add_command(label="Ingresar Salida", command=lambda: self.abrir_modulo('asistencias.ingresar_hs', clase_ventana='VentanaSalida'))

        # Corrección para consultar asistencia
        submenu.add_command(label="Consultar", command=lambda: self.abrir_modulo('asistencias.consultar_asistencia', clase_ventana='VentanaConsultarAsistencia'))

        # Corrección para editar asistencia
        submenu.add_command(label="Editar", command=lambda: self.abrir_modulo('asistencias.editar_asistencia', clase_ventana='VentanaEditarAsistencia'))

        # Corrección para eliminar asistencia
        submenu.add_command(label="Eliminar", command=lambda: self.abrir_modulo('asistencias.eliminar_asistencia', clase_ventana='VentanaEliminarAsistencia'))

        return submenu

    def crear_submenu_reportes(self):
        """Crea el submenú de reportes."""
        submenu = Menu(self.root, tearoff=0)
        submenu.add_command(label="Reporte Individual", command=lambda: self.abrir_modulo('reportes.reporte_individual'))
        return submenu

    def crear_submenu_mantenimiento(self):
        """Crea el submenú de mantenimiento."""
        submenu = Menu(self.root, tearoff=0)
        submenu.add_command(label="Bitácora", command=lambda: self.abrir_modulo('bitacora'))
        # Submenú Respaldo
        submenu_respaldo = Menu(submenu, tearoff=0)
        submenu_respaldo.add_command(label="Crear Respaldo", command=lambda: self.abrir_modulo('mantenimiento.respaldo.crear_respaldo'))
        submenu_respaldo.add_command(label="Restaurar", command=lambda: self.abrir_modulo('mantenimiento.respaldo.restaurar'))
        submenu.add_cascade(label="Respaldo", menu=submenu_respaldo)
        submenu.add_command(label="Manual", command=lambda: self.abrir_modulo('mantenimiento.manual'))
        return submenu

    def abrir_modulo(self, nombre_modulo: str, clase_ventana: str = 'Ventana'):
        """Abre un módulo de manera segura con manejo de errores."""
        try:
            print(f"Abriendo módulo: {nombre_modulo}, Clase: {clase_ventana}")
            modulo = __import__(nombre_modulo, fromlist=[clase_ventana])
            VentanaClase = getattr(modulo, clase_ventana)
            ventana = VentanaClase(self.root)
            ventana.grab_set()  # Hacer la ventana modal
        except ModuleNotFoundError as e:
            messagebox.showinfo(
                "Módulo no encontrado",
                f"No se pudo encontrar el módulo '{nombre_modulo}'.\nDetalles: {e}",
                parent=self.root
            )
        except AttributeError as e:
            messagebox.showerror(
                "Clase no encontrada",
                f"No se pudo encontrar la clase '{clase_ventana}' en el módulo '{nombre_modulo}'.\nDetalles: {e}",
                parent=self.root
            )
        except Exception as e:
            messagebox.showerror(
                "Error inesperado",
                f"Ocurrió un error al cargar '{nombre_modulo}'.\nDetalles: {e}",
                parent=self.root
            )

def mostrar_opciones_sistema():
    """Inicia la ventana principal de opciones del sistema."""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    mostrar_opciones_sistema()

