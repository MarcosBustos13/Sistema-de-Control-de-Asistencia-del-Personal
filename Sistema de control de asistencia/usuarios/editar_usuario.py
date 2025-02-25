import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from core.conexion import Conexion
from core.estilos import Estilos

class Ventana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Editar Usuario")
        self.geometry("1100x600")  # Ancho fijo para ver todas las columnas
        self.configure(background="navy")
        self.estilos = Estilos()
        self.db = Conexion(db_name='ASISTENCIAS_JFS')
        self.configurar_estilos()
        self.crear_interfaz()
        self.centrar_ventana()
        # Configurar el cursor en la primera casilla
        self.entry_cedula.focus()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 1100
        alto = 600
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def configurar_estilos(self):
        """Configura los estilos de la interfaz."""
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.estilo.configure('TFrame', background=self.estilos.colores.get('fondo', 'navy'))
        self.estilo.configure('TLabel', background=self.estilos.colores.get('fondo', 'navy'), foreground='white', font=('Arial', 12, 'bold'))
        self.estilo.configure('TButton', background='white', foreground='black', font=('Arial', 12, 'bold'))
        self.estilo.configure('Treeview',
                              background="white",
                              foreground="black",
                              rowheight=25,
                              font=('Arial', 10))
        self.estilo.map('Treeview', background=[('selected', '#347083')])

    def crear_interfaz(self):
        """Crea la interfaz gráfica de la ventana."""
        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.grid(padx=20, pady=20, sticky='nsew')

        # Campo de búsqueda
        search_frame = ttk.Frame(main_frame, style='TFrame')
        search_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky='n')
        ttk.Label(search_frame, text="Cédula del usuario:", style='TLabel').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_cedula = ttk.Entry(search_frame, width=15, font=('Arial', 12))  # Ajustar el ancho
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.entry_cedula.bind("<Return>", self.enfocar_siguiente)
        self.entry_cedula.config(validate='key', validatecommand=(self.register(self._validar_max_length), '%P', '%d', 8))

        ttk.Button(search_frame, text="Buscar", command=self.buscar_usuario, style='TButton').grid(row=0, column=2, padx=10, pady=5, sticky='w')
        ttk.Button(search_frame, text="Limpiar", command=self.limpiar_busqueda, style='TButton').grid(row=0, column=3, padx=10, pady=5, sticky='w')

        # Tabla de resultados
        self.tabla = ttk.Treeview(main_frame, columns=('Nacionalidad', 'Nombres', 'Email', 'Teléfono', 'Tipo', 'Fecha Nac.', 'Domicilio'))
        self.tabla.heading('#0', text='ID')
        self.tabla.heading('Nacionalidad', text='Nacionalidad')
        self.tabla.heading('Nombres', text='Nombres y Apellidos')
        self.tabla.heading('Email', text='Correo Electrónico')
        self.tabla.heading('Teléfono', text='Teléfono')
        self.tabla.heading('Tipo', text='Tipo Trabajador')
        self.tabla.heading('Fecha Nac.', text='Fecha Nac.')
        self.tabla.heading('Domicilio', text='Domicilio')
        self.tabla.column('#0', width=50, anchor='center')
        self.tabla.column('Nacionalidad', width=80, anchor='center')
        self.tabla.column('Nombres', width=200)
        self.tabla.column('Email', width=150)
        self.tabla.column('Teléfono', width=100, anchor='center')
        self.tabla.column('Tipo', width=100, anchor='center')
        self.tabla.column('Fecha Nac.', width=100, anchor='center')
        self.tabla.column('Domicilio', width=300)
        self.tabla.grid(row=1, column=0, columnspan=3, pady=20, sticky='nsew')

        # Botones Editar y Cerrar
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky='n')
        ttk.Button(btn_frame, text="Editar", command=self.abrir_ventana_editar, style='TButton').grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(btn_frame, text="Cerrar", command=self._cerrar, style='TButton').grid(row=0, column=1, padx=10, pady=5)

        # Configuración responsive
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def enfocar_siguiente(self, event):
        """Avanza el cursor al siguiente campo cuando se presiona Enter."""
        event.widget.tk_focusNext().focus()
        return "break"

    def _validar_max_length(self, valor, accion, max_length):
        """Valida que el campo no exceda una longitud máxima."""
        if accion == '1':  # Inserción de caracteres
            return len(valor) <= int(max_length) and valor.isdigit()
        return True  # Permitir borrado de caracteres

    def buscar_usuario(self):
        """Busca un usuario en la base de datos y muestra los resultados en la tabla."""
        cedula = self.entry_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Advertencia", "Ingrese un número de cédula.")
            return

        try:
            if not self.db.conectar():
                raise Exception("Error de conexión a la base de datos.")

            cursor = self.db.connection.cursor()
            cursor.execute("""
                SELECT 
                    id,
                    nacionalidad,
                    CONCAT(primer_nombre, ' ', COALESCE(segundo_nombre, ''), ' ', 
                          primer_apellido, ' ', COALESCE(segundo_apellido, '')),
                    e_mail,
                    nro_telf,
                    CASE tipo_trabajador
                        WHEN 1 THEN 'Docente'
                        WHEN 2 THEN 'Administrativo'
                        WHEN 3 THEN 'Obrero'
                    END,
                    fecha_nac,
                    domicilio
                FROM usuarios 
                WHERE cedula_id = ?""", (cedula,))
            resultado = cursor.fetchone()

            self.tabla.delete(*self.tabla.get_children())
            if resultado:
                self.tabla.insert('', 'end',
                                  text=resultado[0],
                                  values=(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6], resultado[7]))
            else:
                messagebox.showinfo("Información", "No se encontró el usuario.")
            self.db.desconectar()
        except pyodbc.Error as e:
            messagebox.showerror("Error BD", f"Error en base de datos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_busqueda(self):
        """Limpia los campos de búsqueda y la tabla."""
        self.entry_cedula.delete(0, tk.END)
        self.tabla.delete(*self.tabla.get_children())
        self.entry_cedula.focus()

    def abrir_ventana_editar(self):
        """Abre una ventana para editar los datos del usuario seleccionado."""
        selected_item = self.tabla.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para editar.")
            return

        item = self.tabla.item(selected_item)
        user_id = item['text']
        valores = item['values']

        # Crear la ventana de edición
        editar_ventana = tk.Toplevel(self)
        editar_ventana.title("Editar Usuario")
        editar_ventana.geometry("400x400")
        editar_ventana.configure(background="navy")
        
        ttk.Label(editar_ventana, text="Editar datos del usuario", font=('Arial', 14, 'bold')).pack(pady=10)

        # Campos de edición
        labels = ["Nacionalidad:", "Nombres y Apellidos:", "Correo Electrónico:", "Teléfono:", "Tipo Trabajador:", "Fecha Nac:", "Domicilio:"]
        self.edit_entries = []

        for idx, label_text in enumerate(labels):
            frame = ttk.Frame(editar_ventana, style='TFrame')
            frame.pack(pady=5)
            ttk.Label(frame, text=label_text, style='TLabel').pack(side='left')
            
            if label_text == "Tipo Trabajador:":
                # Usar un Combobox para el tipo de trabajador
                combo = ttk.Combobox(frame, values=["Docente", "Administrativo", "Obrero"], state="readonly")
                combo.set(valores[idx])
                combo.pack(side='left')
                self.edit_entries.append(combo)
            else:
                entry = ttk.Entry(frame, width=30)
                entry.insert(0, valores[idx])
                entry.pack(side='left')
                self.edit_entries.append(entry)

        # Botón para guardar cambios
        ttk.Button(editar_ventana, text="Guardar Cambios", command=lambda: self.guardar_cambios(user_id, editar_ventana), style='TButton').pack(pady=20)

    def guardar_cambios(self, user_id, ventana):
        """Guarda los cambios del usuario en la base de datos."""
        nuevos_valores = [entry.get() for entry in self.edit_entries]

        # Separar los nombres y apellidos para que coincidan con los campos de la base de datos
        nombres_completos = nuevos_valores[1].split()
        primer_nombre = nombres_completos[0]
        segundo_nombre = nombres_completos[1] if len(nombres_completos) > 2 else ''
        primer_apellido = nombres_completos[-2] if len(nombres_completos) > 2 else nombres_completos[1]
        segundo_apellido = nombres_completos[-1] if len(nombres_completos) > 2 else ''

        # Convertir el tipo de trabajador de texto a número
        tipo_trabajador_texto = nuevos_valores[4]
        if tipo_trabajador_texto == "Docente":
            tipo_trabajador = 1
        elif tipo_trabajador_texto == "Administrativo":
            tipo_trabajador = 2
        elif tipo_trabajador_texto == "Obrero":
            tipo_trabajador = 3
        else:
            messagebox.showwarning("Advertencia", "Tipo de trabajador no válido.")
            return

        try:
            if not self.db.conectar():
                raise Exception("Error de conexión a la base de datos.")

            cursor = self.db.connection.cursor()
            cursor.execute("""
                UPDATE usuarios SET
                    nacionalidad = ?,
                    primer_nombre = ?,
                    segundo_nombre = ?,
                    primer_apellido = ?,
                    segundo_apellido = ?,
                    e_mail = ?,
                    nro_telf = ?,
                    tipo_trabajador = ?,
                    fecha_nac = ?,
                    domicilio = ?
                WHERE id = ?
            """, (nuevos_valores[0], primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, nuevos_valores[2], nuevos_valores[3], tipo_trabajador, nuevos_valores[5], nuevos_valores[6], user_id))

            self.db.connection.commit()
            messagebox.showinfo("Éxito", "Datos del usuario actualizados correctamente.")
            self.db.desconectar()
            ventana.destroy()
            self.buscar_usuario()  # Actualizar la tabla con los nuevos datos
        except pyodbc.Error as e:
            messagebox.showerror("Error BD", f"Error en base de datos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cerrar(self):
        """Cierra la ventana."""
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Ventana(root)
    root.mainloop()
