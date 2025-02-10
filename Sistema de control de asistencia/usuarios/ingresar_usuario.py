# ingresar_usuario.py
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import logging
from core.conexion import Conexion
from core.estilos import Estilos
import hashlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Ventana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.widgets = {}
        self.estilos = Estilos()
        self.conexion = Conexion(db_name='ASISTENCIAS_JFS')
        self.connection = self.conexion.conectar()
        if not self.connection:
            messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")
            self.destroy()
            return
        self.title("Ingresar Personal")
        self.geometry("500x600")
        self.resizable(False, False)
        self.configure(background=self.estilos.colores.get('fondo', '#000080'))
        self._centrar_ventana()
        self.tipo_trabajador = self._cargar_tipo_trabajador()
        self._crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self._cerrar)
        self.widgets['cedula_id'].focus()

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho, alto = 500, 600
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _cargar_tipo_trabajador(self):
        """Carga los tipos de trabajador desde la base de datos."""
        try:
            query = "SELECT id, descripcion FROM TIPO_DE_PERSONAL"
            cursor = self.conexion.ejecutar_consulta(query)
            return {row[1]: row[0] for row in cursor.fetchall()} if cursor else {}
        except Exception as e:
            logging.error(f"Error cargando tipos de personal: {str(e)}")
            return {}

    def _crear_interfaz(self):
        """Crea la interfaz gráfica de la ventana."""
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
            ("Contraseña*:", "contrasena")  # Campo de contraseña
        ]
        for idx, (label, field) in enumerate(campos):
            # Etiqueta alineada a la derecha
            tk.Label(self, text=label, font=('Helvetica', 12), fg='white', bg=self.estilos.colores.get('fondo', '#000080')).grid(
                row=idx, column=0, padx=15, pady=8, sticky='e'
            )
            
            # Crear el widget correspondiente
            if field == 'tipo_trabajador':
                self.widgets[field] = ttk.Combobox(self, values=list(self.tipo_trabajador.keys()), state='readonly')
            elif field == 'contrasena':  # Campo de contraseña
                self.widgets[field] = ttk.Entry(self, show="*")  # Mostrar asteriscos
            else:
                self.widgets[field] = ttk.Entry(self)
            
            # Ajustar el ancho de los campos de entrada
            self.widgets[field].config(width=25)  # Reducir el ancho
            
            self.widgets[field].grid(row=idx, column=1, padx=15, pady=8, sticky='ew')
            # Validaciones específicas
            if field == 'cedula_id':
                self.widgets[field].config(validate="key", validatecommand=(self.register(self._validar_cedula), "%P"))
            elif field == 'nro_telf':
                self.widgets[field].config(validate="key", validatecommand=(self.register(self._validar_numeros), "%P"))
            elif field == 'e_mail':
                self.widgets[field].bind("<FocusOut>", self._validar_email)
            # Enlazar la tecla "Enter" para avanzar al siguiente campo
            self.widgets[field].bind("<Return>", lambda event, next_field=field: self._avanzar_cursor(next_field))
        
        # Agregar una fila vacía antes de los botones
        tk.Label(self, text="", bg=self.estilos.colores.get('fondo', '#000080')).grid(row=len(campos), column=0, columnspan=2)
        # Botones ajustados más abajo
        ttk.Button(self, text="Guardar", command=self._procesar_guardado).grid(row=len(campos) + 1, column=0, columnspan=1, pady=20)
        ttk.Button(self, text="Cancelar", command=self._cerrar).grid(row=len(campos) + 1, column=1, columnspan=1, pady=20)

    def _validar_cedula(self, value):
        """Valida que la cédula contenga solo números y tenga un máximo de 8 dígitos."""
        if value.isdigit() and len(value) <= 8:
            return True
        elif value == "":
            return True  # Permitir borrar el campo
        return False

    def _validar_numeros(self, value):
        """Valida que el campo contenga solo números."""
        return value.isdigit() or value == ""

    def _validar_email(self, event):
        """Valida el formato del correo electrónico."""
        email = self.widgets['e_mail'].get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Advertencia", "El correo electrónico debe tener un formato válido (ejemplo@dominio.com).")
            self.widgets['e_mail'].focus()

    def _avanzar_cursor(self, current_field):
        """Avanza el cursor al siguiente campo cuando se presiona Enter."""
        fields = list(self.widgets.keys())
        current_index = fields.index(current_field)
        if current_index < len(fields) - 1:
            next_field = fields[current_index + 1]
            self.widgets[next_field].focus()

    def _procesar_guardado(self):
        """Procesa y guarda los datos del usuario en la base de datos."""
        datos = {campo: self.widgets[campo].get().strip() for campo in self.widgets}
        campos_obligatorios = ['cedula_id', 'primer_apellido', 'primer_nombre', 'fecha_nac', 'domicilio', 'nro_telf', 'e_mail', 'tipo_trabajador', 'contrasena']
        if any(not datos[c] for c in campos_obligatorios):
            messagebox.showwarning("Advertencia", "Todos los campos marcados con * deben estar completos.")
            return
        
        try:
            # Validar fecha de nacimiento
            datos['fecha_nac'] = datetime.strptime(datos['fecha_nac'], "%d/%m/%Y").strftime("%Y-%m-%d")
            
            # Hashear la contraseña
            datos['contrasena'] = hashlib.sha256(datos['contrasena'].encode()).hexdigest()
            
            # Obtener el ID del tipo de trabajador
            tipo_trabajador_id = self.tipo_trabajador.get(datos['tipo_trabajador'])
            if not tipo_trabajador_id:
                messagebox.showwarning("Advertencia", "Seleccione un tipo de personal válido.")
                return
            
            # Insertar datos en la base de datos
            query = """
            INSERT INTO USUARIOS (cedula_id, nacionalidad, primer_apellido, segundo_apellido, primer_nombre, segundo_nombre, fecha_nac, domicilio, nro_telf, e_mail, tipo_trabajador, contrasena)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.conexion.ejecutar_consulta(query, (
                datos['cedula_id'], datos['nacionalidad'], datos['primer_apellido'], datos['segundo_apellido'],
                datos['primer_nombre'], datos['segundo_nombre'], datos['fecha_nac'], datos['domicilio'],
                datos['nro_telf'], datos['e_mail'], tipo_trabajador_id, datos['contrasena']
            ))
            messagebox.showinfo("Éxito", "Usuario guardado exitosamente.")
            self._cerrar()
        except ValueError:
            messagebox.showerror("Error", "La fecha de nacimiento debe tener el formato DD/MM/AAAA.")
        except Exception as e:
            logging.error(f"Error al guardar el usuario: {str(e)}")
            messagebox.showerror("Error", "No se pudo guardar el usuario.")

    def _cerrar(self):
        """Cierra la ventana."""
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    Ventana(root)
    root.mainloop()