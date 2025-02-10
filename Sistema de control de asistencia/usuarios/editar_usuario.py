# editar_usuario.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import hashlib
from core.conexion import Conexion  # Importación absoluta
from core.estilos import Estilos  # Importar la clase Estilos

class VentanaSolicitarCedula(tk.Toplevel):
    def __init__(self, parent, db_name):
        super().__init__(parent)
        self.parent = parent
        self.db_name = db_name
        self.widgets = {}
        self.estilos = Estilos()  # Inicializar los estilos
        # Configuración esencial
        self.title("Editar Usuario")
        self.geometry("300x150")
        self.resizable(False, False)
        self.configure(background=self.estilos.colores["fondo"])  # Fondo navy
        self._centrar_ventana()
        # Crear interfaz
        self._crear_interfaz()
        self.widgets['cedula_id'].focus()

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_interfaz(self):
        """Crea la interfaz de la ventana."""
        main_frame = ttk.Frame(self, style='TFrame')  # Usa el estilo TFrame
        main_frame.grid(padx=25, pady=25, sticky='nsew')
        # Cédula ID
        self._crear_campo(main_frame, "Cédula ID:", 'cedula_id', 0)
        # Botones
        self._crear_botones(main_frame, 1)

    def _crear_campo(self, parent, etiqueta, nombre_campo, fila):
        """Crea un campo de entrada con su etiqueta."""
        lbl = ttk.Label(
            parent,
            text=etiqueta,
            style='TLabel'  # Usa el estilo TLabel
        )
        lbl.grid(row=fila, column=0, padx=15, pady=8, sticky='w')
        self.widgets[nombre_campo] = ttk.Entry(parent)
        self.widgets[nombre_campo].grid(row=fila, column=1, padx=15, pady=8, sticky='ew')

    def _crear_botones(self, parent, fila):
        """Crea los botones de la interfaz."""
        btn_frame = ttk.Frame(parent, style='TFrame')  # Usa el estilo TFrame
        btn_frame.grid(row=fila, column=0, columnspan=2, pady=20)
        btn_aceptar = ttk.Button(btn_frame, text="Aceptar", command=self._aceptar, style='TButton')
        btn_aceptar.grid(row=0, column=0, padx=10)
        btn_cancelar = ttk.Button(btn_frame, text="Cancelar", command=self._cerrar, style='TButton')
        btn_cancelar.grid(row=0, column=1, padx=10)
        # Centrar los botones
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

    def _aceptar(self):
        """Valida la cédula ingresada y abre la ventana de edición."""
        cedula = self.widgets['cedula_id'].get()
        if not cedula.isdigit() or len(cedula) != 8:
            messagebox.showwarning("Advertencia", "Ingrese una cédula válida de 8 dígitos.")
            return
        # Verificar si la cédula existe en la base de datos
        conexion = Conexion(self.db_name)
        conexion.conectar()
        query = "SELECT * FROM usuarios WHERE cedula_id = ?"
        cursor = conexion.ejecutar_consulta(query, (cedula,))
        if cursor and cursor.fetchone():
            self.destroy()
            VentanaEditarUsuario(self.parent, cedula, self.db_name)
        else:
            messagebox.showwarning("Advertencia", "La cédula no existe en la base de datos.")
        conexion.desconectar()

    def _cerrar(self):
        """Cierra la ventana."""
        self.destroy()


class VentanaEditarUsuario(tk.Toplevel):
    def __init__(self, parent, cedula_id, db_name):
        super().__init__(parent)
        self.parent = parent
        self.cedula_id = cedula_id
        self.db_name = db_name
        self.widgets = {}
        self.estilos = Estilos()  # Inicializar los estilos
        # Configuración esencial
        self.title("Editar Usuario")
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(background=self.estilos.colores["fondo"])  # Fondo navy
        self._centrar_ventana()
        # Crear interfaz
        self._crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        # Cargar datos del usuario desde la base de datos
        self.buscar_usuario()

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_interfaz(self):
        """Crea la interfaz de la ventana."""
        main_frame = ttk.Frame(self, style='TFrame')  # Usa el estilo TFrame
        main_frame.grid(padx=25, pady=25, sticky='nsew')
        # Lista de campos
        campos = [
            ("Cédula ID*:", "cedula_id"),
            ("Nacionalidad (V/E):", "nacionalidad"),
            ("Primer Apellido*:", "primer_apellido"),
            ("Segundo Apellido:", "segundo_apellido"),
            ("Primer Nombre*:", "primer_nombre"),
            ("Segundo Nombre:", "segundo_nombre"),
            ("Fecha Nac. (DD/MM/AAAA)*:", "fecha_nac"),
            ("Domicilio*:", "domicilio"),
            ("Teléfono*:", "nro_telf"),
            ("Email*:", "e_mail"),
            ("Tipo de Personal*:", "tipo_trabajador"),
            ("Contraseña:", "contrasena")
        ]
        # Crear widgets
        for idx, (etiqueta, campo) in enumerate(campos):
            self._crear_campo(main_frame, etiqueta, campo, idx)
        # Botones
        self._crear_botones(main_frame, len(campos) + 1)

    def _crear_campo(self, parent, etiqueta, campo, fila):
        """Crea un campo de entrada con su etiqueta."""
        lbl = ttk.Label(
            parent,
            text=etiqueta,
            style='TLabel'  # Usa el estilo TLabel
        )
        lbl.grid(row=fila, column=0, padx=15, pady=8, sticky='w')
        if campo == 'tipo_trabajador':
            self._crear_combobox_trabajador(parent, fila)
        else:
            entry = ttk.Entry(parent)
            if campo == 'contrasena':
                entry.config(show='•')
            if campo == 'e_mail':
                entry.bind("<FocusOut>", self._validar_email_completo)
            entry.grid(row=fila, column=1, padx=15, pady=8, sticky='ew')
            self.widgets[campo] = entry

    def _crear_combobox_trabajador(self, parent, fila):
        """Crea un Combobox para seleccionar el tipo de personal."""
        combo = ttk.Combobox(
            parent,
            values=['Docente', 'Administrativo', 'Obrero'],
            state='readonly',
        )
        combo.grid(row=fila, column=1, padx=15, pady=8, sticky='ew')
        combo.set('Seleccione...')
        self.widgets['tipo_trabajador'] = combo

    def _crear_botones(self, parent, fila):
        """Crea los botones de la interfaz."""
        btn_frame = ttk.Frame(parent, style='TFrame')  # Usa el estilo TFrame
        btn_frame.grid(row=fila, column=0, columnspan=2, pady=20)
        btn_guardar = ttk.Button(btn_frame, text="Guardar Cambios", command=self._procesar_guardado, style='TButton')
        btn_guardar.grid(row=0, column=0, padx=10)
        btn_cancelar = ttk.Button(btn_frame, text="Cancelar", command=self._cerrar, style='TButton')
        btn_cancelar.grid(row=0, column=1, padx=10)
        # Centrar los botones
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

    def _validar_email_completo(self, event):
        """Valida el formato del email."""
        email = self.widgets['e_mail'].get()
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Advertencia", "El formato del email no es válido")

    def buscar_usuario(self):
        """Carga los datos del usuario desde la base de datos."""
        conexion = Conexion(self.db_name)
        conexion.conectar()
        query = """
        SELECT cedula_id, nacionalidad, primer_apellido, segundo_apellido,
        primer_nombre, segundo_nombre, fecha_nac, domicilio,
        nro_telf, e_mail, tipo_trabajador
        FROM usuarios
        WHERE cedula_id = ?
        """
        cursor = conexion.ejecutar_consulta(query, (self.cedula_id,))
        if cursor:
            usuario = cursor.fetchone()
            if usuario:
                self.cargar_datos_usuario(usuario)
            else:
                messagebox.showwarning("Advertencia", "Usuario no encontrado.")
        conexion.desconectar()

    def cargar_datos_usuario(self, usuario):
        """Carga los datos del usuario en los campos."""
        campos = [
            "cedula_id", "nacionalidad", "primer_apellido", "segundo_apellido",
            "primer_nombre", "segundo_nombre", "fecha_nac", "domicilio",
            "nro_telf", "e_mail", "tipo_trabajador"
        ]
        for campo, valor in zip(campos, usuario):
            if campo == 'tipo_trabajador':
                self.widgets[campo].set(valor)
            else:
                self.widgets[campo].delete(0, tk.END)
                self.widgets[campo].insert(0, valor)

    def _procesar_guardado(self):
        """Procesa el guardado de los datos del usuario en la base de datos."""
        datos = {campo: self.widgets[campo].get() for campo in self.widgets}
        # Validar campos obligatorios
        campos_obligatorios = ['cedula_id', 'nacionalidad', 'primer_apellido', 'primer_nombre', 'fecha_nac', 'domicilio',
                               'nro_telf', 'e_mail', 'tipo_trabajador']
        if any(not datos[campo] for campo in campos_obligatorios):
            messagebox.showwarning("Advertencia", "Todos los campos marcados con * son obligatorios")
            return
        # Validar formato de fecha
        try:
            datetime.strptime(datos['fecha_nac'], "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Advertencia", "El formato de la fecha no es válido (DD/MM/AAAA)")
            return
        # Validar tipo de personal
        if datos['tipo_trabajador'] == 'Seleccione...':
            messagebox.showwarning("Advertencia", "Seleccione un tipo de personal válido")
            return
        # Encriptar contraseña
        if datos.get('contrasena'):
            datos['contrasena'] = hashlib.sha256(datos['contrasena'].encode()).hexdigest()
        # Guardar cambios en la base de datos
        conexion = Conexion(self.db_name)
        conexion.conectar()
        try:
            query = """
            UPDATE usuarios
            SET nacionalidad = ?, primer_apellido = ?, segundo_apellido = ?,
            primer_nombre = ?, segundo_nombre = ?, fecha_nac = ?,
            domicilio = ?, nro_telf = ?, e_mail = ?, tipo_trabajador = ?,
            contrasena = ?
            WHERE cedula_id = ?
            """
            params = (
                datos['nacionalidad'], datos['primer_apellido'], datos['segundo_apellido'],
                datos['primer_nombre'], datos['segundo_nombre'], datos['fecha_nac'],
                datos['domicilio'], datos['nro_telf'], datos['e_mail'], datos['tipo_trabajador'],
                datos.get('contrasena', ''), self.cedula_id
            )
            # Depuración: Mostrar los datos que se enviarán a la consulta
            print("Datos a actualizar:", params)
            cursor = conexion.ejecutar_consulta(query, params)
            if cursor:
                # Verificar que los cambios se hayan aplicado correctamente
                query_verificacion = "SELECT * FROM usuarios WHERE cedula_id = ?"
                cursor_verificacion = conexion.ejecutar_consulta(query_verificacion, (self.cedula_id,))
                if cursor_verificacion and cursor_verificacion.fetchone():
                    messagebox.showinfo("Éxito", "El usuario ha sido actualizado exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo verificar la actualización en la base de datos.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar el usuario: {str(e)}")
        finally:
            conexion.desconectar()
            self._cerrar()

    def _cerrar(self):
        """Cierra la ventana."""
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    db_name = "ASISTENCIAS_JFS"  # Cambia esto por el nombre de tu base de datos
    VentanaSolicitarCedula(root, db_name)
    root.mainloop()